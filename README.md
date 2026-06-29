# Midjargon

**Midjargon** is a Python library and command-line tool for parsing, manipulating, and converting [Midjourney](https://www.midjourney.com)-style prompts.

Midjourney uses a distinctive syntax for its prompts, which we call "midjargon." This includes permutation with `{}` (e.g., `a {red,blue} cat`) and parameters prefixed by `--` (e.g., `--ar 16:9`). While originally Midjourney-specific, this syntax has broader applications—particularly useful for building prompts for other generative AI models.

The `midjargon` package breaks down these prompts into structured components with full type safety and validation. It expands permutations, enforces parameter rules, converts to formats like [Fal.ai](https://fal.ai/), and serializes back to standard Midjourney format.

## Who is Midjargon for?

*   **Midjourney Users:** Those who frequently create or experiment with Midjourney prompts and want better control over variations and structure.
*   **Developers & AI Engineers:** Programmers integrating prompt parsing into Python applications or custom tools.
*   **Content Creators & Prompt Engineers:** People converting prompts between AI image services or systematically exploring large prompt spaces.

## Why use Midjargon?

*   **Accurate Parsing:** Splits complex Midjourney prompts into text, image URLs, parameters, and weights.
*   **Permutation Expansion:** Handles all combinations from `{option1, option2}` syntax, including nested groups and escaped characters.
*   **Parameter Validation:** Enforces Midjourney's parameter rules—numeric ranges, types, boolean flags, multi-value support.
*   **Image URL Support:** Extracts and validates image URLs at the start of prompts.
*   **Weighted Prompts:** Processes multi-part prompts with weighting syntax (e.g., `text1 ::1 text2 ::0.5`).
*   **Type Safety:** Full type hints and Pydantic models ensure clean data handling.
*   **CLI Tool:** Command-line interface for fast parsing, expansion, and conversion with JSON output.
*   **Format Conversion:** Parses Midjourney prompts and converts them to Fal.ai or back to Midjourney format.

## Installation

Install with pip:

```bash
pip install midjargon
```

Or with `uv`:

```bash
uv pip install midjargon
```

## Usage

Midjargon works as both a CLI tool and a Python library.

### Command-Line Interface

Run `midjargon` directly, with `python -m midjargon`, or `uv run midjargon --` if you prefer not to install globally.

**Show available commands:**

```bash
midjargon --help
python -m midjargon --help
```

**Main commands:**

*   **`perm`**: Expand permutations.
    ```bash
    midjargon perm "A {red, blue} cat sitting on a {mat, rug} --mood {happy, sleepy}"
    ```

*   **`json`**: Parse prompt to structured JSON. Expands permutations by default.
    ```bash
    midjargon json "A futuristic cityscape --ar 16:9 --v 6 --style raw"
    ```

*   **`mj`**: Convert to valid Midjourney prompt string(s).
    ```bash
    midjargon mj "A detailed portrait --ar 1:1 --stylize 250"
    ```

*   **`fal`**: Convert to Fal.ai format.
    ```bash
    midjargon fal "photo of a robot --ar 1:1 --seed 123"
    ```

**Command-specific help:**

```bash
midjargon perm --help
midjargon json --help
midjargon mj --help
midjargon fal --help
```

### Python Library

Use `midjargon` programmatically in your projects.

**Key functions from `midjargon.core.converter`:**

*   `permute_prompt(text: str) -> list[str]`: Expands permutations.
*   `parse_prompt(text: str, permute: bool = True) -> MidjargonDict | list[MidjargonDict]`: Parses to generic dictionaries.
*   `to_midjourney_prompts(prompt_input) -> MidjourneyPrompt | list[MidjourneyPrompt]`: Parses and validates into `MidjourneyPrompt` Pydantic models.
*   `to_fal_dicts(prompt_input) -> FalDict | list[FalDict]`: Converts to Fal.ai dictionaries.

**Example: Parsing for Midjourney**

```python
from midjargon.core.converter import to_midjourney_prompts
from midjargon.engines.midjourney.models import MidjourneyPrompt

prompt_string = "A {cyberpunk, steampunk} city --ar 16:9 --chaos {10, 20}"

results = to_midjourney_prompts(prompt_string)

if isinstance(results, list):
    for i, mj_prompt_model in enumerate(results):
        print(f"--- Variant {i+1} ---")
        print(f"Text: {mj_prompt_model.text}")
        print(f"Aspect Ratio: {mj_prompt_model.aspect_ratio}")
        print(f"Chaos: {mj_prompt_model.chaos}")
elif isinstance(results, MidjourneyPrompt):
    print(f"Text: {results.text}")
else:
    print("Unexpected result type")

# For simpler parsing without Midjourney validation:
from midjargon.core.converter import parse_prompt

parsed_dicts = parse_prompt("A simple prompt --param value")
if parsed_dicts:
    print(f"\nGeneric parsed dict example: {parsed_dicts[0]}")
```

For more advanced use cases, explore the modules under `midjargon.core` and `midjargon.engines`.

## Technical Overview

This section explains how `midjargon` works internally and how to contribute.

### Processing Pipeline

1.  **Input Permutation (`midjargon.core.permutations`):**
    *   The raw prompt is first expanded by `expand_permutations`.
    *   Handles `{option1, option2}`, nested groups like `{a, {b, c}}`, and escaped characters (`\,`, `\{`, `\}`).
    *   Output is a list of all possible prompt strings.

2.  **Core Parsing (`midjargon.core.parser`):**
    *   Each expanded string is parsed by `parse_midjargon_prompt_to_dict`.
    *   Extracts leading image URLs.
    *   Separates text from parameter section (starting with `--`).
    *   Parameter parsing via `midjargon.core.parameters`:
        *   Splits on `--`.
        *   Separates names from values.
        *   Handles boolean flags and normalizes aliases.

3.  **Validation & Modeling (`midjargon.engines`):**
    *   Generic `MidjargonDict` is passed to engine-specific parsers.
    *   Each engine defines Pydantic models (e.g., `MidjourneyPrompt`) with type and constraint info.
    *   Engine parser (e.g., `MidjourneyParser`) converts `MidjargonDict` to typed model:
        *   Applies type conversion.
        *   Validates against allowed ranges and enums.
        *   Sets defaults where needed.
    *   Validation logic uses Pydantic's `@field_validator` and `@model_validator`.

4.  **Conversion & Serialization (`midjargon.core.converter`):**
    *   High-level functions orchestrate permutation, parsing, and validation.
    *   `MidjourneyParser.to_prompt_string()` serializes model back to prompt string.
    *   `FalParser` converts `MidjargonDict` to `FalDict` for Fal.ai API.

5.  **CLI (`midjargon.cli.main`):**
    *   Built with `fire` library.
    *   `MidjargonCLI` defines `perm`, `json`, `mj`, `fal` commands.
    *   Calls `midjargon.core.converter` functions and outputs JSON or formatted text.

### Midjourney Syntax

For full details on Midjourney prompt syntax—including parameters, ranges, multi-prompts, and reference types (`--cref`, `--sref`)—see the **[Midjourney Prompt Format Specification](docs/specification.md)**.

### Project Structure

```
.
├── LICENSE
├── README.md
├── docs
│   ├── specification.md
│   └── ...
├── pyproject.toml
├── src
│   └── midjargon
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli
│       │   └── main.py
│       ├── core
│       │   ├── converter.py
│       │   ├── input.py
│       │   ├── models.py
│       │   ├── parameters.py
│       │   ├── parser.py
│       │   ├── permutations.py
│       │   └── type_defs.py
│       └── engines
│           ├── base.py
│           ├── fal
│           └── midjourney
│               ├── constants.py
│               ├── models.py
│               └── parser.py
└── tests
```

### Contribution Guidelines

Contributions welcome. Follow these steps:

*   **Setup:**
    1.  Clone the repo:
        ```bash
        git clone https://github.com/twardoch/midjargon.git
        cd midjargon
        ```
    2.  Use a virtual environment. With `uv`:
        ```bash
        uv venv
        uv pip install -e ".[all]"
        ```
        Or standard tools:
        ```bash
        python -m venv .venv
        source .venv/bin/activate
        pip install -e ".[all]"
        ```
    3.  Install `hatch` for task management:
        ```bash
        pip install hatch
        ```

*   **Run Tests:**
    ```bash
    hatch test
    ```

*   **Format & Lint:**
    ```bash
    hatch run lint:all
    # Or:
    hatch run lint:fmt
    hatch run lint:style
    ```

*   **Type Check:**
    ```bash
    hatch run lint:typing
    ```

*   **Commit Messages:**
    Use conventional commits: `feat:`, `fix:`, etc.

*   **Pull Requests:**
    *   Submit to main development branch.
    *   Include:
        *   Description of changes.
        *   Passing tests.
        *   Lint and type checks.
        *   Updated docs if needed.

*   **Code Style:**
    *   Follow PEP 8 (enforced by Ruff).
    *   Prefer clarity.
    *   Use type hints.
    *   Leverage Pydantic for data validation.

### License

MIT. See [LICENSE](LICENSE).