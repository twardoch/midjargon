# Midjargon

A Python library for parsing and manipulating Midjourney prompts using a specialized syntax. This tool helps you work with Midjourney prompts in a structured way, handling complex features like permutations, parameter validation, and image URL extraction.

## Features

- **Robust Prompt Parsing**: 
  - Parse Midjourney prompts into structured components (text, parameters, image URLs)
  - Type-safe parsing with comprehensive validation
  - Support for complex prompt structures and syntax

- **Advanced Permutation Support**: 
  - Handle nested permutations in curly braces `{option1, option2}`
  - Support for escaped characters in permutations (e.g., `\,` for literal commas)
  - Combine permutations across text and parameters
  - Automatic expansion of all possible combinations

- **Comprehensive Parameter Handling**:
  - Validate parameter names and values
  - Support for numeric ranges (stylize, chaos, weird, etc.)
  - Handle aspect ratios and style parameters
  - Process boolean flags and multi-value parameters
  - Proper type conversion and validation

- **Image URL Processing**:
  - Extract and validate image URLs
  - Support for multiple image inputs
  - Validate file extensions and URL formats
  - Handle image weights and reference images

- **Multi-prompt Support**:
  - Handle weighted prompts using `::`
  - Process multiple variations in a single input
  - Support for negative weights and prompt mixing

- **Type Safety**:
  - Full type hints throughout the codebase
  - Pydantic models for robust validation
  - Clear error messages for invalid inputs
  - Modern Python type annotations

- **Rich CLI Interface**:
  - Beautiful console output with syntax highlighting
  - JSON output option for automation
  - Support for raw parsing and full validation
  - Helpful error messages and formatting

## Installation

```bash
pip install midjargon
```

## Quick Start

### Basic Usage

```python
from midjargon import parse_midjourney_dict, expand_midjargon_input

# Parse a simple prompt
prompt = "a serene landscape --ar 16:9 --stylize 100"
result = expand_midjargon_input(prompt)[0]
validated = parse_midjourney_dict(result)

# Work with permutations
prompt_with_perms = "a {red, blue} bird on a {flower, leaf} --ar 16:9"
variations = expand_midjargon_input(prompt_with_perms)
for variation in variations:
    parsed = parse_midjourney_dict(variation)
    print(parsed.text)  # Prints each combination

# Complex prompt with images and weights
complex_prompt = """
https://example.com/image.jpg 
mystical forest ::2 foggy mountains ::1 
--chaos 20 --stylize 100
"""
parsed = parse_midjourney_dict(complex_prompt)
```

### CLI Usage

```bash
# Basic prompt parsing
midjargon "a photo of a cat --ar 16:9"

# Get JSON output
midjargon --json-output "a photo of a cat --ar 16:9"

# Raw parsing without validation
midjargon --raw "any text with parameters"

# Parse prompt with permutations
midjargon "a {red, blue} bird --stylize {100, 500}"
```

## Project Structure

```
midjargon/
├── src/midjargon/
│   ├── core/           # Core parsing functionality
│   ├── engines/        # Engine-specific implementations
│   └── cli/            # Command-line interface
├── tests/              # Test suite
├── SPEC.md            # Format specification
└── CODE.md            # Code documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Some ways to contribute:

- Bug fixes and feature improvements
- Documentation updates
- Additional test cases
- Performance optimizations
- New engine implementations
- CLI enhancements

### Development Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```
4. Format code:
   ```bash
   ruff check --fix --unsafe-fixes . && ruff format --respect-gitignore --target-version py312 .
   ```

## License

MIT License - See LICENSE file for details 