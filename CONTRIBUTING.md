# Contributing

Thank you for your interest in contributing to the RAG System project! We welcome contributions from the community.

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment: `cp .env.example .env` and add your API keys
4. Run tests: `pytest`
5. Build index: `python build_index.py`
6. Run app: `streamlit run app.py`

## Code Style

- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Add docstrings to all classes and methods
- Use logging instead of print statements
- Write unit tests for new features

## Testing

- Add unit tests in the `tests/` directory
- Ensure test coverage for new code
- Run tests before submitting PR

## Reporting Issues

- Use the GitHub issue tracker
- Provide detailed steps to reproduce
- Include error messages and logs
- Specify your environment (OS, Python version, etc.)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.