# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Hybrid search combining vector similarity and BM25 keyword search
- Type hints throughout the codebase
- Comprehensive logging system
- Unit tests for core components
- Retry mechanism for PDF downloads
- Configurable prompts via config.py
- User-provided ground truth for evaluations
- Security notes in README

### Changed
- Updated from OpenAI to Groq API
- Improved error handling and validation
- Enhanced scraper robustness with retries
- Better UI with hybrid search option and metrics display

### Fixed
- Inconsistencies in error messages and loader imports
- Missing dependencies in requirements.txt
- Hardcoded prompts and paths

### Security
- Removed API keys from version control
- Added .gitignore for sensitive files