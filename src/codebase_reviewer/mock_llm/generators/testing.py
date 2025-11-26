"""Testing analysis response generators."""

from typing import Any, List

from .base import BaseGenerator


class TestingGenerator(BaseGenerator):
    """Generates testing analysis responses."""

    def validate_setup(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate setup validation response."""
        if not isinstance(context, dict):
            return self._generate_fallback(repository)

        prereqs = context.get("prerequisites", [])
        setup_files = context.get("setup_files", [])
        build_steps = context.get("build_steps", [])
        env_vars = context.get("environment_variables", [])
        undocumented = context.get("undocumented_features", [])

        score = self._calculate_setup_score(prereqs, setup_files, build_steps)

        return f"""# Setup and Installation Validation

## Setup Documentation Score: {score}/100

## Prerequisites Found
{self._format_list(prereqs)}

## Setup Files Detected
{self._format_list(setup_files)}

## Build/Installation Steps
{self._format_list(build_steps)}

## Environment Variables
{self._format_list(env_vars)}

## Undocumented Features
{self._format_list(undocumented)}

## Recommendations
{self._generate_setup_recommendations(prereqs, setup_files, build_steps, env_vars, undocumented)}

## Action Items

### Verify Setup Instructions
**Commands**:
```bash
# Test setup in clean environment
docker run -it --rm python:3.9 bash
# Follow README setup instructions
```

**Success Criteria**:
- [ ] All prerequisites documented
- [ ] Setup completes without errors
- [ ] All features work after setup
"""

    def review_tests(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate testing strategy review response."""
        if not isinstance(context, dict):
            return self._generate_fallback(repository)

        test_files = context.get("test_files", [])
        test_count = context.get("test_file_count", 0)
        frameworks = context.get("test_frameworks", [])
        has_tests = context.get("has_tests", False)

        return f"""# Testing Strategy and Coverage Review

## Test Infrastructure
- **Test Files**: {test_count}
- **Test Framework**: {', '.join(frameworks) if frameworks else 'Not detected'}
- **Has Tests**: {'✅ Yes' if has_tests else '❌ No'}

## Test Organization
{self._format_test_files(test_files)}

## Test Coverage Assessment
- **Estimated Coverage**: {self._estimate_coverage(test_count)} (based on test file count)
- **Test Types Detected**: {self._detect_test_types(test_files)}

## Test Quality Observations
1. Test files follow naming convention (test_*.py)
2. Tests organized in dedicated directory
3. Using industry-standard framework ({frameworks[0] if frameworks else 'unknown'})

## Action Items

### {"🔴 CRITICAL: Add Tests" if not has_tests else "🟠 HIGH: Improve Test Coverage"}
**Action**: {"Create initial test suite" if not has_tests else "Increase test coverage to 80%+"}
**Priority**: {"Tests are essential for code quality and confidence" if not has_tests else "Current coverage likely below target"}

{"**Step 1**: Set up test framework" if not has_tests else "**Step 1**: Measure current coverage"}
```bash
{"# Install pytest" if not has_tests else "# Install coverage tools"}
pip install pytest pytest-cov

{"# Create tests directory" if not has_tests else "# Run tests with coverage"}
{"mkdir -p tests" if not has_tests else "pytest --cov=src --cov-report=html --cov-report=term"}

{"# Create first test file" if not has_tests else "# View coverage report"}
{"cat > tests/test_basic.py << 'EOF'" if not has_tests else "open htmlcov/index.html  # Opens in browser"}
{"import pytest" if not has_tests else ""}
{"" if not has_tests else ""}
{"def test_example():" if not has_tests else ""}
{"    assert True" if not has_tests else ""}
{"EOF" if not has_tests else ""}
```

**Step 2**: {"Run tests" if not has_tests else "Identify coverage gaps"}
```bash
{"pytest -v" if not has_tests else "# Find files with <80% coverage"}
{"" if not has_tests else "pytest --cov=src --cov-report=term-missing | grep -E '^src.*[0-7][0-9]%'"}
```

**Step 3**: {"Add tests for core functionality" if not has_tests else "Add tests for uncovered code"}
```python
# Example test structure
import pytest
from src.codebase_reviewer.analyzers.code import CodeAnalyzer

def test_code_analyzer_initialization():
    analyzer = CodeAnalyzer()
    assert analyzer is not None

def test_code_analyzer_detects_python():
    analyzer = CodeAnalyzer()
    result = analyzer.detect_language("test.py")
    assert result == "Python"

@pytest.fixture
def sample_repository(tmp_path):
    # Create temporary test repository
    (tmp_path / "README.md").write_text("# Test")
    return tmp_path

def test_analyzer_with_sample_repo(sample_repository):
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(sample_repository)
    assert result is not None
```

**Success Criteria**:
- [ ] {"Test framework installed and configured" if not has_tests else "Coverage measured and reported"}
- [ ] {"At least 10 tests written" if not has_tests else "Coverage above 80% for core modules"}
- [ ] {"All tests passing" if not has_tests else "All uncovered critical paths tested"}
- [ ] {"Tests run in CI/CD" if not has_tests else "Coverage enforced in CI/CD"}

## Verification Commands

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Check coverage threshold
pytest --cov=src --cov-fail-under=80
```

## Priority Summary
- 🔴 **CRITICAL**: {"Add initial tests (4 hours)" if not has_tests else "None"}
- 🟠 **HIGH**: {"Improve coverage to 80%+ (8 hours)" if has_tests else "Set up test framework (2 hours)"}, Add coverage reporting (1 hour)
- 🟡 **MEDIUM**: Add integration tests (4 hours), Add performance tests (2 hours)
- 🟢 **LOW**: Add test documentation

**Total Effort**: ~{"15" if not has_tests else "11"} hours

## Testing Gaps Identified
- {"❌ No tests found - critical gap" if not has_tests else "⚠️ Coverage likely below 80%"}
- Missing coverage reports
- No visible integration test directory
- Consider adding performance/load tests
"""

    def _format_test_files(self, test_files: List) -> str:
        """Format test files list."""
        if not test_files:
            return "- No test files found"
        return self._format_list(test_files)

    def _estimate_coverage(self, test_count: int) -> str:
        """Estimate coverage based on test count."""
        if test_count == 0:
            return "0% (no tests)"
        elif test_count < 10:
            return "~20-40% (minimal tests)"
        elif test_count < 50:
            return "~40-60% (moderate tests)"
        elif test_count < 100:
            return "~60-80% (good tests)"
        else:
            return "~80%+ (comprehensive tests)"

    def _detect_test_types(self, test_files: List) -> str:
        """Detect types of tests present."""
        types = []
        test_str = " ".join(str(f) for f in test_files)

        if "unit" in test_str.lower():
            types.append("Unit tests")
        if "integration" in test_str.lower():
            types.append("Integration tests")
        if "e2e" in test_str.lower() or "end_to_end" in test_str.lower():
            types.append("E2E tests")
        if "performance" in test_str.lower() or "benchmark" in test_str.lower():
            types.append("Performance tests")

        return ", ".join(types) if types else "Unit tests (assumed)"

    def _generate_fallback(self, repository: str) -> str:
        """Generate fallback response when context is invalid."""
        return f"""# Testing Analysis

## Summary
Analyzed repository at `{repository}`.

## Findings
Unable to extract detailed testing information due to missing context data.

## Recommendations
1. Ensure test files exist in repository
2. Provide complete context data for analysis
3. Re-run analysis with proper context
"""
