---
this_file: TODO.md
---
# Midjargon Package Implementation Plan

## Priority 0: Python Version and Build System Fixes [IMMEDIATE]

### 0.1 Fix Python Version Compatibility [CRITICAL]
- [ ] Update Python version requirements in pyproject.toml
  - [ ] Change requires-python to ">=3.10" to match current environment
  - [ ] Update tool.ruff.target-version to "py310"
  - [ ] Update tool.mypy.python_version to "3.10"
  - [ ] Remove Python 3.10 from tool.hatch.envs.all.matrix (since we'll support it)
  - Detailed steps:
    1. [ ] Edit pyproject.toml:
       ```toml
       [project]
       requires-python = ">=3.10"
       
       [tool.ruff]
       target-version = "py310"
       
       [tool.mypy]
       python_version = "3.10"
       ```
    2. [ ] Update tool.hatch.envs.all.matrix to only include 3.11 and 3.12

### 0.2 Fix Build System Configuration [CRITICAL]
- [ ] Update build system dependencies
  - [ ] Verify hatchling and hatch-vcs versions
  - [ ] Add missing development dependencies
  - [ ] Fix dependency resolution issues
  - Detailed steps:
    1. [ ] Check and update build-system.requires versions
    2. [ ] Add any missing dev dependencies to tool.rye.dev-dependencies
    3. [ ] Verify all dependency versions are compatible

## Priority 1: Critical Model and Parser Fixes

### 1.1 Fix Pydantic Model Implementation [CRITICAL]
- [ ] Fix MidjourneyPrompt model validation issues
  - [ ] Fix character_reference and style_reference list validation
  - [ ] Ensure proper type conversion for list fields
  - [ ] Add proper validation for empty lists
  - [ ] Fix extra_params handling in model_dump()
  - [ ] Fix aspect ratio handling and validation
  - [ ] Fix computed_field for images property
  - [ ] Fix parameters property implementation
  - Detailed steps:
    1. [ ] Update src/midjargon/core/models.py:
       - [ ] Add proper validators for character_reference and style_reference
       - [ ] Implement proper type conversion for list fields
       - [ ] Add validation for empty lists with custom error messages
       - [ ] Fix model_dump() method to handle extra_params correctly
       - [ ] Add proper aspect ratio validation with regex pattern
       - [ ] Fix computed_field decorator usage for images property
       - [ ] Implement parameters property with proper caching

### 1.2 Fix Parameter Parsing [CRITICAL]
- [ ] Fix parse_parameters function
  - [ ] Fix type conversion for numeric parameters
  - [ ] Fix flag parameter handling (True/False values)
  - [ ] Fix list parameter parsing (character_reference, style_reference)
  - [ ] Fix aspect ratio parameter parsing
  - [ ] Add proper validation for all parameter types
  - [ ] Fix version parameter handling
  - Detailed steps:
    1. [ ] Update src/midjargon/core/parameters.py:
       - [ ] Add proper numeric type conversion with error handling
       - [ ] Implement consistent flag parameter handling
       - [ ] Fix list parameter parsing with proper delimiter handling
       - [ ] Add regex validation for aspect ratio
       - [ ] Add comprehensive parameter validation
       - [ ] Implement version parameter normalization

### 1.3 Fix Core Parser [CRITICAL]
- [ ] Fix parse_midjargon_prompt function
  - [ ] Fix parameter extraction and validation
  - [ ] Fix image URL extraction
  - [ ] Fix text part extraction
  - [ ] Add proper error handling and messages
  - [ ] Fix model instantiation with parameters
  - Detailed steps:
    1. [ ] Update src/midjargon/core/parser.py:
       - [ ] Implement robust parameter extraction
       - [ ] Add proper URL validation for images
       - [ ] Fix text extraction with proper escaping
       - [ ] Add detailed error messages
       - [ ] Fix model instantiation with validated parameters

## Priority 2: Code Quality Fixes

### 2.1 Fix Linting Issues
- [ ] Fix FBT001/FBT002 issues in CLI
  - [ ] Replace boolean positional arguments with proper flags
  - [ ] Use dataclasses or Pydantic models for CLI options
- [ ] Fix complexity issues
  - [ ] Refactor `parse_weighted_prompt` (C901)
  - [ ] Refactor `convert_parameter_value` (C901)
  - [ ] Refactor `parse_parameters` (C901)
- [ ] Fix error handling
  - [ ] Replace bare excepts with specific exception handling
  - [ ] Add proper error chaining with `raise ... from`
  - [ ] Add descriptive error messages

### 2.2 Fix Type Safety
- [ ] Add proper type hints throughout
- [ ] Fix unused arguments (ARG003)
- [ ] Add validation for all input parameters
- [ ] Add runtime type checking where necessary

## Priority 3: Core Functionality Fixes

### 3.1 Fix Permutation Handling
- [ ] Fix expand_midjargon_input function
  - [ ] Fix weighted prompt handling
  - [ ] Fix nested permutation groups
  - [ ] Fix whitespace handling
  - [ ] Fix escape character handling
  - [ ] Add proper validation for permutation syntax

### 3.2 Fix Input Processing
- [ ] Fix input validation and sanitization
  - [ ] Add proper URL validation
  - [ ] Fix multi-prompt handling
  - [ ] Fix weight parsing
  - [ ] Add proper input sanitization
  - [ ] Fix escape character handling

### 3.3 Fix CLI Implementation
- [ ] Fix command implementations
  - [ ] Fix 'mj' command
  - [ ] Fix 'fal' command
  - [ ] Fix 'perm' command
  - [ ] Fix JSON output formatting
  - [ ] Add proper error handling

## Priority 4: Engine-Specific Fixes

### 4.1 Fix Midjourney Engine
- [ ] Fix MidjourneyParser implementation
  - [ ] Fix parameter mapping
  - [ ] Fix type conversion
  - [ ] Fix validation
  - [ ] Fix reference handling

### 4.2 Fix Fal.ai Engine
- [ ] Fix FalParser implementation
  - [ ] Fix parameter mapping
  - [ ] Fix type conversion
  - [ ] Fix validation
  - [ ] Fix reference handling

## Priority 5: Testing and Documentation

### 5.1 Fix Test Suite
- [ ] Fix core functionality tests
  - [ ] Fix parameter parsing tests
  - [ ] Fix model validation tests
  - [ ] Fix permutation tests
  - [ ] Add missing edge cases

### 5.2 Update Documentation
- [ ] Update API documentation
  - [ ] Document model attributes
  - [ ] Document parameter handling
  - [ ] Document CLI commands
  - [ ] Add error handling guide

## Implementation Order

1. Start with Priority 0: Fix missing exports (IMMEDIATE)
   - This is blocking the test suite from running
   - Add missing exports to __init__.py

2. Move to Priority 1: Critical Model and Parser Fixes
   - Fix MidjourneyPrompt model validation issues
   - Fix parameter parsing
   - Fix core parser implementation

3. Address Priority 2: Code Quality Fixes
   - Fix linting issues
   - Improve type safety
   - Clean up error handling

4. Then proceed with remaining priorities in order

## Current Focus

The immediate focus should be on fixing the missing exports in __init__.py:
1. Add `expand_midjargon_input` to exports
2. Add `PromptVariant` to exports
3. Verify all necessary types and functions are exported

## Dependencies
- pydantic (>=2.0.0)
- rich (>=13.0.0)
- fire (>=0.5.0)
- python-box (>=7.3.2)
- fal-client (>=0.5.8)

## Development Guidelines
1. Maintain type safety
2. Follow code quality standards
3. Add comprehensive tests
4. Keep documentation updated
5. Consider performance
6. Handle errors gracefully

## Priority 0: Model Implementation Fixes [IMMEDIATE]

### 0.1 Fix MidjourneyPrompt Model [CRITICAL]
- [ ] Add missing methods to MidjourneyPrompt class
  - [ ] Implement `to_string()` method
  - [ ] Fix model validation for image references
  - [ ] Add proper attribute access for parameters
  - Detailed steps:
    1. [ ] Update src/midjargon/core/models.py:
       ```python
       def to_string(self) -> str:
           """Convert prompt back to string format."""
           parts = [self.text]
           if self.image_prompts:
               parts = [str(img) for img in self.image_prompts] + parts
           if self.parameters:
               parts.append(self.parameters.to_string())
           return " ".join(parts)
       ```
    2. [ ] Fix image reference validation in model definition
    3. [ ] Add proper parameter attribute access

### 0.2 Fix MidjourneyParameters Model [CRITICAL]
- [ ] Add missing attributes to MidjourneyParameters class
  - [ ] Add `aspect` property
  - [ ] Add `style_reference` handling
  - [ ] Add `character_reference` handling
  - [ ] Fix parameter validation
  - Detailed steps:
    1. [ ] Update parameter model in src/midjargon/core/models.py
    2. [ ] Add computed properties for convenience access
    3. [ ] Fix parameter validation rules

### 0.3 Fix Parameter Parsing [CRITICAL]
- [ ] Fix parameter parsing in core/parameters.py
  - [ ] Fix flag parameter handling
  - [ ] Fix numeric parameter validation
  - [ ] Fix reference parameter parsing
  - [ ] Add proper error handling
  - Detailed steps:
    1. [ ] Update parameter parsing logic
    2. [ ] Add proper validation for all parameter types
    3. [ ] Improve error messages

## Priority 1: CLI Implementation Fixes

### 1.1 Fix CLI Commands [HIGH]
- [ ] Fix CLI command implementations
  - [ ] Fix JSON output formatting
  - [ ] Fix command error handling
  - [ ] Fix parameter handling in commands
  - Detailed steps:
    1. [ ] Update src/midjargon/cli/main.py
    2. [ ] Fix JSON serialization
    3. [ ] Add proper error handling
    4. [ ] Fix parameter processing

### 1.2 Fix Integration Tests [HIGH]
- [ ] Fix integration test failures
  - [ ] Fix workflow tests
  - [ ] Fix CLI command tests
  - [ ] Fix parameter handling tests
  - Detailed steps:
    1. [ ] Update test assertions
    2. [ ] Fix test data
    3. [ ] Add missing test cases

## Priority 2: Core Functionality Fixes

### 2.1 Fix Permutation Handling
- [ ] Fix expand_midjargon_input function
  - [ ] Fix weighted prompt handling
  - [ ] Fix nested permutation groups
  - [ ] Fix whitespace handling
  - [ ] Fix escape character handling
  - [ ] Add proper validation for permutation syntax

### 2.2 Fix Input Processing
- [ ] Fix input validation and sanitization
  - [ ] Add proper URL validation
  - [ ] Fix multi-prompt handling
  - [ ] Fix weight parsing
  - [ ] Add proper input sanitization
  - [ ] Fix escape character handling

### 2.3 Fix CLI Implementation
- [ ] Fix command implementations
  - [ ] Fix 'mj' command
  - [ ] Fix 'fal' command
  - [ ] Fix 'perm' command
  - [ ] Fix JSON output formatting
  - [ ] Add proper error handling

### 2.4 Fix Engine-Specific Implementations
- [ ] Fix MidjourneyParser implementation
  - [ ] Fix parameter mapping
  - [ ] Fix type conversion
  - [ ] Fix validation
  - [ ] Fix reference handling

- [ ] Fix FalParser implementation
  - [ ] Fix parameter mapping
  - [ ] Fix type conversion
  - [ ] Fix validation
  - [ ] Fix reference handling

## Priority 3: Testing and Documentation

### 3.1 Fix Test Suite
- [ ] Fix core functionality tests
  - [ ] Fix parameter parsing tests
  - [ ] Fix model validation tests
  - [ ] Fix permutation tests
  - [ ] Add missing edge cases

### 3.2 Update Documentation
- [ ] Update API documentation
  - [ ] Document model attributes
  - [ ] Document parameter handling
  - [ ] Document CLI commands
  - [ ] Add error handling guide

## Implementation Order

1. Start with Priority 0: Fix missing exports (IMMEDIATE)
   - This is blocking the test suite from running
   - Add missing exports to __init__.py

2. Move to Priority 1: Critical Model and Parser Fixes
   - Fix MidjourneyPrompt model validation issues
   - Fix parameter parsing
   - Fix core parser implementation

3. Address Priority 2: Code Quality Fixes
   - Fix linting issues
   - Improve type safety
   - Clean up error handling

4. Then proceed with remaining priorities in order

## Current Focus

The immediate focus should be on fixing the missing exports in __init__.py:
1. Add `expand_midjargon_input` to exports
2. Add `PromptVariant` to exports
3. Verify all necessary types and functions are exported

## Dependencies
- pydantic (>=2.0.0)
- rich (>=13.0.0)
- fire (>=0.5.0)
- python-box (>=7.3.2)
- fal-client (>=0.5.8)

## Development Guidelines
1. Maintain type safety
2. Follow code quality standards
3. Add comprehensive tests
4. Keep documentation updated
5. Consider performance
6. Handle errors gracefully

