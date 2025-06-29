# Midjargon

**Midjargon** is a powerful Python library and command-line interface (CLI) tool meticulously designed to parse, manipulate, and convert [Midjourney](https://www.midjourney.com)-style prompts.

Midjourney utilizes a unique and expressive syntax for its prompts, which we refer to as "midjargon." This syntax includes features like permutation using `{}` (e.g., `a {red,blue} cat`) and parameter specification with an `--` prefix (e.g., `--ar 16:9`). While native to Midjourney, this versatile syntax is also beneficial for other applications, such as constructing prompts for different generative AI models.

The `midjargon` package robustly deconstructs these prompts into manageable, structured components, ensuring type-safe operations and comprehensive validation. It excels at expanding permutations, handling complex parameter rules, and converting midjargon prompts into other formats, such as those used by [Fal.ai](https://fal.ai/), as well as serializing them back into the standard Midjourney format.

## Who is Midjargon for?

*   **Midjourney Users:** Anyone who frequently crafts and experiments with Midjourney prompts and wants a better way to manage, generate variations, or understand their structure.
*   **Developers & AI Engineers:** Programmers looking to integrate Midjourney prompt parsing and manipulation into their Python applications, workflows, or custom tools.
*   **Content Creators & Prompt Engineers:** Individuals who need to convert prompts between different AI image generation services or require a systematic way to explore vast prompt spaces.

## Why use Midjargon?

*   **Robust Parsing:** Accurately deconstructs complex Midjourney prompts into their fundamental components: text, image URLs, parameters, and weights.
*   **Advanced Permutation Engine:** Automatically expands all possible prompt combinations from permutation syntax (`{option1, option2}`), including support for nested permutations and escaped characters.
*   **Comprehensive Parameter Handling:** Validates parameter names and their values according to Midjourney rules, supporting numeric ranges, type conversions, boolean flags, and multi-value parameters.
*   **Image URL Processing:** Extracts and validates image URLs, supporting multiple image inputs and common file extensions.
*   **Multi-Prompt & Weighting Support:** Correctly interprets and processes prompts with multiple weighted segments (e.g., `text1 ::1 text2 ::0.5`).
*   **Type Safety:** Built with full type hints and Pydantic models for robust data validation and improved developer experience.
*   **Versatile CLI Tool:** Offers a user-friendly command-line interface for quick parsing, permutation, and conversion tasks, with JSON output for easy automation.
*   **Format Conversion:** Supports conversion of Midjourney prompts to other formats like Fal.ai and can serialize processed prompts back to the Midjourney format.

## Installation

You can install Midjargon using pip:

```bash
pip install midjargon
```
Or, if you use `uv`:
```bash
uv pip install midjargon
```

## How to Use Midjargon

Midjargon can be used both as a command-line tool and as a Python library.

### Command-Line Interface (CLI) Usage

The `midjargon` CLI provides several commands to work with your prompts. You can run it directly, via `python -m midjargon`, or even with `uv run midjargon --` followed by the command arguments if you prefer not to install it globally.

**Basic Invocation:**

```bash
midjargon --help  # Shows all available commands
python -m midjargon --help
```

**Main Commands:**

*   **`perm`**: Expands all permutations in a prompt.
    ```bash
    midjargon perm "A {red, blue} cat sitting on a {mat, rug} --mood {happy, sleepy}"
    ```

*   **`json`**: Parses a prompt and outputs its structured representation in JSON format. This is useful for understanding the prompt's components or for programmatic use. By default, it permutes the prompt first.
    ```bash
    midjargon json "A futuristic cityscape --ar 16:9 --v 6 --style raw"
    ```

*   **`mj`**: Converts a prompt (potentially with non-standard syntax or after manipulation) back into one or more valid Midjourney prompt strings.
    ```bash
    midjargon mj "A detailed portrait --ar 1:1 --stylize 250"
    ```

*   **`fal`**: Converts a Midjourney prompt into the format expected by Fal.ai.
    ```bash
    midjargon fal "photo of a robot --ar 1:1 --seed 123"
    ```

**Getting Help for Specific Commands:**

For detailed options for each command, use `--help`:

```bash
midjargon perm --help
midjargon json --help
midjargon mj --help
midjargon fal --help
```

### Programmatic Usage (Python Library)

Integrate `midjargon` into your Python projects to leverage its parsing and manipulation capabilities.

**Key Functions from `midjargon.core.converter`:**

*   `permute_prompt(text: str) -> list[str]`: Expands permutations.
*   `parse_prompt(text: str, permute: bool = True) -> MidjargonDict | list[MidjargonDict]`: Parses to generic dictionaries.
*   `to_midjourney_prompts(prompt_input) -> MidjourneyPrompt | list[MidjourneyPrompt]`: Parses and validates into `MidjourneyPrompt` Pydantic models.
*   `to_fal_dicts(prompt_input) -> FalDict | list[FalDict]`: Converts to Fal.ai dictionaries.

**Basic Example (Parsing and Validating for Midjourney):**

```python
from midjargon.core.converter import to_midjourney_prompts
from midjargon.engines.midjourney.models import MidjourneyPrompt # Pydantic model
# Assuming MidjourneyParser might be needed for string reconstruction
# from midjargon.engines.midjourney.parser import MidjourneyParser


prompt_string = "A {cyberpunk, steampunk} city --ar 16:9 --chaos {10, 20}"

# to_midjourney_prompts handles permutation and parsing
results = to_midjourney_prompts(prompt_string)

# Results will be a list if there were permutations
if isinstance(results, list):
    for i, mj_prompt_model in enumerate(results):
        print(f"--- Variant {i+1} ---")
        # mj_prompt_model is a MidjourneyPrompt Pydantic object
        print(f"Text: {mj_prompt_model.text}")
        print(f"Aspect Ratio: {mj_prompt_model.aspect_ratio}")
        print(f"Chaos: {mj_prompt_model.chaos}")
        # print(f"Full Model: {mj_prompt_model.model_dump_json(indent=2)}")

        # To convert back to a string, you'd typically use the parser:
        # Example: reconstructed_string = MidjourneyParser().to_prompt_string(mj_prompt_model)
        # print(f"Reconstructed String: {reconstructed_string}")
elif isinstance(results, MidjourneyPrompt):
    # Single result (no permutations or input was already specific)
    print(f"Text: {results.text}")
    # ... and so on
    # Example: reconstructed_string = MidjourneyParser().to_prompt_string(results)
    # print(f"Reconstructed String: {reconstructed_string}")
else:
    print("Unexpected result type")


# For simpler parsing to a generic dictionary without Midjourney-specific validation:
from midjargon.core.converter import parse_prompt
# parse_prompt by default permutes and returns a list of dicts
parsed_dicts = parse_prompt("A simple prompt --param value")

if parsed_dicts: # It will be a list
    print(f"\nGeneric parsed dict example: {parsed_dicts[0]}")

```
*Self-correction: The `MidjourneyPrompt` model itself doesn't have a `to_prompt_string()` method directly. This functionality is part of the `MidjourneyParser`. The example above has been commented to reflect this.*

This provides a glimpse into `midjargon`'s capabilities. For more advanced scenarios, explore the functions and classes within the `midjargon.core` and `midjargon.engines` modules.

## Technical Deep Dive

This section provides a more detailed look into how `midjargon` works internally and outlines guidelines for contributing to the project.

### How Midjargon Works

The `midjargon` library processes prompts in several stages:

1.  **Input Permutation (`midjargon.core.input`, `midjargon.core.permutations`):**
    *   The initial raw prompt string is first processed by the permutation engine (`expand_permutations` in `midjargon.core.permutations`).
    *   This engine identifies permutation groups denoted by curly braces `{option1, option2, ...}`.
    *   It supports nested permutations (e.g., `{a, {b, c}}`) and escaped characters (`\,`, `\{`, `\}`) to allow literal commas and braces within permutations.
    *   The `permute_prompt` function in `midjargon.core.converter` (which uses `expand_midjargon_input` from `midjargon.core.input`) generates a list of all possible prompt strings.

2.  **Core Parsing (`midjargon.core.parser`):**
    *   Each expanded prompt string is then passed to the core parser (`parse_midjargon_prompt_to_dict` in `midjargon.core.parser`).
    *   This parser's primary role is to dissect the string into a structured `MidjargonDict` (a Python dictionary).
    *   **Image URL Extraction:** It first identifies and extracts any image URLs at the beginning of the prompt.
    *   **Text and Parameter Separation:** The remaining string is split into the main textual part of the prompt and the parameter part (which starts with `--`).
    *   **Parameter Parsing (`midjargon.core.parameters`):** The `parse_parameters` function from `midjargon.core.parameters` breaks down the parameter string.
        *   It splits parameters based on the `--` prefix.
        *   It distinguishes parameter names from their values.
        *   It handles boolean flags and normalizes parameter names using aliases.

3.  **Type-Safe Modeling and Engine-Specific Validation (`midjargon.engines`):**
    *   The `MidjargonDict` is a generic representation. For engine-specific interpretation (like Midjourney), this dictionary is processed by an engine parser.
    *   **Pydantic Models:** Each engine (e.g., `midjargon.engines.midjourney`) has its own Pydantic models (e.g., `MidjourneyPrompt` in `midjargon.engines.midjourney.models`). These define structure, data types, and validation rules.
    *   **Engine Parser (`midjargon.engines.base.EngineParser`):**
        *   The `MidjourneyParser` (from `midjargon.engines.midjourney.parser`) takes the `MidjargonDict`.
        *   Its `parse_from_dict` method converts raw values into the strongly-typed fields of its Pydantic model (`MidjourneyPrompt`), involving type conversion, validation against constraints (numeric ranges, enums), and applying defaults.
        *   The `MidjourneyPrompt` model itself (in `midjargon.engines.midjourney.models.py`) uses Pydantic's `@field_validator` and `@model_validator` for these rules, referencing constants from `midjargon.engines.midjourney.constants.py`.

4.  **Conversion and Serialization (`midjargon.core.converter`, `midjargon.engines`):**
    *   The `midjargon.core.converter` module provides high-level functions like `to_midjourney_prompts` and `to_fal_dicts`.
    *   These functions orchestrate permutation, parsing, and engine-specific validation.
    *   **To Midjourney String:** The validated `MidjourneyPrompt` model can be serialized back into a compliant Midjourney prompt string by the `MidjourneyParser`'s `to_prompt_string(model)` method.
    *   **To Fal.ai Dictionary:** The `FalParser` in `midjargon.engines.fal.converter` converts a `MidjargonDict` into a `FalDict` suitable for the Fal.ai API.

5.  **Command-Line Interface (`midjargon.cli.main`):**
    *   The CLI is built using the `fire` library.
    *   The `MidjargonCLI` class in `src/midjargon/cli/main.py` defines commands (`perm`, `json`, `mj`, `fal`).
    *   These CLI commands call the respective functions from `midjargon.core.converter` to perform operations and format the output (Rich console output or JSON).

### Midjourney Prompt Syntax Reference

For a comprehensive understanding of the Midjourney prompt syntax that `midjargon` is designed to parse, including all parameters, their value types, ranges, and advanced features like multi-prompts, permutation syntax, and various reference types (`--cref`, `--sref`), please consult the **[Midjourney Prompt Format Specification](docs/specification.md)**.

### Project Structure

```
.
├── LICENSE                    # MIT license
├── README.md                  # Project introduction and documentation
├── docs                       # Project documentation
│   ├── specification.md        # Detailed midjargon prompt syntax specification
│   └── ...                    # Other docs
├── pyproject.toml             # Python project configuration (PEP 518, PEP 621)
├── src                        # Source code
│   └── midjargon
│       ├── __init__.py
│       ├── __main__.py        # Main CLI entry point
│       ├── cli                # Command-Line Interface logic
│       │   └── main.py        # CLI command definitions using Fire
│       ├── core               # Core parsing, permutation, and conversion logic
│       │   ├── converter.py     # High-level functions for prompt conversion
│       │   ├── input.py         # Input processing, permutation expansion entry
│       │   ├── models.py        # Core Pydantic models (e.g., PromptVariant)
│       │   ├── parameters.py    # Parsing and validation of parameters
│       │   ├── parser.py        # Basic prompt string parsing into MidjargonDict
│       │   ├── permutations.py  # Permutation expansion logic
│       │   └── type_defs.py     # Core type definitions (MidjargonInput, MidjargonDict)
│       └── engines            # Engine-specific parsers and models
│           ├── base.py          # Abstract base class for engine parsers
│           ├── fal              # Fal.ai engine implementation
│           └── midjourney       # Midjourney engine implementation
│               ├── constants.py   # Parameter constraints, defaults for Midjourney
│               ├── models.py      # Pydantic models for validated Midjourney prompts
│               └── parser.py      # Midjourney-specific parsing logic (MidjourneyParser)
└── tests                      # Test suite for midjargon
    # ... (test structure mirrors src structure)
```
*(Other files like `package.toml`, `TODO.md` exist but are omitted for brevity in this view).*

### Coding and Contribution Guidelines

We welcome contributions to `midjargon`! Please follow these guidelines:

*   **Development Setup:**
    1.  Clone the repository:
        ```bash
        git clone https://github.com/twardoch/midjargon.git
        cd midjargon
        ```
    2.  It's recommended to use a virtual environment. If you use `uv` (as indicated by `uv.lock` and `pyproject.toml`):
        ```bash
        uv venv  # Create a virtual environment (e.g., .venv)
        uv pip install -e ".[all]" # Install in editable mode with all extras
        ```
        Alternatively, with standard `pip` and `venv`:
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # On Windows: .venv\Scripts\activate
        pip install -e ".[all]"
        ```
    3.  The project uses `hatch` for task management (testing, linting), configured in `pyproject.toml`. Ensure `hatch` is installed (`pip install hatch` or `uv pip install hatch`).

*   **Running Tests:**
    Execute tests using `hatch`:
    ```bash
    hatch test
    ```
    This will run all tests defined in the `tests` directory. New features or bug fixes must include corresponding tests.

*   **Code Formatting and Linting:**
    The project uses `Ruff` for formatting and linting. Configuration is in `pyproject.toml`.
    To format and lint your code via `hatch` (recommended):
    ```bash
    hatch run lint:all  # Runs ruff format and ruff check
    # Or individually:
    hatch run lint:fmt  # Formats and auto-fixes where possible
    hatch run lint:style # Checks for style issues
    ```
    Please ensure your code passes linting before submitting a pull request.

*   **Type Checking:**
    `midjargon` uses `mypy` for static type checking. Configuration is in `pyproject.toml`.
    To run type checks via `hatch`:
    ```bash
    hatch run lint:typing
    ```
    Code must be fully type-hinted and pass type checking.

*   **Commit Messages:**
    Follow conventional commit message standards (e.g., `feat: add new parameter support`, `fix: resolve parsing bug for nested permutations`).

*   **Pull Requests:**
    *   Submit pull requests to the main development branch.
    *   Ensure your PR includes:
        *   A clear description of the changes.
        *   Passing tests (including new tests for your changes).
        *   Passing linter and type checks.
        *   Updates to documentation (README, `docs/specification.md`) if your changes affect user-facing features or the prompt syntax.

*   **Code Style:**
    *   Follow PEP 8 guidelines, enforced by Ruff.
    *   Prioritize clarity and readability.
    *   Use the type hinting system extensively.
    *   Pydantic models are central to data validation and structuring.

### Licensing

`midjargon` is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
