# Code Organization

The `midjargon` package is organized into a modular structure with clear separation of concerns. Here's a detailed breakdown of the codebase organization:

## Directory Structure

```
src/
└── midjargon/
    ├── __init__.py         # Package exports and version
    ├── __main__.py         # CLI entry point with uv dependencies
    ├── __version__.py      # Version information
    ├── cli/                # Command-line interface
    │   ├── __init__.py
    │   └── main.py         # CLI implementation with rich output
    ├── core/               # Core functionality
    │   ├── __init__.py
    │   ├── input.py        # Input string processing
    │   ├── parameters.py   # Parameter handling
    │   ├── parser.py       # Basic prompt parsing
    │   ├── permutations.py # Permutation expansion
    │   └── type_defs.py    # Type definitions
    └── engines/            # Engine-specific implementations
        ├── __init__.py
        ├── base.py         # Base engine interfaces
        └── midjourney/     # Midjourney engine
            ├── __init__.py
            ├── constants.py # Midjourney-specific constants
            ├── models.py    # Midjourney data models
            └── parser.py    # Midjourney-specific parsing
```

## Component Overview

### 1\. Core Layer (`core/`)

The core layer provides the fundamental functionality of the package:

- **Type Definitions (`type_defs.py`)**:
  - Defines basic type aliases for the package
  - Provides foundational types for parameters and prompts

- **Input Processing (`input.py`)**:
  - Handles initial prompt string preprocessing
  - Manages whitespace and basic text normalization
  - Provides string manipulation utilities

- **Parameter Handling (`parameters.py`)**:
  - Processes command-line style parameters (e.g., `--ar 16:9`)
  - Handles parameter shortcuts and aliases
  - Supports special cases like niji versions and personalization
  - Validates parameter format and basic structure
  - Implements robust parameter string parsing

- **Basic Parsing (`parser.py`)**:
  - Implements core prompt parsing logic
  - Separates text, parameters, and image URLs
  - Handles basic validation of prompt structure

- **Permutations (`permutations.py`)**:
  - Processes permutation syntax `{option1, option2}`
  - Handles nested permutations
  - Supports escaped commas in options
  - Manages expansion of multiple permutation groups

### 2\. Engines Layer (`engines/`)

The engines layer contains engine-specific implementations:

- **Midjourney Engine (`midjourney/`)**:
  - `constants.py`: 
    - Defines parameter ranges and constraints
    - Specifies allowed file extensions
    - Lists valid styles and versions
    - Provides extensible configuration
  
  - `models.py`: 
    - Implements `ImagePrompt` for URL validation
    - Defines `MidjourneyPrompt` with comprehensive validation
    - Handles all parameter types from the spec
    - Validates parameter ranges and combinations
    - Supports mode flags and their constraints
  
  - `parser.py`: 
    - Implements Midjourney-specific parsing
    - Handles weight syntax (::)
    - Processes image references
    - Manages parameter conversion and validation

### 3\. CLI Layer (`cli/`)

The command-line interface implementation:

- **Main CLI (`main.py`)**:

  - Implements the command-line interface using Fire
  - Provides rich console output with syntax highlighting
  - Handles command parsing and execution
  - Supports raw parsing and Midjourney validation
  - Offers JSON output option
  - Uses uv for dependency management

## Data Flow

1. **Input → Core Processing**:

  - Raw input string → Input processing via `expand_midjargon_input`
  - Permutation expansion using `expand_text`
  - Basic parameter parsing with `parse_parameters`

2. **Core → Engine Processing**:

  - Parsed dictionary → Engine-specific parsing
  - Validation and normalization through Pydantic models
  - Engine-specific output generation (e.g., `MidjourneyPrompt`)

3. **Engine → Output**:

  - Final processed prompt
  - Validation results
  - Formatted output (via CLI or API)
  - Rich console output with syntax highlighting

## Usage Patterns

1. **Basic Usage**:

```python
from midjargon import expand_midjargon_input, parse_midjargon_prompt_to_dict

# Expand permutations
expanded = expand_midjargon_input("a {red, blue} bird")

# Parse into dictionary
parsed = parse_midjargon_prompt_to_dict(expanded[0])
```

2. **Engine-Specific Usage**:

```python
from midjargon.engines.midjourney import parse_midjourney_dict

# Parse for Midjourney
midjourney_prompt = parse_midjourney_dict(parsed)
```

3. **CLI Usage**:

```bash
# Basic parsing
midjargon "a photo of a cat --ar 16:9"

# JSON output
midjargon --json-output "a photo of a cat --ar 16:9"

# Raw parsing without validation
midjargon --raw "any text with parameters"
```

## Extension Points

1. **New Engines**:

  - Create new engine package in `engines/`
  - Implement engine-specific parser and models
  - Follow the base engine interface
  - Add appropriate type hints and validation

2. **Additional Parameters**:

  - Add parameter handling in `core/parameters.py`
  - Implement validation in engine-specific parsers
  - Update type definitions as needed

3. **New Features**:

  - Add core functionality in appropriate core module
  - Extend CLI commands in `cli/main.py`
  - Update type definitions in `type_defs.py`
  - Follow PEP 8 and modern Python practices
