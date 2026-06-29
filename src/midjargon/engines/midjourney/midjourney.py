#!/usr/bin/env python3
# this_file: src/midjargon/engines/midjourney/midjourney.py
"""Parse a MidjargonDict into a validated MidjourneyPrompt."""

from __future__ import annotations

from typing import Any

from midjargon.core.models import ImageReference, MidjourneyParameters, MidjourneyPrompt
from pydantic import HttpUrl

# ---------------------------------------------------------------------------
# Aliases: short / alternative key names → canonical parameter field name
# ---------------------------------------------------------------------------
_KEY_ALIASES: dict[str, str] = {
    "ar": "aspect",
    "aspect_ratio": "aspect",
    "v": "version",
    "s": "stylize",
    "c": "chaos",
    "w": "weird",
    "iw": "image_weight",
    "q": "quality",
    "cw": "character_weight",
    "sw": "style_weight",
    "sv": "style_version",
    "r": "repeat",
    "p": "personalization",
    "cref": "character_reference",
    "sref": "style_reference",
    "image_prompts": "images",   # normalise to "images"
}

# ---------------------------------------------------------------------------
# Per-parameter numeric ranges for explicit range validation.
# These raise ValueError (not Pydantic ValidationError) so pytest.raises works.
# ---------------------------------------------------------------------------
_PARAM_RANGES: dict[str, tuple[float, float]] = {
    "stylize":          (0.0,  1000.0),
    "chaos":            (0.0,  100.0),
    "weird":            (0.0,  3000.0),
    "image_weight":     (0.0,  2.0),
    "quality":          (0.25, 2.0),
    "character_weight": (0.0,  200.0),
    "style_weight":     (0.0,  1000.0),
    "style_version":    (1,    3),
    "repeat":           (1,    40),
    "stop":             (10,   100),
}


def _convert_numeric(raw: str) -> int | float:
    """Convert a numeric string to int (if whole) or float."""
    f = float(raw)
    return int(f) if f.is_integer() else f


def _validate_range(name: str, value: int | float) -> None:
    """Raise ValueError if *value* is outside the allowed range for *name*."""
    if name not in _PARAM_RANGES:
        return
    lo, hi = _PARAM_RANGES[name]
    if value < lo or value > hi:
        raise ValueError(f"Invalid numeric value for {name}: {value}")


def _resolve_personalization(val: Any) -> bool | list[str]:
    """Convert raw personalization value to the canonical bool | list[str]."""
    if val is None or val == "":
        # ``--p`` flag present with no code → enabled, no custom code
        return True
    if isinstance(val, bool):
        return val
    if isinstance(val, list):
        return val if val else False
    if isinstance(val, str):
        codes = val.split()
        return codes if codes else True
    return bool(val)


class MidjourneyParser:
    """Parser for converting between Midjourney prompt formats."""

    def _parse_url(self, url: str) -> HttpUrl:
        return HttpUrl(url)

    def parse_dict(self, prompt_dict: dict[str, Any]) -> MidjourneyPrompt:  # noqa: C901
        """Parse a dictionary into a MidjourneyPrompt.

        Accepts both short aliases (``"v"``, ``"s"``, ``"ar"``, …) and
        canonical names.  Range validation raises ``ValueError`` with a
        message of the form ``"Invalid numeric value for <param>: <value>"``.

        Args:
            prompt_dict: Dictionary containing prompt data. Not mutated.

        Returns:
            Validated :class:`~midjargon.core.models.MidjourneyPrompt`.

        Raises:
            ValueError: If the prompt text is empty or a parameter value is
                        out of range.
        """
        # Work on a copy so callers' dicts are not mutated.
        d: dict[str, Any] = dict(prompt_dict)

        # ------------------------------------------------------------------
        # Expand aliases
        # ------------------------------------------------------------------
        for alias, canonical in _KEY_ALIASES.items():
            if alias in d and canonical not in d:
                d[canonical] = d.pop(alias)
            elif alias in d:
                d.pop(alias)  # canonical already present; drop alias

        # ------------------------------------------------------------------
        # Text
        # ------------------------------------------------------------------
        text = str(d.pop("text", "") or "").strip()
        if not text:
            raise ValueError("Empty prompt")

        # ------------------------------------------------------------------
        # Image prompts  (accept both "images" and "image_prompts")
        # ------------------------------------------------------------------
        raw_images: list[Any] = d.pop("images", []) or []
        image_prompts: list[ImageReference] = []
        for img in raw_images:
            if isinstance(img, str):
                try:
                    image_prompts.append(ImageReference(url=self._parse_url(img)))
                except Exception:
                    pass  # invalid URL — silently skip
            elif isinstance(img, dict):
                try:
                    if "url" in img and isinstance(img["url"], str):
                        img = dict(img)
                        img["url"] = self._parse_url(img["url"])
                    image_prompts.append(ImageReference(**img))
                except Exception:
                    pass
            elif isinstance(img, ImageReference):
                image_prompts.append(img)

        # ------------------------------------------------------------------
        # Build the params dict for MidjourneyParameters
        # ------------------------------------------------------------------
        params: dict[str, Any] = {}

        # --- aspect ratio -------------------------------------------------
        if "aspect" in d:
            aspect_str = d.pop("aspect")
            if aspect_str:
                try:
                    w_str, h_str = str(aspect_str).split(":")
                    params["aspect_width"] = int(w_str)
                    params["aspect_height"] = int(h_str)
                    params["aspect_ratio"] = f"{int(w_str)}:{int(h_str)}"
                except (ValueError, AttributeError):
                    params["aspect_ratio"] = str(aspect_str)

        # --- version + niji -----------------------------------------------
        if "niji" in d:
            niji_val = d.pop("niji")
            params["version"] = f"niji {niji_val}" if niji_val else "niji"
        elif "version" in d:
            v_raw = d.pop("version")
            if v_raw is not None:
                params["version"] = str(v_raw)

        # --- style --------------------------------------------------------
        if "style" in d:
            params["style"] = d.pop("style")

        # --- numeric parameters -------------------------------------------
        _numeric_fields = {
            "stylize", "chaos", "weird", "image_weight", "quality",
            "character_weight", "style_weight", "style_version", "repeat", "stop",
        }
        for field in _numeric_fields:
            if field not in d:
                continue
            raw = d.pop(field)
            if raw is None:
                params[field] = None
                continue
            try:
                val = _convert_numeric(str(raw))
            except (ValueError, TypeError):
                # non-numeric value — store as extra param
                d[field] = raw
                continue
            _validate_range(field, val)
            params[field] = val

        # --- seed ---------------------------------------------------------
        if "seed" in d:
            params["seed"] = d.pop("seed")

        # --- boolean flags ------------------------------------------------
        for flag in ("tile", "turbo", "relax"):
            if flag in d:
                val = d.pop(flag)
                # None means the flag was present (e.g. ``--tile`` with no value)
                params[flag] = True if val is None else bool(val)

        # --- personalization ----------------------------------------------
        if "personalization" in d:
            params["personalization"] = _resolve_personalization(d.pop("personalization"))

        # --- character_reference ------------------------------------------
        if "character_reference" in d:
            cref_raw = d.pop("character_reference")
            refs = cref_raw if isinstance(cref_raw, list) else [cref_raw]
            params["character_reference"] = [str(r) for r in refs if r is not None]

        # --- style_reference ----------------------------------------------
        if "style_reference" in d:
            sref_raw = d.pop("style_reference")
            refs = sref_raw if isinstance(sref_raw, list) else [sref_raw]
            params["style_reference"] = [str(r) for r in refs if r is not None]

        # --- everything remaining goes to extra_params --------------------
        params["extra_params"] = {k: v for k, v in d.items()
                                  if k not in ("text", "images")}

        mj_params = MidjourneyParameters(**params)

        return MidjourneyPrompt(
            text=text,
            image_prompts=image_prompts,
            parameters=mj_params,
        )


def parse_midjourney_dict(prompt_dict: dict[str, Any]) -> MidjourneyPrompt:
    """Convenience wrapper: convert a dict to a MidjourneyPrompt."""
    return MidjourneyParser().parse_dict(prompt_dict)
