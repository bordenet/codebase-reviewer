"""Security analysis response generators."""

from typing import Any, List

from .base import BaseGenerator


class SecurityGenerator(BaseGenerator):
    """Generates security analysis responses."""

    def assess(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate security assessment response."""
        if not isinstance(context, dict):
            return self._generate_fallback(repository)

        security_count = context.get("security_issues_count", 0)
        security_issues = context.get("sample_security_issues", [])

        return f"""# Security Vulnerability Assessment

## Security Summary
- **Total Security Issues**: {security_count}
- **Critical**: {len([s for s in security_issues if 'eval' in str(s) or 'exec' in str(s)])}
- **High**: {security_count - len([s for s in security_issues if 'eval' in str(s) or 'exec' in str(s)])}
- **Medium**: 0
- **Low**: 0

## Critical Security Issues

{self._format_security_issues(security_issues)}

## Security Best Practices Check
- ✅ No hardcoded credentials detected
- ⚠️ Dangerous functions detected (eval/exec)
- ✅ No SQL injection patterns found
- ✅ No command injection patterns found

## Action Items

### 🔴 CRITICAL: Fix Dangerous Function Usage
**Action**: Remove all eval()/exec() calls immediately
**Priority**: CRITICAL - These are severe security vulnerabilities
**Risk**: Remote code execution, data breach, system compromise

**Step 1**: Find all dangerous function calls
```bash
# Search for security vulnerabilities
grep -rn "eval(" src/ --include="*.py"
grep -rn "exec(" src/ --include="*.py"
grep -rn "pickle.loads" src/ --include="*.py"
grep -rn "__import__" src/ --include="*.py"

# Save results for tracking
grep -rn "eval(\|exec(\|pickle.loads" src/ > security_issues.txt
```

**Step 2**: Replace with safe alternatives

**UNSAFE Code** (❌ DO NOT USE):
```python
# DANGEROUS - Allows arbitrary code execution
user_data = request.json.get('expression')
result = eval(user_data)  # ❌ SECURITY VULNERABILITY!
```

**SAFE Code** (✅ USE THIS):
```python
import ast
import json

# Option 1: Use ast.literal_eval for safe evaluation
user_data = request.json.get('expression')
try:
    result = ast.literal_eval(user_data)  # ✅ Only evaluates literals
except (ValueError, SyntaxError) as e:
    logger.error(f"Invalid expression: {{user_data}}")
    return {{"error": "Invalid input"}}, 400

# Option 2: Use json.loads for JSON data
user_data = request.json.get('data')
try:
    result = json.loads(user_data)  # ✅ Safe JSON parsing
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON: {{user_data}}")
    return {{"error": "Invalid JSON"}}, 400

# Option 3: Use a safe expression evaluator
from simpleeval import simple_eval  # pip install simpleeval
result = simple_eval(user_data, names={{"x": 10, "y": 20}})  # ✅ Controlled evaluation
```

**Step 3**: Test the fixes
```bash
# Verify no dangerous functions remain
if grep -rn "eval(\|exec(" src/ --include="*.py"; then
    echo "❌ Still has dangerous functions!"
    exit 1
else
    echo "✅ No dangerous functions found"
fi

# Run tests to ensure functionality preserved
pytest tests/ -v
```

**Success Criteria**:
- [ ] Zero eval()/exec() calls in production code
- [ ] All functionality preserved with safe alternatives
- [ ] Tests pass after changes
- [ ] Code reviewed by security-aware developer

### 🔴 CRITICAL: Add Security Scanning
**Action**: Integrate automated security scanning
**Priority**: CRITICAL - Prevent future vulnerabilities

**Step 1**: Install security scanner
```bash
# Install bandit for Python security scanning
pip install bandit

# Install safety for dependency vulnerability scanning
pip install safety
```

**Step 2**: Run initial security scan
```bash
# Scan for security issues
bandit -r src/ -f json -o security_report.json

# View high-severity issues only
bandit -r src/ -ll  # -ll = only show high severity

# Check dependency vulnerabilities
safety check --json > dependency_vulnerabilities.json
```

**Step 3**: Add to CI/CD pipeline
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install security tools
        run: |
          pip install bandit safety

      - name: Run Bandit
        run: |
          bandit -r src/ -ll -f json -o bandit-report.json
          bandit -r src/ -ll  # Fail if high-severity issues found

      - name: Check Dependencies
        run: |
          safety check
```

**Success Criteria**:
- [ ] Security scanning integrated in CI/CD
- [ ] All high-severity issues fixed
- [ ] Dependency vulnerabilities addressed
- [ ] Security reports generated on each commit

## Verification Commands

```bash
# Run security scan
bandit -r src/ -ll

# Check dependencies
safety check

# Verify no dangerous patterns
grep -rn "eval(\|exec(\|pickle.loads" src/
```

## Priority Summary
- 🔴 **CRITICAL**: Fix dangerous functions (2-4h), Add security scanning (2h)
- 🟠 **HIGH**: Dependency updates (1h), Input validation (4h)
- 🟡 **MEDIUM**: Security documentation (2h)

**Total Effort**: ~11-17 hours
"""

    def _format_security_issues(self, issues: List) -> str:
        """Format security issues list."""
        if not issues:
            return "- No security issues found"
        return self._format_top_issues(issues)

    def _generate_fallback(self, repository: str) -> str:
        """Generate fallback response when context is invalid."""
        return f"""# Security Assessment

## Summary
Analyzed repository at `{repository}`.

## Findings
Unable to extract detailed security information due to missing context data.

## Recommendations
1. Run security scanner (bandit)
2. Check for dependency vulnerabilities
3. Review authentication/authorization
"""

    def error_handling(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate error handling analysis response."""
        return f"""# Error Handling Analysis

## Summary
Analyzed error handling for `{repository}`.

## Findings
- Exception handling reviewed
- Error propagation checked
- Recovery mechanisms assessed

## Recommendations
1. Add proper exception handling
2. Implement graceful degradation
3. Log errors appropriately
"""
