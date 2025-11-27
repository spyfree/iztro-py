# Contributing to iztro-py

Thank you for your interest in contributing to iztro-py! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/spyfree/iztro-py.git
cd iztro-py
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/iztro_py --cov-report=term-missing

# Run specific test file
pytest tests/test_api.py
```

### Code Quality

Before submitting a PR, ensure your code passes all quality checks:

```bash
# Format code
black src tests

# Lint code
ruff check src

# Type check
mypy src --ignore-missing-imports
```

### Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

Examples:
```
feat: add support for ja-JP language
fix: correct star brightness calculation
docs: update README with new examples
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Make your changes
4. Run all quality checks
5. Commit your changes with a descriptive message
6. Push to your fork
7. Open a Pull Request

### PR Requirements

- [ ] All tests pass
- [ ] Code is formatted with Black
- [ ] No ruff warnings
- [ ] mypy passes without errors
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated for user-facing changes

## Project Structure

```
iztro-py/
├── src/iztro_py/       # Main library code
│   ├── astro/          # Chart creation and analysis
│   ├── data/           # Data types and constants
│   ├── i18n/           # Internationalization
│   ├── star/           # Star placement algorithms
│   └── utils/          # Utility functions
├── tests/              # Test files
├── docs/               # Documentation
├── examples/           # Usage examples
└── scripts/            # Development scripts
```

## Adding New Features

### Adding a New Language

1. Create a new locale file in `src/iztro_py/i18n/locales/`
2. Add the language code to `Language` type in `data/types.py`
3. Update `_load_locale()` in `i18n/__init__.py`
4. Add tests for the new language
5. Update documentation

### Adding New Stars

1. Add star name to appropriate type in `data/types.py`
2. Implement placement logic in `star/` module
3. Add brightness data if applicable
4. Add tests

## Questions?

Feel free to open an issue for any questions or discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
