src/midjargon/engines/midjourney/parser.py:206:9: C901 `_handle_version_param` is too complex (11 > 10)
    |
204 |         return str(value) if value is not None else None
205 |
206 |     def _handle_version_param(
    |         ^^^^^^^^^^^^^^^^^^^^^ C901
207 |         self, name: str, raw_value: str | list[str] | None
208 |     ) -> tuple[str | None, Any]:
    |

src/midjargon/engines/midjourney/parser.py:376:9: C901 `_process_numeric_params` is too complex (12 > 10)
    |
374 |                     break  # Stop after finding a --v parameter
375 |
376 |     def _process_numeric_params(
    |         ^^^^^^^^^^^^^^^^^^^^^^^ C901
377 |         self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
378 |     ) -> None:
    |

src/midjargon/engines/midjourney/parser.py:420:25: PLW2901 `for` loop variable `value` overwritten by assignment target
    |
419 |                     if isinstance(value, list):
420 |                         value = value[0] if value else None
    |                         ^^^^^ PLW2901
421 |                         if value is None:
422 |                             continue
    |

src/midjargon/engines/midjourney/parser.py:627:9: C901 `_format_numeric_params` is too complex (12 > 10)
    |
625 |         return prompt
626 |
627 |     def _format_numeric_params(self, prompt: MidjourneyPrompt) -> dict[str, str]:
    |         ^^^^^^^^^^^^^^^^^^^^^^ C901
628 |         """Format numeric parameters for dictionary output."""
629 |         params = {}
    |

src/midjargon/engines/midjourney/parser.py:809:25: B904 Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to distinguish them from errors in exception handling
    |
807 |                     except (ValueError, TypeError):
808 |                         msg = f"Invalid numeric value for {param}: {value}"
809 |                         raise ValueError(msg)
    |                         ^^^^^^^^^^^^^^^^^^^^^ B904
810 |
811 |     def _process_version(
    |

tests/cli/test_main.py:44:9: B904 Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to distinguish them from errors in exception handling
   |
42 |     except json.JSONDecodeError:
43 |         msg = "No JSON found in output"
44 |         raise ValueError(msg)
   |         ^^^^^^^^^^^^^^^^^^^^^ B904
   |

Found 6 errors.