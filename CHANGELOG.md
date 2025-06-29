# Changelog

All notable changes to the midjargon project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation in README.md detailing all features and usage
- Pre-commit hooks configuration for code quality enforcement
- Full test suite coverage for core functionality
- GitHub Actions workflows for CI/CD (push.yml and release.yml)
- Devcontainer configuration for consistent development environments
- Examples directory with basic usage demonstrations
- Detailed error tracking in ERRORS.txt
- Support for multiple AI engine formats (Midjourney and Fal.ai)

### Changed
- Major refactoring of codebase structure with improved organization
- Enhanced parameter parsing with better validation and type safety
- Improved permutation engine with support for nested groups and escaped characters
- Better error handling with descriptive error messages throughout

### Fixed
- Multiple linting issues identified by ruff
- Type safety improvements across all modules
- Parameter validation edge cases
- Permutation handling for complex nested structures

## [2.2.0] - 2024-12-28

### Added
- Initial stable release with core functionality
- Midjourney prompt parsing capabilities
- CLI interface with json, mj, fal, and perm commands
- Pydantic models for type-safe operations
- Support for image URL extraction and validation
- Weight parsing for multi-prompt handling
- Parameter conversion for different AI engines

## Previous Versions

The project underwent rapid development with versions 1.5.0 through 1.8.1, focusing on:
- Core parsing engine implementation
- CLI tool development
- Testing framework setup
- Documentation improvements
- Bug fixes and stability improvements

[Unreleased]: https://github.com/twardoch/midjargon/compare/v2.2.0...HEAD
[2.2.0]: https://github.com/twardoch/midjargon/releases/tag/v2.2.0