# Contributing to TOPSIS Web Service

Thank you for considering contributing to this project! Please follow these guidelines when submitting contributions.

## Code of Conduct

- Be respectful to all contributors
- Provide constructive feedback
- Focus on the code, not the person

## How to Contribute

### Reporting Bugs

When reporting a bug, please include:
- A clear title and description
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment details (OS, Python version, etc.)

### Suggesting Enhancements

When suggesting enhancements, include:
- A clear description of the enhancement
- Rationale for the change
- Possible implementation approach

### Pull Requests

1. Fork the repository and create a new branch
2. Make your changes
3. Write/update tests
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request with clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/topsis-web-service.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov flake8 black
```

## Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Keep functions focused and modular
- Add unit tests for new functionality

## Testing

Before submitting a pull request:

```bash
# Run tests
python -m pytest tests/ -v

# Check code style
flake8 app/ tests/

# Format code
black app/ tests/
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings for all public functions
- Include examples for new features

## Commit Messages

Use clear, descriptive commit messages:
- ✅ `Add TOPSIS evaluation endpoint`
- ✅ `Fix weight normalization bug`
- ✅ `Update documentation`
- ❌ `Fix stuff`
- ❌ `Update`

## Review Process

A maintainer will review your pull request and:
- Verify code quality
- Check test coverage
- Validate documentation
- Suggest changes if needed

Thank you for contributing!
