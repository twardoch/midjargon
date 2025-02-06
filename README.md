# Midjargon

A Python library for parsing and manipulating Midjourney prompts using a specialized syntax. This tool helps you work with Midjourney prompts in a structured way, handling complex features like permutations, parameter parsing, and image URL extraction.

## Features

- Parse Midjourney prompts into structured components (text, parameters, image URLs)
- Handle permutation prompts (expand combinations in curly braces)
- Process and validate prompt parameters
- Support for multi-prompts with weights
- Extract and validate image URLs
- Clean parameter handling with proper value parsing

## Installation

```bash
pip install midjargon
```

## Usage

```python
from midjargon import parse_prompt

# Simple prompt parsing
prompt = "a serene landscape --ar 16:9 --stylize 100"
result = parse_prompt(prompt)

# Handling permutations
prompt_with_permutations = "a {red, blue} bird on a {flower, leaf} --ar 16:9"
variations = parse_prompt(prompt_with_permutations)

# Working with image URLs and parameters
complex_prompt = "https://example.com/image.jpg mystical forest ::2 foggy mountains ::1 --chaos 20"
parsed = parse_prompt(complex_prompt)
```

## Documentation

The library follows the [Midjourney Prompt Format Specification](SPEC.md) which defines:

- Image prompts (optional URLs at the start)
- Text description (required if no image provided)
- Parameters (optional modifiers)
- Advanced features like multi-prompts and permutations

For detailed documentation and examples, see [SPEC.md](SPEC.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License 