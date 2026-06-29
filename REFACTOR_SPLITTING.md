## Refactoring Large Code Files in `midjargon`

**Goal:** Split large Python files into smaller, focused modules to improve organization, readability, and maintainability. Prioritize minimal functional changes and clear separation of concerns.

**General Principles:**

1.  **No Functional Changes:** Refactor for structure only. No new features or behavior modifications.
2.  **Maintain Imports:** Update all imports to reflect new file locations.
3.  **Preserve Public API:** Functions and classes exposed in `__init__.py` or used externally must remain accessible at their original paths (e.g., `from midjargon.core.models import MidjourneyPrompt`). Update `__init__.py` files accordingly.
4.  **Run Tests Frequently:** After each logical step, run `hatch test` to catch breakage immediately.
5.  **Clear Naming:** New files and directories should have descriptive names indicating their purpose.

---

### Phase 1: Refactoring `src/midjargon/core/models.py`

**Current Size:** 14 KB  
**Reason for Splitting:** Contains multiple Pydantic models and validators, making navigation difficult.

**Steps:**

1.  **Create New Directory:**
    *   Create: `/src/midjargon/core/models/`

2.  **Create `src/midjargon/core/models/base.py`:**
    *   Move `MidjourneyVersion` and `StyleMode` enums here.
    *   **Content:**
        ```python
        from enum import Enum
        from typing import Any
        from pydantic import BaseModel, field_validator

        class MidjourneyVersion(str, Enum):
            # ... full content ...

        class StyleMode(str, Enum):
            # ... full content ...
        ```
    *   Run `hatch test`.

3.  **Create `src/midjargon/core/models/references.py`:**
    *   Move `ImageReference`, `CharacterReference`, and `StyleReference` here.
    *   **Content:**
        ```python
        from typing import Any
        from pydantic import BaseModel, Field, HttpUrl, model_validator
        # from .base import MidjourneyVersion, StyleMode # if needed

        class ImageReference(BaseModel):
            # ... full content ...

        class CharacterReference(BaseModel):
            # ... full content ...

        class StyleReference(BaseModel):
            # ... full content ...
        ```
    *   Import required Pydantic components. If enums are used, import from `.base`.
    *   Run `hatch test`.

4.  **Create `src/midjargon/core/models/parameters.py`:**
    *   Move `MidjourneyParameters` here.
    *   **Content:**
        ```python
        from typing import Any, Union
        from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator
        from .base import MidjourneyVersion, StyleMode
        from .references import CharacterReference, StyleReference

        class MidjourneyParameters(BaseModel):
            # ... full content ...
        ```
    *   Import all necessary Pydantic components and models from `.base` and `.references`.
    *   Run `hatch test`.

5.  **Update `src/midjargon/core/models.py`:**
    *   Keep only `MidjourneyPrompt` and `PromptVariant`. Import other models from new submodules.
    *   **Content:**
        ```python
        from __future__ import annotations
        from typing import Any, TypeVar
        from pydantic import BaseModel
        from .models.base import MidjourneyVersion, StyleMode
        from .models.references import ImageReference, CharacterReference, StyleReference
        from .models.parameters import MidjourneyParameters

        T = TypeVar("T", bound="BaseModel")

        class MidjourneyPrompt(BaseModel):
            # ... full content ...

        class PromptVariant(BaseModel):
            # ... full content ...
        ```
    *   Update internal imports to point to new locations.
    *   Run `hatch test`.

6.  **Update `src/midjargon/core/__init__.py`:**
    *   Expose moved models from new locations to maintain public API.
    *   **Content:**
        ```python
        # ... existing imports ...
        from midjargon.core.models.base import MidjourneyVersion, StyleMode
        from midjargon.core.models.references import ImageReference, CharacterReference, StyleReference
        from midjargon.core.models.parameters import MidjourneyParameters
        from midjargon.core.models import MidjourneyPrompt, PromptVariant

        __all__ = [
            # ... existing exports ...
            "MidjourneyVersion",
            "StyleMode",
            "ImageReference",
            "CharacterReference",
            "StyleReference",
            "MidjourneyParameters",
            "MidjourneyPrompt",
            "PromptVariant",
        ]
        ```
    *   Run `hatch test`.

