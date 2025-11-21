# Repository Quality Bootstrap Guide

**Purpose**: Transform any Python repository into an enterprise-grade project with comprehensive CI/CD, quality enforcement, and professional documentation.

**Target Audience**: AI assistants (Claude, GPT-4, etc.) tasked with improving repository quality standards.

---

## 🎯 Mission Statement

When asked to "bring this repository up to professional standards" or "add proper CI/CD and quality checks", execute ALL of the following steps. Do not ask permission for each step - this is a comprehensive quality upgrade that includes everything below.

---

## 📋 Complete Checklist

Execute these in order. Mark each as complete before moving to the next.

### Phase 1: Code Quality Infrastructure

#### 1.1 Add Development Dependencies

**File**: `setup.py` or `pyproject.toml`

Add to `extras_require` (setup.py) or `[project.optional-dependencies]` (pyproject.toml):

```python
"dev": [
    "pylint>=3.0.3",
    "pytest>=7.4.3",
    "pytest-cov>=4.1.0",
    "black>=23.12.1",
    "mypy>=1.7.1",
    "isort>=5.13.2",
    "pre-commit>=3.6.0",
],
```

**Verification**: Run `pip install -e ".[dev]"` successfully.

#### 1.2 Create Coverage Configuration

**File**: `.coveragerc`

```ini
[run]
source = src/<package_name>
omit =
    */tests/*
    */test_*.py
    */__pycache__/*
    */venv/*
    */.venv/*
    */setup.py

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov
```

**Action**: Replace `<package_name>` with actual package name.

#### 1.3 Create Pre-Commit Configuration

**File**: `.pre-commit-config.yaml`

```yaml
# Pre-commit hooks for quality enforcement
# See https://pre-commit.com for more information

repos:
  # General file checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements
      - id: mixed-line-ending

  # Python code formatting with black
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        args: ['--line-length=120']
        language_version: python3

  # Python import sorting
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile', 'black', '--line-length', '120']

  # Python linting with pylint
  - repo: local
    hooks:
      - id: pylint
        name: pylint
        entry: .venv/bin/python
        args: ['-m', 'pylint', 'src/<package_name>', '--max-line-length=120', '--fail-under=9.5']
        language: system
        types: [python]
        require_serial: true
        pass_filenames: false
        always_run: true

  # Python type checking with mypy
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: .venv/bin/python
        args: ['-m', 'mypy', 'src/<package_name>', '--ignore-missing-imports']
        language: system
        types: [python]
        require_serial: true
        pass_filenames: false
        always_run: true

  # Run pytest tests with coverage
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: .venv/bin/python
        args: ['-m', 'pytest', 'tests/', '-v', '--tb=short', '--cov=src/<package_name>', '--cov-report=term-missing:skip-covered', '--cov-fail-under=80']
        language: system
        types: [python]
        require_serial: true
        pass_filenames: false
        always_run: true

  # Check requirements.txt is sorted
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: requirements-txt-fixer
        files: requirements.txt
```

**Actions**:
- Replace ALL instances of `<package_name>` with actual package name
- Adjust paths if project uses different structure (e.g., no `src/` directory)
- Adjust coverage threshold (80%) based on current coverage

**Verification**: Run `pre-commit install` and `pre-commit run --all-files`.

---

### Phase 2: GitHub Actions CI/CD Pipeline

#### 2.1 Create CI Workflow

**File**: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt', '**/pyproject.toml') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -e ".[dev]"

    - name: Run black (code formatting check)
      run: |
        black --check --line-length=120 src/<package_name> tests/

    - name: Run isort (import sorting check)
      run: |
        isort --check-only --profile black --line-length 120 src/<package_name> tests/

    - name: Run pylint
      run: |
        pylint src/<package_name> --max-line-length=120 --fail-under=9.5

    - name: Run mypy
      run: |
        mypy src/<package_name> --ignore-missing-imports

    - name: Run tests with coverage
      run: |
        pytest tests/ -v --cov=src/<package_name> --cov-report=xml --cov-report=term-missing

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false
      env:
        CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pre-commit

    - name: Run pre-commit hooks
      run: |
        pip install -r requirements.txt
        pip install -e ".[dev]"
        pre-commit run --all-files
