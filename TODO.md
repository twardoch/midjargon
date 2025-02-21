---
this_file: TODO.md
---
# Midjargon Package Implementation Plan

## Priority 0: Critical Import Fixes [IMMEDIATE]

### 0.1 Fix Missing Exports [CRITICAL]
- [ ] Fix `__init__.py` exports
  - [ ] Add `expand_midjargon_input` to exports from `core.input`
  - [ ] Add `PromptVariant` to exports from `core.models`
  - [ ] Verify all necessary types and functions are exported

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

### 1.2 Fix Parameter Parsing [CRITICAL]
- [ ] Fix parse_parameters function
  - [ ] Fix type conversion for numeric parameters
  - [ ] Fix flag parameter handling (True/False values)
  - [ ] Fix list parameter parsing (character_reference, style_reference)
  - [ ] Fix aspect ratio parameter parsing
  - [ ] Add proper validation for all parameter types
  - [ ] Fix version parameter handling

### 1.3 Fix Core Parser [CRITICAL]
- [ ] Fix parse_midjargon_prompt function
  - [ ] Fix parameter extraction and validation
  - [ ] Fix image URL extraction
  - [ ] Fix text part extraction
  - [ ] Add proper error handling and messages
  - [ ] Fix model instantiation with parameters

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

