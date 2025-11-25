# Contributing to Codebase Reviewer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## Getting Started

### Prerequisites

- Python 3.8+
- Go 1.19+
- Git
- Make

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/bordenet/codebase-reviewer.git
cd codebase-reviewer

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Build Go tool
make build

# Run tests
make test
```

## Development Workflow

### 1. Create a Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bug fix branch
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation

### 3. Run Tests

```bash
# Run all tests
make test

# Run specific tests
pytest tests/test_security_rules.py

# Run with coverage
pytest --cov=src/codebase_reviewer tests/

# Run linting
make lint
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new security rule for SQL injection"

# Or for bug fixes
git commit -m "fix: Correct false positive in XSS detection"
```

**Commit Message Format**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test changes
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance tasks

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

## Code Style

### Python

- **Formatter**: Black (line length: 120)
- **Import sorting**: isort
- **Linting**: Pylint, Flake8
- **Type hints**: Use type hints for all functions

```python
def analyze_code(path: str, options: Dict[str, Any]) -> AnalysisResult:
    """Analyze code at the given path.
    
    Args:
        path: Path to code directory
        options: Analysis options
        
    Returns:
        Analysis results
    """
    pass
```

### Go

- **Formatter**: gofmt
- **Linting**: golangci-lint
- **Error handling**: Always check errors

```go
func analyzeCode(path string) (*AnalysisResult, error) {
    if path == "" {
        return nil, fmt.Errorf("path cannot be empty")
    }
    // ...
}
```

## Testing

### Writing Tests

```python
# tests/test_new_feature.py
import pytest
from codebase_reviewer.new_feature import NewFeature

def test_new_feature_basic():
    """Test basic functionality."""
    feature = NewFeature()
    result = feature.process("input")
    assert result == "expected"

def test_new_feature_edge_case():
    """Test edge case."""
    feature = NewFeature()
    with pytest.raises(ValueError):
        feature.process(None)
```

### Test Coverage

- Aim for **80%+ coverage** for new code
- All security rules must have tests
- All bug fixes must have regression tests

## Adding New Features

### Adding a Security Rule

1. Create rule in `src/codebase_reviewer/rules/security/`
2. Add test in `tests/test_security_rules.py`
3. Update documentation in `docs/STATIC_ANALYSIS.md`
4. Add example in `examples/`

### Adding a Quality Rule

1. Create rule in `src/codebase_reviewer/rules/quality/`
2. Add test in `tests/test_quality_rules.py`
3. Update documentation

### Adding Language Support

1. Add parser in `src/codebase_reviewer/parsers/`
2. Add language-specific rules
3. Add tests
4. Update documentation

## Documentation

### Code Documentation

- All public functions must have docstrings
- Use Google-style docstrings
- Include examples where helpful

### User Documentation

- Update `README.md` for major features
- Update `docs/` for detailed guides
- Update `CHANGELOG.md` for all changes

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted (Black, gofmt)
- [ ] Linting passes (Pylint, golangci-lint)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Commit messages follow format

### PR Description

Include:
- **What**: What does this PR do?
- **Why**: Why is this change needed?
- **How**: How does it work?
- **Testing**: How was it tested?
- **Screenshots**: If UI changes

Example:
```markdown
## What
Adds SQL injection detection for Python Django ORM

## Why
Django ORM can be vulnerable to SQL injection when using raw queries

## How
- Added pattern matching for `raw()` and `extra()` methods
- Checks for string concatenation in queries
- Validates parameterized queries

## Testing
- Added 10 test cases covering various scenarios
- Tested on real Django projects
- No false positives detected

## Screenshots
N/A
```

## Review Process

1. **Automated Checks**: CI runs tests, linting, coverage
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address review comments
4. **Approval**: Maintainer approves PR
5. **Merge**: PR is merged to main

## Release Process

Maintainers handle releases:

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create git tag
4. Push to PyPI
5. Create GitHub release

## Questions?

- **Documentation**: Check `docs/` directory
- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Email**: bordenet@users.noreply.github.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉

