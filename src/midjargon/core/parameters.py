#!/usr/bin/env python3
# this_file: src/midjargon/core/parameters.py
"""
Parse Midjourney prompt parameters from a raw ``--key value`` string into a dict.

All values are returned as strings (or None for flags, list[str] for multi-value
params). Numeric conversion is the responsibility of higher-level callers.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Public type aliases
# ---------------------------------------------------------------------------
ParamName = str
ParamValue = str | list[str] | None
ParamDict = dict[ParamName, ParamValue]

# ---------------------------------------------------------------------------
# Alias table: short name → canonical name
# ---------------------------------------------------------------------------
PARAMETER_ALIASES: dict[str, str] = {
    "s": "stylize",
    "c": "chaos",
    "w": "weird",
    "iw": "image_weight",
    "ar": "aspect",
    "p": "personalization",
    "v": "version",
    "q": "quality",
    "cw": "character_weight",
    "sw": "style_weight",
    "sv": "style_version",
    "r": "repeat",
    "cref": "character_reference",
    "sref": "style_reference",
}

# Parameters that take NO value (presence means True/None)
FLAG_PARAMS: frozenset[str] = frozenset({"tile", "turbo", "relax", "video", "remix"})

# Parameters that consume ALL remaining tokens until the next ``--``
MULTI_VALUE_PARAMS: frozenset[str] = frozenset(
    {"personalization", "character_reference", "style_reference"}
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _tokenize(param_str: str) -> list[str]:
    """Split *param_str* into tokens, honouring single- and double-quoted spans."""
    tokens: list[str] = []
    current: list[str] = []
    in_quotes = False
    quote_char = ""

    for char in param_str:
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
        elif in_quotes and char == quote_char:
            in_quotes = False
            quote_char = ""
        elif char.isspace() and not in_quotes:
            if current:
                tokens.append("".join(current))
                current = []
        else:
            current.append(char)

    if current:
        tokens.append("".join(current))

    return tokens


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_parameters(param_str: str) -> ParamDict:
    """Parse a ``--key [value …]`` parameter string into a dict.

    Args:
        param_str: Raw parameter string, e.g. ``"--ar 16:9 --stylize 100"``.

    Returns:
        Ordered dict mapping canonical parameter names to their values.
        Flag parameters map to ``None``; multi-value parameters map to a
        ``list[str]``; all others map to a single ``str``.

    Raises:
        ValueError: On syntax errors (missing ``--``, empty name, missing value).
    """
    if not param_str:
        return {}

    stripped = param_str.strip()
    if not stripped:
        return {}

    # Top-level string must begin with ``--``
    if not stripped.startswith("--"):
        raise ValueError(f"Parameter name cannot start with dash: {stripped}")

    tokens = _tokenize(stripped)
    params: ParamDict = {}
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if not token.startswith("--"):
            raise ValueError(f"Parameter name cannot start with dash: {token}")

        name = token[2:]  # strip the leading ``--``
        if not name:
            raise ValueError("Empty parameter name")

        # ---- special: --niji [N] ----------------------------------------
        if name == "niji":
            i += 1
            if i < len(tokens) and not tokens[i].startswith("--"):
                params["version"] = f"niji {tokens[i]}"
                i += 1
            else:
                params["version"] = "niji"
            continue

        expanded = PARAMETER_ALIASES.get(name, name)

        # ---- flag parameters (no value) ------------------------------------
        if expanded in FLAG_PARAMS:
            params[expanded] = None
            i += 1
            continue

        # ---- personalization: optional multi-value -------------------------
        if expanded == "personalization":
            i += 1
            values: list[str] = []
            while i < len(tokens) and not tokens[i].startswith("--"):
                # A quoted token like "CODE1 CODE2" arrives as one token;
                # split it so each code is a separate list element.
                values.extend(tokens[i].split())
                i += 1
            params["personalization"] = values if values else None
            continue

        # ---- character_reference / style_reference: multi-value -----------
        if expanded in {"character_reference", "style_reference"}:
            i += 1
            refs: list[str] = []
            while i < len(tokens) and not tokens[i].startswith("--"):
                refs.append(tokens[i])
                i += 1
            params[expanded] = refs
            continue

        # ---- regular single-value parameter --------------------------------
        i += 1
        if i >= len(tokens) or tokens[i].startswith("--"):
            raise ValueError(f"Missing value for parameter: {name}")

        params[expanded] = tokens[i]
        i += 1

    return params
