src/midjargon/core/input.py:58:13: PLW2901 `for` loop variable `text` overwritten by assignment target
   |
56 |             "‹ESCAPED_COMMA›": ",",
57 |         }.items():
58 |             text = text.replace(marker, original)
   |             ^^^^ PLW2901
59 |         restored.append(text)
   |

src/midjargon/core/parameters.py:210:5: C901 `_process_param_chunk` is too complex (13 > 10)
    |
210 | def _process_param_chunk(
    |     ^^^^^^^^^^^^^^^^^^^^ C901
211 |     chunk: str, params: dict[str, str | None]
212 | ) -> tuple[str, str | None]:
    |

src/midjargon/core/parameters.py:210:5: PLR0911 Too many return statements (7 > 6)
    |
210 | def _process_param_chunk(
    |     ^^^^^^^^^^^^^^^^^^^^ PLR0911
211 |     chunk: str, params: dict[str, str | None]
212 | ) -> tuple[str, str | None]:
    |

src/midjargon/core/parameters.py:274:5: C901 `parse_parameters` is too complex (20 > 10)
    |
274 | def parse_parameters(param_str: str) -> ParamDict:
    |     ^^^^^^^^^^^^^^^^ C901
275 |     """
276 |     Parse a parameter string into a dictionary.
    |

src/midjargon/core/parameters.py:274:5: PLR0912 Too many branches (23 > 12)
    |
274 | def parse_parameters(param_str: str) -> ParamDict:
    |     ^^^^^^^^^^^^^^^^ PLR0912
275 |     """
276 |     Parse a parameter string into a dictionary.
    |

src/midjargon/core/parameters.py:274:5: PLR0915 Too many statements (63 > 50)
    |
274 | def parse_parameters(param_str: str) -> ParamDict:
    |     ^^^^^^^^^^^^^^^^ PLR0915
275 |     """
276 |     Parse a parameter string into a dictionary.
    |

src/midjargon/core/permutations.py:304:5: C901 `expand_permutations` is too complex (11 > 10)
    |
304 | def expand_permutations(text: str) -> list[str]:
    |     ^^^^^^^^^^^^^^^^^^^ C901
305 |     """
306 |     Expand all permutations in a text string.
    |

src/midjargon/engines/midjourney/parser.py:63:9: C901 `_handle_numeric_param` is too complex (16 > 10)
   |
61 |                 raise ValueError(msg)
62 |
63 |     def _handle_numeric_param(
   |         ^^^^^^^^^^^^^^^^^^^^^ C901
64 |         self, name: str, raw_value: str | list[str] | None
65 |     ) -> tuple[str | None, Any]:
   |

src/midjargon/engines/midjourney/parser.py:63:9: PLR0911 Too many return statements (14 > 6)
   |
61 |                 raise ValueError(msg)
62 |
63 |     def _handle_numeric_param(
   |         ^^^^^^^^^^^^^^^^^^^^^ PLR0911
64 |         self, name: str, raw_value: str | list[str] | None
65 |     ) -> tuple[str | None, Any]:
   |

src/midjargon/engines/midjourney/parser.py:63:9: PLR0912 Too many branches (15 > 12)
   |
61 |                 raise ValueError(msg)
62 |
63 |     def _handle_numeric_param(
   |         ^^^^^^^^^^^^^^^^^^^^^ PLR0912
64 |         self, name: str, raw_value: str | list[str] | None
65 |     ) -> tuple[str | None, Any]:
   |

src/midjargon/engines/midjourney/parser.py:186:9: C901 `_handle_version_param` is too complex (11 > 10)
    |
184 |         return "style", new_value
185 |
186 |     def _handle_version_param(
    |         ^^^^^^^^^^^^^^^^^^^^^ C901
187 |         self, name: str, raw_value: str | list[str] | None
188 |     ) -> tuple[str | None, Any]:
    |

src/midjargon/engines/midjourney/parser.py:298:9: C901 `_parse_dict` is too complex (27 > 10)
    |
296 |         return None, None
297 |
298 |     def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
    |         ^^^^^^^^^^^ C901
299 |         """Parse a dictionary into a MidjourneyPrompt."""
300 |         prompt_data: dict[str, Any] = {
    |

src/midjargon/engines/midjourney/parser.py:298:9: PLR0912 Too many branches (30 > 12)
    |
296 |         return None, None
297 |
298 |     def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
    |         ^^^^^^^^^^^ PLR0912
299 |         """Parse a dictionary into a MidjourneyPrompt."""
300 |         prompt_data: dict[str, Any] = {
    |

src/midjargon/engines/midjourney/parser.py:298:9: PLR0915 Too many statements (79 > 50)
    |
296 |         return None, None
297 |
298 |     def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
    |         ^^^^^^^^^^^ PLR0915
299 |         """Parse a dictionary into a MidjourneyPrompt."""
300 |         prompt_data: dict[str, Any] = {
    |

src/midjargon/engines/midjourney/parser.py:489:9: C901 `_format_numeric_params` is too complex (12 > 10)
    |
487 |         return prompt
488 |
489 |     def _format_numeric_params(self, prompt: MidjourneyPrompt) -> dict[str, str]:
    |         ^^^^^^^^^^^^^^^^^^^^^^ C901
490 |         """Format numeric parameters for dictionary output."""
491 |         params = {}
    |

src/midjargon/engines/midjourney/parser.py:611:9: C901 `parse_midjourney_dict` is too complex (21 > 10)
    |
609 |         return result
610 |
611 |     def parse_midjourney_dict(self, data: MidjargonDict) -> MidjourneyPrompt:
    |         ^^^^^^^^^^^^^^^^^^^^^ C901
612 |         """
613 |         Parse a dictionary into a MidjourneyPrompt object.
    |

src/midjargon/engines/midjourney/parser.py:611:9: PLR0912 Too many branches (22 > 12)
    |
609 |         return result
610 |
611 |     def parse_midjourney_dict(self, data: MidjargonDict) -> MidjourneyPrompt:
    |         ^^^^^^^^^^^^^^^^^^^^^ PLR0912
612 |         """
613 |         Parse a dictionary into a MidjourneyPrompt object.
    |

src/midjargon/engines/midjourney/parser.py:611:9: PLR0915 Too many statements (60 > 50)
    |
609 |         return result
610 |
611 |     def parse_midjourney_dict(self, data: MidjargonDict) -> MidjourneyPrompt:
    |         ^^^^^^^^^^^^^^^^^^^^^ PLR0915
612 |         """
613 |         Parse a dictionary into a MidjourneyPrompt object.
    |

tests/cli/test_main.py:44:9: B904 Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to distinguish them from errors in exception handling
   |
42 |     except json.JSONDecodeError:
43 |         msg = "No JSON found in output"
44 |         raise ValueError(msg)
   |         ^^^^^^^^^^^^^^^^^^^^^ B904
   |

Found 19 errors.