```

**Actions**:
- Replace ALL instances of `<package_name>` with actual package name
- Adjust Python versions in matrix based on project requirements
- Adjust branch names if using different convention (main vs master)
- Adjust paths if not using `src/` directory structure

**Verification**: Push to GitHub and verify workflow runs successfully.

#### 2.2 Optional: Add Release Workflow

**File**: `.github/workflows/release.yml`

```yaml
name: Release

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
      run: twine upload dist/*
```

**Note**: Only add if project will be published to PyPI.

---

### Phase 3: Professional README Badges

#### 3.1 Add Comprehensive Badge Section

**File**: `README.md`

Add immediately after the title (line 1-3):

```markdown
# Project Name

[![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/<owner>/<repo>/branch/main/graph/badge.svg)](https://codecov.io/gh/<owner>/<repo>)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Linting: pylint](https://img.shields.io/badge/linting-pylint%209.5+-yellowgreen)](https://github.com/PyCQA/pylint)
[![Type checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue)](https://github.com/python/mypy)
[![Testing: pytest](https://img.shields.io/badge/testing-pytest-green)](https://github.com/pytest-dev/pytest)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/<owner>/<repo>/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/<owner>/<repo>.svg)](https://github.com/<owner>/<repo>/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/<owner>/<repo>.svg)](https://github.com/<owner>/<repo>/pulls)

Project description here...
```

**Actions**:
- Replace `<owner>` with GitHub username/organization
- Replace `<repo>` with repository name
- Adjust Python version badge to match minimum requirement
- Adjust license badge if not MIT
- Change branch name in codecov badge if not using `main`

**Badge Customization Options**:
- Add language-specific badges (e.g., Flask, Django, FastAPI)
- Add deployment badges (Heroku, AWS, etc.)
- Add documentation badges (Read the Docs, GitHub Pages)
- Add download/install badges (PyPI downloads, etc.)

---

### Phase 4: Documentation Updates

#### 4.1 Add Development Section to README

Add or update the "Development" section in README.md:

```markdown
## Development

### Setup

```bash
# Clone repository
git clone https://github.com/<owner>/<repo>.git
cd <repo>

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/<package_name> --cov-report=html --cov-report=term-missing

# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Code Quality

```bash
# Format code with black
black src/<package_name> tests/

# Sort imports
isort src/<package_name> tests/

# Run linting
pylint src/<package_name>

# Run type checking
mypy src/<package_name>

# Run all pre-commit hooks manually
pre-commit run --all-files
```

### Pre-Commit Hooks

This project uses pre-commit hooks to enforce code quality. All commits must pass:

- **Black** - Code formatting (auto-fixes)
- **isort** - Import sorting (auto-fixes)
- **PyLint** - Linting (requires 9.5+/10)
- **MyPy** - Type checking
- **Pytest** - All tests must pass with 80%+ coverage

The hooks run automatically on `git commit`. If they fail, the commit is blocked.
```

**Actions**:
- Replace `<owner>`, `<repo>`, and `<package_name>` with actual values
- Adjust coverage threshold if different from 80%
- Add project-specific setup steps if needed

#### 4.2 Create or Update CONTRIBUTING.md

**File**: `CONTRIBUTING.md`

```markdown
# Contributing to <Project Name>

Thank you for your interest in contributing!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/<your-username>/<repo>.git`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Install dependencies: `pip install -e ".[dev]"`
6. Install pre-commit hooks: `pre-commit install`

## Code Quality Standards

All contributions must meet these standards:

### Formatting
- **Black**: Code must be formatted with black (line length: 120)
- **isort**: Imports must be sorted

### Quality Checks
- **PyLint**: Must score 9.5+/10
- **MyPy**: Must pass type checking
- **Tests**: All tests must pass
- **Coverage**: New code must maintain 80%+ coverage

### Pre-Commit Hooks

Pre-commit hooks automatically enforce these standards. They run on every commit.

To run manually:
```bash
pre-commit run --all-files
```

## Testing

### Writing Tests
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use pytest fixtures for common setup
- Aim for high coverage of new code

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/<package_name> --cov-report=term-missing

# Run specific test file
pytest tests/test_specific.py -v
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Ensure all tests pass: `pytest tests/ -v`
4. Ensure pre-commit hooks pass: `pre-commit run --all-files`
5. Commit your changes (pre-commit hooks will run automatically)
6. Push to your fork: `git push origin feature/your-feature-name`
7. Open a Pull Request

### PR Requirements
- [ ] All tests pass
- [ ] Code coverage maintained or improved
- [ ] Pre-commit hooks pass
- [ ] Code is documented (docstrings for public APIs)
- [ ] CHANGELOG.md updated (if applicable)

## Code Style

- Follow PEP 8 (enforced by black and pylint)
- Use type hints for function signatures
- Write docstrings for public functions/classes
- Keep functions focused and small
- Write descriptive variable names

## Questions?

Open an issue or reach out to the maintainers.
```

**Actions**:
- Replace `<Project Name>`, `<repo>`, `<package_name>` with actual values
- Customize contribution guidelines based on project needs
- Add project-specific coding conventions

---

### Phase 5: External Service Setup

⚠️ **CRITICAL**: These steps are REQUIRED for badges to work. Do not skip!

#### 5.1 Codecov Setup (REQUIRED)

**Why**: Without this, the codecov badge will show "unknown" and coverage won't be tracked.

**Steps**:
1. Visit https://codecov.io
2. Click "Sign up" or "Log in" → Choose "Sign in with GitHub"
3. Authorize Codecov to access your GitHub account
4. Click "Add new repository" or go to https://app.codecov.io/gh/<owner>
5. Find your repository in the list and click it
6. You'll see a setup page with your upload token
7. Copy the upload token (starts with something like `abc123...`)
8. Go to your GitHub repository
9. Click Settings → Secrets and variables → Actions
10. Click "New repository secret"
11. Name: `CODECOV_TOKEN` (exactly this, case-sensitive)
12. Value: (paste the token you copied)
13. Click "Add secret"

**Verification**:
- Secret should appear in the list (value will be hidden)
- Next CI run should upload coverage to Codecov
- Codecov badge should update within 5 minutes of successful upload

**Troubleshooting**:
- If badge still shows "unknown" after CI run, check Codecov dashboard for errors
- Verify token is named exactly `CODECOV_TOKEN`
- Check CI logs for "Upload coverage to Codecov" step - should show success
- May need to wait 5-10 minutes for badge to update after first upload

#### 5.2 Fix CI Failures (REQUIRED)

**Why**: CI badge shows "failing" when tests/quality checks don't pass.

**Common Causes & Fixes**:

**A. Coverage Below Threshold**

Check CI logs for:
```
FAILED tests/ - AssertionError: coverage is below 80%
```

**Fix Options**:
1. **Improve test coverage** (preferred):
   ```bash
   # Find uncovered code
   pytest tests/ -v --cov=src/<package_name> --cov-report=term-missing
   # Add tests for missing lines
   ```

2. **Lower threshold temporarily**:
   - Edit `.pre-commit-config.yaml`: Change `--cov-fail-under=80` to `--cov-fail-under=60`
   - Edit `.github/workflows/ci.yml`: Add `--cov-fail-under=60` to pytest command
   - Commit and push

**B. Pylint Score Below 9.5**

Check CI logs for:
```
Your code has been rated at 8.5/10
```

**Fix Options**:
1. **Fix linting issues** (preferred):
   ```bash
   # See all issues
   pylint src/<package_name>
   # Fix issues in code
   ```

2. **Lower threshold temporarily**:
   - Edit `.pre-commit-config.yaml`: Change `--fail-under=9.5` to `--fail-under=8.0`
   - Edit `.github/workflows/ci.yml`: Change `--fail-under=9.5` to `--fail-under=8.0`
   - Commit and push

**C. Type Checking Failures**

Check CI logs for mypy errors.

**Fix Options**:
1. **Fix type issues** (preferred):
   ```bash
   mypy src/<package_name>
   # Add type hints or fix type errors
   ```

2. **Add exceptions**:
   - Create `mypy.ini`:
     ```ini
     [mypy]
     ignore_missing_imports = True
     disallow_untyped_defs = False
     ```

**D. Import Sorting Issues**

Check CI logs for isort errors.

**Fix**:
```bash
# Auto-fix locally
isort src/<package_name> tests/
# Commit and push
```

**E. Code Formatting Issues**

Check CI logs for black errors.

**Fix**:
```bash
# Auto-fix locally
black src/<package_name> tests/
# Commit and push
```

**Verification After Fixes**:
1. Run locally: `pre-commit run --all-files`
2. All checks should pass
3. Commit and push
4. Wait for CI to complete (check Actions tab)
5. CI badge should turn green within 2-3 minutes

#### 5.3 Optional: Read the Docs Setup

If project needs documentation hosting:

1. Visit https://readthedocs.org
2. Import the repository
3. Configure build settings
4. Add badge to README:
   ```markdown
   [![Documentation Status](https://readthedocs.org/projects/<project>/badge/?version=latest)](https://<project>.readthedocs.io/en/latest/?badge=latest)
   ```

---

### Phase 6: Verification & Testing

#### 6.1 Local Verification Checklist

Run these commands locally to verify everything works:

```bash
# 1. Install in development mode
pip install -e ".[dev]"

# 2. Install pre-commit hooks
pre-commit install

# 3. Run pre-commit on all files
pre-commit run --all-files

# 4. Run tests with coverage
pytest tests/ -v --cov=src/<package_name> --cov-report=term-missing

# 5. Verify coverage threshold
pytest tests/ -v --cov=src/<package_name> --cov-fail-under=80

# 6. Run individual quality checks
black --check src/<package_name> tests/
isort --check-only src/<package_name> tests/
pylint src/<package_name> --fail-under=9.5
mypy src/<package_name>
```

**Expected Results**:
- ✅ All pre-commit hooks pass
- ✅ All tests pass
- ✅ Coverage meets threshold (80%+)
- ✅ Linting score 9.5+/10
- ✅ Type checking passes

#### 6.2 GitHub Actions Verification

After pushing to GitHub:

1. Go to repository → Actions tab
2. Verify CI workflow runs
3. Check that all jobs pass (test matrix + lint)
4. Verify coverage upload to Codecov
5. Check that badges update correctly

#### 6.3 Badge Verification

Visit the README on GitHub and verify:
- ✅ CI badge shows "passing"
- ✅ Coverage badge shows percentage
- ✅ All badges render correctly
- ✅ Badge links work

---

## 🚨 Common Issues & Solutions

### Issue: Pre-commit hooks fail on first run

**Solution**: This is normal. Pre-commit downloads hook environments on first run. Run again:
```bash
pre-commit run --all-files
```

### Issue: Coverage below threshold

**Solution**: Either improve test coverage or temporarily lower threshold in `.pre-commit-config.yaml`:
```yaml
args: [..., '--cov-fail-under=60']  # Lower from 80 to 60
```

### Issue: Pylint score below 9.5

**Solution**: Fix issues or add `.pylintrc` to customize rules:
```bash
pylint --generate-rcfile > .pylintrc
# Edit .pylintrc to disable specific checks
```

### Issue: CI fails but local passes

**Causes**:
- Different Python versions
- Missing dependencies in requirements.txt
- Path differences (Windows vs Linux)

**Solution**: Test locally with same Python version as CI matrix.

### Issue: Codecov badge shows "unknown"

**Solution**:
1. Verify CODECOV_TOKEN is set in GitHub secrets
2. Wait for first successful CI run with coverage upload
3. Check Codecov dashboard for errors

---

## 📊 Success Criteria

After completing all phases, the repository should have:

### Infrastructure
- ✅ Pre-commit hooks configured and working
- ✅ GitHub Actions CI/CD pipeline running
- ✅ Code coverage tracking with Codecov
- ✅ All quality tools configured (black, isort, pylint, mypy, pytest)

### Documentation
- ✅ Professional README with comprehensive badges
- ✅ Development setup instructions
- ✅ Contributing guidelines
- ✅ Code quality standards documented

### Quality Gates
- ✅ All commits blocked if quality checks fail
- ✅ All PRs require CI to pass
- ✅ Coverage threshold enforced (80%+)
- ✅ Linting threshold enforced (9.5+/10)

### Visibility
- ✅ CI status visible via badge
- ✅ Code coverage visible via badge
- ✅ Quality standards visible in README
- ✅ Maintenance status clear

---

## 🎓 Best Practices for AI Assistants

### When Executing This Guide

1. **Don't ask permission for each step** - This is a comprehensive upgrade; execute all phases
2. **Use task management** - Create tasks for each phase and mark complete as you go
3. **Verify each phase** - Run verification commands before moving to next phase
4. **Adapt to project structure** - Adjust paths/names based on actual project layout
5. **Test before committing** - Always run tests and pre-commit hooks locally first
6. **Commit atomically** - One commit per phase with descriptive message
7. **Push and verify** - After pushing, verify CI runs successfully

### Customization Points

Always check and adapt these to the specific project:

- **Package name**: Replace `<package_name>` everywhere
- **Python versions**: Adjust based on project requirements
- **Coverage threshold**: Start lower if current coverage is low
- **Linting threshold**: May need to start at 8.0 and gradually increase
- **Directory structure**: Adjust if not using `src/` layout
- **Branch names**: Adjust if using `master` instead of `main`

### Communication with User

After completing all phases, provide:

1. **Summary of changes** - List all files created/modified
2. **Verification results** - Show test results, coverage percentage
3. **Next steps** - Codecov setup, any manual configuration needed
4. **Links** - Direct links to CI runs, coverage reports

### Example Completion Message

```
✅ Repository quality upgrade complete!

## Changes Made
- Created .github/workflows/ci.yml (CI/CD pipeline)
- Created .pre-commit-config.yaml (quality enforcement)
- Created .coveragerc (coverage configuration)
- Updated README.md (added 12 professional badges)
- Updated setup.py (added dev dependencies)
- Created CONTRIBUTING.md (contribution guidelines)

## Current Status
- Tests: 45/45 passing ✅
- Coverage: 87.3% (exceeds 80% threshold) ✅
- Linting: 9.8/10 (exceeds 9.5 threshold) ✅
- Type checking: Passing ✅

## Next Steps
1. Set up Codecov: https://codecov.io (add CODECOV_TOKEN to GitHub secrets)
2. Review CI run: https://github.com/<owner>/<repo>/actions
3. Verify badges: https://github.com/<owner>/<repo>

All changes committed and pushed to origin/main.
```

---

## 📝 Template Commit Messages

Use these commit message templates:

### Phase 1
```
Add code quality infrastructure

- Add development dependencies (pylint, mypy, black, pytest-cov)
- Create .coveragerc for coverage configuration
- Create .pre-commit-config.yaml with comprehensive hooks
- Configure black (120 line length), isort, pylint (9.5+), mypy
- Add pytest with 80% coverage requirement
```

### Phase 2
```
Add GitHub Actions CI/CD pipeline

- Create .github/workflows/ci.yml
- Add multi-version Python testing (3.9-3.12)
- Add quality checks: black, isort, pylint, mypy
- Add pytest with coverage reporting
- Add Codecov integration
- Add separate lint job for pre-commit validation
```

### Phase 3
```
Add professional README badges and documentation

- Add 12 comprehensive badges (CI, coverage, quality tools)
- Add Development section with setup instructions
- Add testing and code quality documentation
- Create CONTRIBUTING.md with contribution guidelines
- Document pre-commit hooks and quality standards
```

---

## 🔗 Reference Links

- **Pre-commit**: https://pre-commit.com
- **Black**: https://black.readthedocs.io
- **Pylint**: https://pylint.pycqa.org
- **MyPy**: https://mypy.readthedocs.io
- **Pytest**: https://docs.pytest.org
- **Codecov**: https://codecov.io
- **GitHub Actions**: https://docs.github.com/en/actions
- **Shields.io** (badges): https://shields.io

---

**Version**: 1.0
**Last Updated**: 2025-11-21
**Maintained By**: AI Assistant Quality Standards Team