---

### Phase 2: Refactoring `src/midjargon/core/parameters.py`

**Current Size:** 13 KB  
**Reason for Splitting:** Mixes constants, validation functions, type conversion logic, and parsing logic.

**Steps:**

1.  **Create New Directory:**
    *   Create: `/src/midjargon/core/parameters/`

2.  **Create `src/midjargon/core/parameters/constants.py`:**
    *   Move `ALIASES`, `STRING_PARAMS`, `INT_PARAMS`, `SPECIAL_SEED_VALUES`, `NIJI_PREFIX_LENGTH`, `PARAMETER_ALIASES` here.
    *   **Content:**
        ```python
        # ... all constant definitions ...
        ```
    *   Run `hatch test`.

3.  **Create `src/midjargon/core/parameters/validation.py`:**
    *   Move `validate_param_name` and `validate_param_value` here.
    *   **Content:**
        ```python
        from typing import Any
        # from midjargon.core.models.base import MidjourneyVersion, StyleMode # if needed
        # from midjargon.core.models.references import CharacterReference, StyleReference # if needed

        class ParameterValidationError(Exception):
            # ... full content ...

        def validate_param_name(name: str) -> None:
            # ... full content ...

        def validate_param_value(name: str, value: Any) -> None:
            # ... full content ...
        ```
    *   Import `ParameterValidationError` and any needed models from new locations.
    *   Run `hatch test`.

4.  **Create `src/midjargon/core/parameters/conversion.py`:**
    *   Move `convert_parameter_value` here.
    *   **Content:**
        ```python
        from typing import Any
        from urllib.parse import urlparse
        from .constants import FLAG_PARAMS, INT_PARAMS, STRING_PARAMS, SPECIAL_SEED_VALUES
        from midjargon.core.models.base import MidjourneyVersion, StyleMode
        from midjargon.core.models.references import CharacterReference, StyleReference
        from pydantic import HttpUrl

        def is_url(text: str) -> bool:
            try:
                result = urlparse(text)
                return all([result.scheme, result.netloc])
            except Exception:
                return False

        def convert_parameter_value(param: str, value: Any) -> Any:
            # ... full content ...
        ```
    *   Import constants from `.constants` and models from `midjargon.core.models`.
    *   Run `hatch test`.

5.  **Update `src/midjargon/core/parameters.py`:**
    *   Keep only core parsing logic (`parse_parameters`, `_process_param_chunk`, `_process_current_param`).
    *   **Content:**
        ```python
        from __future__ import annotations
        from typing import Any, Union
        from .parameters.constants import ALIASES, PARAMETER_ALIASES, FLAG_PARAMS, MULTI_VALUE_PARAMS
        from .parameters.validation import validate_param_name, validate_param_value
        from .parameters.conversion import convert_parameter_value

        def _split_param_chunks(param_str: str) -> list[str]:
            # ... full content ...

        def _process_param_chunk(chunk: str, params: dict[str, str | list[str] | None]) -> tuple[str, str | list[str] | None]:
            # ... full content ...

        def _process_current_param(current_param: str | None, current_values: list[str], params: dict[str, str | list[str] | None]) -> None:
            # ... full content ...

        def parse_parameters(param_str: str) -> dict[str, str | list[str] | None]:
            # ... full content ...
        ```
    *   Import from new submodules.
    *   Run `hatch test`.

6.  **Update `src/midjargon/core/__init__.py`:**
    *   Expose moved functions from new locations.
    *   **Content:**
        ```python
        # ... existing imports ...
        from midjargon.core.parameters.constants import ALIASES, PARAMETER_ALIASES
        from midjargon.core.parameters.validation import validate_param_name, validate_param_value
        from midjargon.core.parameters.conversion import convert_parameter_value
        from midjargon.core.parameters import parse_parameters

        __all__ = [
            # ... existing exports ...
            "parse_parameters",
            # Add other exposed functions/constants if necessary
        ]
        ```
    *   Run `hatch test`.

---

### Phase 3: Refactoring `src/midjargon/core/permutations.py`

**Current Size:** 10 KB  
**Reason for Splitting:** Many helper functions obscure core permutation logic.

**Steps:**

1.  **Create New Directory:**
    *   Create: `/src/midjargon/core/permutations/`

2.  **Create `src/midjargon/core/permutations/helpers.py`:**
    *   Move `_find_matching_brace`, `_extract_options`, `_format_part`, `_add_spacing`, `_handle_escaped_char`, `_handle_literal_char` here.
    *   **Content:**
        ```python
        from typing import TYPE_CHECKING, Any

        def _find_matching_brace(text: str, start: int) -> int:
            # ... full content ...

        def _extract_options(text: str, start: int, end: int) -> list[str]:
            # ... full content ...

        def _format_part(before: str, option: str, after: str) -> str:
            # ... full content ...

        def _add_spacing(before: str, after: str) -> tuple[str, str]:
            # ... full content ...

        def _handle_escaped_char(text: str, pos: int, result: list[str]) -> int:
            # ... full content ...

        def _handle_literal_char(text: str, pos: int, result: list[str]) -> None:
            # ... full content ...
        ```
    *   Run `hatch test`.

3.  **Create `src/midjargon/core/permutations/options.py`:**
    *   Move `split_options` and `split_permutation_options` here.
    *   **Content:**
        ```python
        from typing import TYPE_CHECKING

        def split_options(text: str) -> list[str]:
            # ... full content ...

        def split_permutation_options(text: str) -> list[str]:
            # ... full content ...
        ```
    *   Run `hatch test`.

4.  **Update `src/midjargon/core/permutations.py`:**
    *   Keep core permutation logic (`_expand_nested`, `expand_single`, `expand_text`, `_handle_permutation`, `expand_permutations`).
    *   **Content:**
        ```python
        from __future__ import annotations
        from typing import TYPE_CHECKING, Sequence, Tuple, List
        from .permutations.helpers import _find_matching_brace, _format_part, _handle_escaped_char, _handle_literal_char, _extract_options
        from .permutations.options import split_options, split_permutation_options

        def _expand_nested(options: Sequence[str]) -> list[str]:
            # ... full content ...

        def expand_single(text: str) -> list[str]:
            # ... full content ...

        def expand_text(text: str) -> list[str]:
            # ... full content ...

        def _handle_permutation(text: str, pos: int, result: list[str]) -> Tuple[list[str], int]:
            # ... full content ...

        def expand_permutations(text: str) -> list[str]:
            # ... full content ...
        ```
    *   Import from new submodules.
    *   Run `hatch test`.

5.  **Update `src/midjargon/core/__init__.py`:**
    *   Expose moved functions from new locations.
    *   **Content:**
        ```python
        # ... existing imports ...
        from midjargon.core.permutations.helpers import _find_matching_brace
        from midjargon.core.permutations.options import split_options, split_permutation_options
        from midjargon.core.permutations import expand_text, expand_permutations

        __all__ = [
            # ... existing exports ...
            "expand_text",
            "expand_permutations",
        ]
        ```
    *   Run `hatch test`.

---

### Final Verification (After all phases):

1.  **Run All Tests:** Execute `hatch test`.
2.  **Linting and Formatting:** Run `hatch run lint:all`.
3.  **Type Checking:** Run `hatch run lint:typing`.
4.  **Manual Inspection:** Review refactored files for logical separation and readability.

This plan provides a structured approach to refactoring, minimizing risk and ensuring functionality remains intact.