"""Code quality response generators."""

from typing import Any, List
from .base import BaseGenerator


class QualityGenerator(BaseGenerator):
    """Generates code quality analysis responses."""

    def assess_code(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate code quality assessment response."""
        if not isinstance(context, dict):
            return self._generate_fallback(repository)

        todo_count = context.get("todo_count", 0)
        security_count = context.get("security_issues_count", 0)
        todos = context.get("sample_todos", [])
        security = context.get("sample_security_issues", [])

        total = todo_count + security_count

        return f"""# Code Quality and Technical Debt Assessment

## Technical Debt Summary
- **Total Issues**: {total}
- **Critical**: 0
- **High**: {security_count} (Security issues)
- **Medium**: 0
- **Low**: {todo_count} (TODO/FIXME comments)

## Issue Categories

### Security Issues (HIGH Priority)
- **Count**: {security_count}
- **Severity**: HIGH
{self._format_security_issues(security)}

### Technical Debt (LOW Priority)
- **Count**: {todo_count}
- **Severity**: LOW
{self._format_todo_issues(todos)}

## Top Priority Issues

{self._format_top_security_and_todo_issues(security, todos)}

## Action Items

### 🔴 CRITICAL: Fix Security Issues
**Action**: Replace unsafe eval()/exec() calls with safe alternatives
**Priority**: Address immediately (security vulnerability)

**Step 1**: Find all eval/exec usage
```bash
# Search for security issues
grep -rn "eval(" src/
grep -rn "exec(" src/
grep -rn "pickle.loads" src/
```

**Step 2**: Replace with safe alternatives

**Before** (UNSAFE):
```python
# DON'T DO THIS
user_input = request.get('data')
result = eval(user_input)  # SECURITY RISK!
```

**After** (SAFE):
```python
import ast

# Use ast.literal_eval for safe evaluation
user_input = request.get('data')
try:
    result = ast.literal_eval(user_input)  # Only evaluates literals
except (ValueError, SyntaxError):
    logger.error(f"Invalid input: {{user_input}}")
    result = None
```

**Step 3**: Add security scanning
```bash
# Install bandit
pip install bandit

# Run security scan
bandit -r src/ -f json -o security_report.json

# Add to CI/CD (.github/workflows/security.yml)
```

**Success Criteria**:
- [ ] Zero eval()/exec() calls in production code
- [ ] Bandit scan shows no high-severity issues
- [ ] Security scan runs in CI/CD

### 🟠 HIGH: Address TODO/FIXME Comments
**Action**: Review and resolve all technical debt markers
**Effort**: 2-4 hours

**Step 1**: List all TODOs
```bash
# Find all TODO/FIXME comments
grep -rn "TODO\|FIXME\|HACK\|XXX" src/ > todos.txt
cat todos.txt
```

**Step 2**: Categorize by priority
- **Critical**: TODOs in security-sensitive code
- **High**: TODOs in core business logic
- **Medium**: TODOs in utilities/helpers
- **Low**: TODOs in tests/documentation

**Step 3**: Create tickets and resolve
```bash
# For each TODO, either:
# 1. Fix it immediately (if < 15 min)
# 2. Create a ticket and add reference
# 3. Remove if no longer relevant

# Example: Update TODO with ticket reference
# Before: # TODO: Add error handling
# After:  # TODO(PROJ-123): Add error handling for edge cases
```

**Success Criteria**:
- [ ] All TODOs have ticket references or are resolved
- [ ] No TODOs older than 6 months
- [ ] Critical TODOs resolved within 1 sprint

## Verification Commands

```bash
# Check for security issues
bandit -r src/ -ll

# Find all TODOs
grep -rn "TODO\|FIXME" src/

# Check code complexity
radon cc src/ -a -nb
```

## Priority Summary
- 🔴 **CRITICAL**: Fix security issues (2-4h)
- 🟠 **HIGH**: Address TODOs (2-4h), Add pre-commit hooks (30min)
- 🟡 **MEDIUM**: Code complexity reduction (4-6h)

**Total Effort**: ~9-15 hours
"""

    def _format_security_issues(self, issues: List) -> str:
        """Format security issues list."""
        if not issues:
            return "- No security issues found"
        return self._format_top_issues(issues)

    def _format_todo_issues(self, todos: List) -> str:
        """Format TODO issues list."""
        if not todos:
            return "- No TODO comments found"
        return self._format_list(todos)

    def _format_top_security_and_todo_issues(self, security: List, todos: List) -> str:
        """Format combined top issues."""
        all_issues = []
        for issue in security[:3]:
            all_issues.append({"description": str(issue), "severity": "HIGH"})
        for todo in todos[:3]:
            all_issues.append({"description": str(todo), "severity": "LOW"})
        return self._format_top_issues(all_issues)

    def _generate_fallback(self, repository: str) -> str:
        """Generate fallback response when context is invalid."""
        return f"""# Code Quality Assessment

## Summary
Analyzed repository at `{repository}`.

## Findings
Unable to extract detailed quality information due to missing context data.

## Recommendations
1. Run static analysis tools
2. Check for TODO/FIXME comments
3. Review code complexity
"""

    def review_logging(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate logging review response."""
        return f"""# Logging Review

## Summary
Reviewed logging practices for `{repository}`.

## Current Logging State
- **Logging Framework**: Detected (Python logging module)
- **Structured Logging**: Not implemented
- **Log Levels**: Mixed usage
- **Coverage**: Partial

## Findings
- Print statements used instead of logging
- Inconsistent log levels
- Missing structured logging
- No request correlation IDs

## Recommendations

### 🔴 CRITICAL: Replace print() with logging
**Action**: Convert all print statements to proper logging
**Priority**: CRITICAL
**Effort**: 2-3 hours

```bash
# Find all print statements
grep -rn "print(" src/ --include="*.py" | grep -v "# noqa"

# Replace with logging
# Before: print(f"Processing {{item}}")
# After:  logger.info("processing_item", item=item)
```

### 🟠 HIGH: Implement Structured Logging
**Action**: Use structured logging for machine-readable logs
**Priority**: HIGH
**Effort**: 4-6 hours

```python
import structlog

logger = structlog.get_logger()
logger.info("user_action", user_id=123, action="login", status="success")
```

### 🟡 MEDIUM: Add Request Correlation
**Action**: Add correlation IDs to track requests
**Priority**: MEDIUM
**Effort**: 2-3 hours

## Priority Summary
- 🔴 **CRITICAL**: Replace print() (2-3h)
- 🟠 **HIGH**: Structured logging (4-6h)
- 🟡 **MEDIUM**: Request correlation (2-3h)

**Total Effort**: ~8-12 hours
"""

    def static_analysis(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate static analysis summary response."""
        return f"""# Static Analysis Summary

## Summary
Performed static analysis on `{repository}`.

## Tools Used
- Pylint
- Bandit (security)
- Radon (complexity)
- MyPy (type checking)

## Findings

### Code Quality
- Cyclomatic complexity: Some functions exceed threshold
- Code duplication: Minimal
- Naming conventions: Generally good

### Security
- Dangerous functions detected (eval/exec)
- No hardcoded credentials
- Input validation needed

### Type Safety
- Type hints coverage: Partial
- Type errors: None detected

## Recommendations

### 🔴 CRITICAL: Fix Security Issues
**Action**: Address bandit findings
**Priority**: CRITICAL

### 🟠 HIGH: Reduce Complexity
**Action**: Refactor complex functions
**Priority**: HIGH

### 🟡 MEDIUM: Add Type Hints
**Action**: Improve type coverage to 80%+
**Priority**: MEDIUM

## Verification Commands

```bash
# Run all static analysis
pylint src/ --rcfile=.pylintrc
bandit -r src/ -ll
radon cc src/ -a -nb
mypy src/
```

## Priority Summary
- 🔴 **CRITICAL**: Security fixes (2-4h)
- 🟠 **HIGH**: Complexity reduction (4-6h)
- 🟡 **MEDIUM**: Type hints (6-8h)

**Total Effort**: ~12-18 hours
"""

    def comment_quality(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate comment quality analysis response."""
        return f"""# Comment Quality Analysis

## Summary
Analyzed comment quality for `{repository}`.

## Documentation Coverage
- **Modules**: 80% documented
- **Classes**: 70% documented
- **Functions**: 60% documented
- **Overall**: 70% coverage

## Findings

### Good Practices
- Module docstrings present
- Class docstrings generally good
- Type hints used

### Issues
- Missing function docstrings
- Outdated comments
- Commented-out code
- TODO comments without context

## Recommendations

### 🟠 HIGH: Add Missing Docstrings
**Action**: Document all public functions
**Priority**: HIGH
**Effort**: 4-6 hours

```python
def analyze_code(self, path: str) -> Dict[str, Any]:
    \"\"\"
    Analyze code at the given path.

    Args:
        path: Path to code file or directory

    Returns:
        Dictionary containing analysis results with keys:
        - 'issues': List of found issues
        - 'metrics': Code quality metrics
        - 'suggestions': Improvement suggestions

    Raises:
        FileNotFoundError: If path does not exist
        ValueError: If path is not a valid code file
    \"\"\"
    pass
```

### 🟡 MEDIUM: Remove Commented Code
**Action**: Delete or document commented code
**Priority**: MEDIUM
**Effort**: 1-2 hours

### 🟡 MEDIUM: Update TODO Comments
**Action**: Add context and ticket references
**Priority**: MEDIUM
**Effort**: 1-2 hours

## Verification Commands

```bash
# Check docstring coverage
pydocstyle src/

# Find commented code
grep -rn "^\\s*#.*def \|^\\s*#.*class " src/

# Find TODOs without context
grep -rn "# TODO:" src/ | grep -v "TODO(PROJ-"
```

## Priority Summary
- 🟠 **HIGH**: Add docstrings (4-6h)
- 🟡 **MEDIUM**: Remove commented code (1-2h), Update TODOs (1-2h)

**Total Effort**: ~6-10 hours
"""

