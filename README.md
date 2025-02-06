# Midjargon

A Python library for parsing and manipulating Midjourney prompts using a specialized syntax. This tool helps you work with Midjourney prompts in a structured way, handling complex features like permutations, parameter validation, and image URL extraction.

## Features

- **Robust Prompt Parsing**: Parse Midjourney prompts into structured components (text, parameters, image URLs)
- **Advanced Permutation Support**: 
  - Handle nested permutations in curly braces `{option1, option2}`
  - Support for escaped characters in permutations
  - Combine permutations across text and parameters
- **Comprehensive Parameter Handling**:
  - Validate parameter names and values
  - Support for numeric ranges (stylize, chaos, weird, etc.)
  - Handle aspect ratios and style parameters
  - Proper type conversion and validation
- **Image URL Processing**:
  - Extract and validate image URLs
  - Support for multiple image inputs
  - Validate file extensions and URL formats
- **Multi-prompt Support**:
  - Handle weighted prompts using `::`
  - Process multiple variations in a single input
- **Type Safety**:
  - Full type hints throughout the codebase
  - Pydantic models for robust validation
  - Clear error messages for invalid inputs

## Installation

```bash
pip install midjargon
```

## Quick Start

```python
from midjargon import parse_prompt, parse_midjourney

# Simple prompt parsing
prompt = "a serene landscape --ar 16:9 --stylize 100"
result = parse_prompt(prompt)  # Basic parsing without validation

# Full Midjourney validation
validated = parse_midjourney(prompt)  # Returns validated MidjourneyPrompt objects

# Working with permutations
prompt_with_perms = "a {red, blue} bird on a {flower, leaf} --ar 16:9"
variations = parse_prompt(prompt_with_perms)  # Expands to all combinations

# Complex prompt with images and weights
complex_prompt = """
https://example.com/image.jpg 
mystical forest ::2 foggy mountains ::1 
--chaos 20 --stylize 100
"""
parsed = parse_midjourney(complex_prompt)
```

## Documentation

The library implements the [Midjourney Prompt Format Specification](SPEC.md) which defines:

- **Image Prompts**: Optional URLs at the start of the prompt
- **Text Description**: Required prompt text (unless image provided)
- **Parameters**: Optional modifiers with validation
- **Advanced Features**: Multi-prompts, weights, and permutations

For detailed documentation and examples, see [SPEC.md](SPEC.md).

## Development

### Project Structure

```
midjargon/
├── src/midjargon/
│   ├── __init__.py
│   ├── midjargon.py     # Core parsing functionality
│   ├── midjourney.py    # Midjourney-specific validation
│   └── permutations.py  # Permutation handling
├── tests/               # Test suite
└── SPEC.md             # Format specification
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Some ways to contribute:

- Bug fixes and feature improvements
- Documentation updates
- Additional test cases
- Performance optimizations

## License

MIT License - See LICENSE file for details 