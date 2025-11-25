"""
Mock LLM for generating context-aware simulation responses.

This module provides realistic LLM-like responses based on the context data
provided to each prompt, enabling effective prompt tuning and evaluation.
"""

import json
from typing import Any, Dict, List, Optional


class MockLLM:
    """Generates context-aware responses that simulate real LLM behavior."""

    def __init__(self):
        """Initialize the mock LLM."""
        self.response_generators = {
            "0.1": self._generate_readme_analysis,
            "1.1": self._generate_architecture_validation,
            "1.2": self._generate_dependency_analysis,
            "2.1": self._generate_code_quality,
            "2.2": self._generate_logging_review,
            "3.1": self._generate_setup_validation,
            "3.2": self._generate_testing_review,
            "static_analysis_summary": self._generate_static_analysis,
            "comment_quality": self._generate_comment_quality,
            "security.1": self._generate_security_assessment,
            "security.2": self._generate_error_handling,
            "arch.1": self._generate_call_graph,
            "arch.2": self._generate_git_hotspots,
            "arch.4": self._generate_cohesion_coupling,
            "strategy.2": self._generate_observability_strategy,
            "strategy.3": self._generate_test_strategy,
            "strategy.4": self._generate_tech_debt_roadmap,
            "strategy.5": self._generate_mentorship_guide,
        }

    def generate_response(
        self, prompt_id: str, prompt_text: str, context: Any, repository: str
    ) -> str:
        """
        Generate a context-aware response for the given prompt.

        Args:
            prompt_id: Unique identifier for the prompt
            prompt_text: The full prompt text
            context: Context data provided to the prompt
            repository: Repository path being analyzed

        Returns:
            A realistic, context-aware response
        """
        generator = self.response_generators.get(
            prompt_id, self._generate_generic_response
        )
        return generator(prompt_id, prompt_text, context, repository)

    def _generate_readme_analysis(
        self, prompt_id: str, prompt_text: str, context: Any, repository: str
    ) -> str:
        """Generate README analysis response."""
        if isinstance(context, dict):
            readme_content = context.get("readme_content", "")
            total_docs = context.get("total_docs_found", 0)

            # Extract key claims from README
            claims = []
            if "Python" in readme_content:
                claims.append("Python-based tool")
            if "workflow" in readme_content.lower():
                claims.append("Customizable workflow system")
            if "Web" in readme_content or "web" in readme_content:
                claims.append("Web UI available")
            if "CLI" in readme_content or "command" in readme_content.lower():
                claims.append("Command-line interface")

            return f"""# README Analysis & Claims Extraction

## Summary
Analyzed {total_docs} documentation file(s) for the repository at `{repository}`.
Found comprehensive documentation with clear project description and setup instructions.

## Testable Claims Extracted

{self._format_claims(claims)}

## Architecture Claims
- **Pattern**: {"Modular architecture mentioned" if "modul" in readme_content.lower() else "Not explicitly stated"}
- **Technologies**: {self._extract_technologies(readme_content)}
- **Components**: {self._extract_components(readme_content)}

## Setup Instructions Found
{self._extract_setup_claims(readme_content)}

## Feature Claims
{self._extract_feature_claims(readme_content)}

## Action Items

### 🟡 MEDIUM: Create Architecture Diagram
**Action**: Add visual architecture diagram to improve documentation clarity
**Location**: Create `docs/architecture.md`
**Steps**:
1. Create docs directory if it doesn't exist:
   ```bash
   mkdir -p docs
   ```
2. Add Mermaid diagram showing system components
3. Link from README.md (add after "Architecture" section)

**Code Example** (docs/architecture.md):
```markdown
# Architecture

```mermaid
graph TD
    A[CLI/Web Interface] --> B[Orchestrator]
    B --> C[Documentation Analyzer]
    B --> D[Code Analyzer]
    B --> E[Validation Engine]
    C --> F[Prompt Generator]
    D --> F
    E --> F
```
```

**Success Criteria**:
- [ ] Diagram renders correctly in GitHub
- [ ] All major components shown
- [ ] Linked from README

### 🟠 HIGH: Validate Workflow System
**Action**: Test workflow system functionality
**Commands**:
```bash
# Test default workflow
review-codebase analyze . --workflow default

# Test reviewer_criteria workflow
review-codebase analyze . --workflow reviewer_criteria

# Verify workflow files exist
ls -la src/codebase_reviewer/prompts/workflows/
```

**Success Criteria**:
- [ ] Both workflows execute without errors
- [ ] Prompts generated match workflow definitions
- [ ] All workflow phases complete successfully

### 🟠 HIGH: Test CLI and Web UI
**Action**: Verify both interfaces work correctly
**Commands**:
```bash
# Test CLI
review-codebase --help
review-codebase analyze --help

# Test Web UI
review-codebase web --port 3000
# Then visit http://localhost:3000
```

**Success Criteria**:
- [ ] CLI shows help text
- [ ] Web UI starts without errors
- [ ] Both interfaces can analyze repositories

### 🟡 MEDIUM: Cross-Check Technology Stack
**Action**: Verify documented technologies are actually used
**Commands**:
```bash
# Check for claimed technologies
grep -r "from flask import\|import flask" src/
grep -r "from django import\|import django" src/
grep -r "\.go$" . --include="*.go"
```

**Expected Results**:
- Flask: Should find imports in src/
- Django: Verify if actually used or documentation error
- Go: Should find .go files in cmd/

**Next Steps**: Update README to remove any technologies not actually used

## Validation Priority
- 🔴 **CRITICAL**: None identified
- 🟠 **HIGH**: Verify workflow system (2 hours), Test interfaces (1 hour)
- 🟡 **MEDIUM**: Add architecture diagram (30 min), Validate tech stack (15 min)
- 🟢 **LOW**: Check documentation completeness score
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_architecture_validation(
        self, prompt_id: str, prompt_text: str, context: Any, repository: str
    ) -> str:
        """Generate architecture validation response."""
        if isinstance(context, dict):
            claimed = context.get("claimed_architecture", {})
            actual = context.get("actual_structure", {})
            validation = context.get("validation_results", [])

            claimed_components = claimed.get("components", [])
            actual_packages = actual.get("packages", [])
            frameworks = actual.get("frameworks", [])

            return rf"""# Architecture Validation Report

## Claimed vs. Actual Architecture
- **Claimed Pattern**: {claimed.get('pattern') or 'Not explicitly stated'}
- **Actual Pattern**: Modular package-based architecture
- **Match Status**: ⚠️ Partial - Pattern not explicitly documented

## Component Validation

{self._validate_components(claimed_components, actual_packages)}

## Technology Stack Validation
- **Claimed Technologies**: {', '.join(claimed_components) if claimed_components else 'Not specified'}
- **Actual Frameworks**: {', '.join(frameworks) if frameworks else 'None detected'}
- **Languages Detected**: {self._format_languages(actual.get('languages', []))}

## Package Structure
{self._format_packages(actual_packages)}

## Validation Results
{self._format_validation_results(validation)}

## Action Items

### 🟠 HIGH: Document Actual Architecture Pattern
**Action**: Add explicit architecture pattern documentation
**Location**: README.md (add new "Architecture Pattern" section after line 50)
**Pattern Identified**: Modular Monolith with layered architecture

**Code Example** (README.md):
```markdown
## Architecture Pattern

This project follows a **Modular Monolith** pattern with clear separation of concerns:

- **Presentation Layer**: CLI (`cli.py`) and Web UI (`web.py`)
- **Orchestration Layer**: `orchestrator.py` coordinates analysis workflow
- **Analysis Layer**: Specialized analyzers (`analyzers/` package)
- **Prompt Layer**: Workflow and template management (`prompts/` package)
- **Data Layer**: Models and data structures (`models.py`)

Each module has well-defined interfaces and minimal coupling.
```

**Success Criteria**:
- [ ] Architecture pattern explicitly documented
- [ ] Layer responsibilities clearly defined
- [ ] Matches actual code structure

### 🟠 HIGH: Update Component List
**Action**: Replace generic component names with actual package structure
**Location**: README.md, docs/architecture.md

**Current (Incorrect)**:
- Extensible
- CLI
- Programmatic

**Actual Components** (from code analysis):
- `src/codebase_reviewer/analyzers/` - Analysis engines
- `src/codebase_reviewer/prompts/` - Prompt generation
- `src/codebase_reviewer/tuning/` - Prompt optimization
- `src/codebase_reviewer/cli.py` - Command-line interface
- `src/codebase_reviewer/web.py` - Web interface
- `src/codebase_reviewer/orchestrator.py` - Workflow coordinator

**Commands to verify**:
```bash
# List actual packages
find src/codebase_reviewer -type d -name "__pycache__" -prune -o -type d -print

# Count modules per package
find src/codebase_reviewer/analyzers -name "*.py" | wc -l
find src/codebase_reviewer/prompts -name "*.py" | wc -l
```

### 🟡 MEDIUM: Create Architecture Diagram
**Action**: Add visual diagram showing package relationships
**Location**: Create `docs/architecture.md`

**Mermaid Diagram**:
```mermaid
graph TB
    subgraph "Presentation Layer"
        CLI[cli.py]
        WEB[web.py]
    end

    subgraph "Orchestration"
        ORCH[orchestrator.py]
    end

    subgraph "Analysis Layer"
        DOC[analyzers/documentation.py]
        CODE[analyzers/code.py]
        VAL[analyzers/validation.py]
        LANG[analyzers/language_detector.py]
    end

    subgraph "Prompt Layer"
        WF[prompts/workflow_loader.py]
        TEMP[prompts/templates/]
    end

    CLI --> ORCH
    WEB --> ORCH
    ORCH --> DOC
    ORCH --> CODE
    ORCH --> VAL
    DOC --> WF
    CODE --> WF
    VAL --> WF
```

**Success Criteria**:
- [ ] All major packages shown
- [ ] Dependencies clearly indicated
- [ ] Diagram renders in GitHub

### 🟢 LOW: Add Package Descriptions
**Action**: Document purpose of each package
**Location**: Add docstrings to `__init__.py` files

**Example** (src/codebase_reviewer/analyzers/__init__.py):
```python
\"\"\"
Analysis engines for codebase review.

This package contains specialized analyzers:
- documentation.py: Extract and validate documentation claims
- code.py: Analyze code structure and quality
- validation.py: Cross-check documentation vs implementation
- language_detector.py: Detect languages and frameworks
- dependency_parser.py: Parse dependency files
- quality_checker.py: Assess code quality metrics
\"\"\"
```

## Validation Commands

```bash
# Verify package structure matches documentation
tree src/codebase_reviewer -L 2

# Check for undocumented packages
find src/codebase_reviewer -name "__init__.py" -exec grep -L 'docstring' {{}} \\;

# Verify all claimed components exist
for component in analyzers prompts tuning; do
    [ -d "src/codebase_reviewer/$component" ] && echo "✓ $component" || echo "✗ $component"
done
```

## Priority Summary
- 🔴 **CRITICAL**: None
- 🟠 **HIGH**: Document architecture pattern (1 hour), Update component list (30 min)
- 🟡 **MEDIUM**: Create architecture diagram (45 min)
- 🟢 **LOW**: Add package descriptions (30 min)

**Total Effort**: ~3 hours
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_code_quality(
        self, prompt_id: str, prompt_text: str, context: Any, repository: str
    ) -> str:
        """Generate code quality assessment response."""
        if isinstance(context, dict):
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

### 🟡 MEDIUM: Add Pre-Commit Hooks
**Action**: Prevent security anti-patterns from being committed
**Effort**: 30 minutes

**Step 1**: Install pre-commit
```bash
pip install pre-commit
```

**Step 2**: Create .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-ll', '-i']  # Low severity, ignore info

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  - repo: local
    hooks:
      - id: no-eval
        name: Prevent eval/exec
        entry: 'eval\(|exec\('
        language: pygrep
        types: [python]
```

**Step 3**: Install hooks
```bash
pre-commit install
pre-commit run --all-files  # Test on existing code
```

**Success Criteria**:
- [ ] Pre-commit hooks installed
- [ ] Blocks commits with eval/exec
- [ ] Runs security scan on every commit

### 🟡 MEDIUM: Establish Technical Debt Policy
**Action**: Create policy for managing technical debt
**Location**: Create `docs/technical-debt-policy.md`

**Policy Template**:
```markdown
# Technical Debt Policy

## TODO Comment Requirements
- Must include ticket reference: `TODO(PROJ-123): Description`
- Must include estimated effort: `TODO(2h): Description`
- Must be reviewed in sprint planning

## Security Anti-Patterns
- **NEVER** use eval()/exec() on user input
- **NEVER** use pickle.loads() on untrusted data
- **ALWAYS** validate and sanitize user input
- **ALWAYS** use parameterized queries for SQL

## Code Review Checklist
- [ ] No new eval/exec calls
- [ ] No hardcoded secrets/passwords
- [ ] All TODOs have ticket references
- [ ] Security scan passes
```

**Success Criteria**:
- [ ] Policy documented and reviewed by team
- [ ] Added to onboarding materials
- [ ] Enforced in code reviews

## Verification Commands

```bash
# Check security issues resolved
bandit -r src/ -ll  # Should show 0 high/medium issues

# Check TODO policy compliance
grep -rn "TODO" src/ | grep -v "TODO(" | wc -l  # Should be 0

# Verify pre-commit hooks
pre-commit run --all-files  # Should pass
```

## Priority Summary
- 🔴 **CRITICAL**: Fix security issues (4 hours) - **DO IMMEDIATELY**
- 🟠 **HIGH**: Address TODOs (2-4 hours) - **This sprint**
- 🟡 **MEDIUM**: Add pre-commit hooks (30 min), Create policy (1 hour) - **Next sprint**
- 🟢 **LOW**: None

**Total Effort**: ~8 hours
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    # Helper methods for formatting
    def _format_claims(self, claims: List[str]) -> str:
        """Format claims as numbered list."""
        if not claims:
            return "- No specific claims extracted"
        return "\n".join(f"{i+1}. {claim}" for i, claim in enumerate(claims))

    def _extract_technologies(self, content: str) -> str:
        """Extract technology mentions from content."""
        techs = []
        tech_keywords = ["Python", "Go", "Flask", "Django", "TypeScript", "JavaScript"]
        for tech in tech_keywords:
            if tech in content:
                techs.append(tech)
        return ", ".join(techs) if techs else "Not specified"

    def _extract_components(self, content: str) -> str:
        """Extract component mentions."""
        # Simple extraction - look for capitalized words that might be components
        return "See detailed analysis in architecture validation"

    def _extract_setup_claims(self, content: str) -> str:
        """Extract setup instruction claims."""
        if "venv" in content.lower() or "virtualenv" in content.lower():
            return "- Virtual environment setup documented\n- Dependency installation via pip"
        return "- Setup instructions present"

    def _extract_feature_claims(self, content: str) -> str:
        """Extract feature claims."""
        features = []
        if "analyz" in content.lower():
            features.append("Code analysis")
        if "workflow" in content.lower():
            features.append("Workflow system")
        if "web" in content.lower():
            features.append("Web interface")
        return (
            "\n".join(f"- {f}" for f in features) if features else "- See documentation"
        )

    def _validate_components(self, claimed: List[str], actual: List[str]) -> str:
        """Validate claimed components against actual packages."""
        if not claimed:
            return "- No components explicitly claimed in documentation"

        result = []
        for component in claimed:
            # Simple matching - check if component name appears in any package
            found = any(component.lower() in pkg.lower() for pkg in actual)
            status = "✅ Found" if found else "❌ Missing"
            result.append(f"- **{component}**: {status}")
        return "\n".join(result)

    def _format_languages(self, languages: List[Dict]) -> str:
        """Format language list."""
        if not languages:
            return "None detected"
        return ", ".join(
            f"{lang['name']} ({lang['percentage']:.1f}%)" for lang in languages[:3]
        )

    def _format_packages(self, packages: List[str]) -> str:
        """Format package list."""
        if not packages:
            return "- No packages found"
        return "\n".join(f"- `{pkg}`" for pkg in packages)

    def _format_validation_results(self, results: List[Dict]) -> str:
        """Format validation results."""
        if not results:
            return "- No validation issues found"
        return "\n".join(
            f"- **{r.get('status', 'unknown').upper()}**: {r.get('evidence', 'N/A')}"
            for r in results
        )

    def _format_security_issues(self, issues: List[Dict]) -> str:
        """Format security issues."""
        if not issues:
            return "- No security issues detected"
        return "\n".join(
            f"- {i+1}. {issue.get('description', 'Unknown issue')}"
            for i, issue in enumerate(issues)
        )

    def _format_todo_issues(self, todos: List[Dict]) -> str:
        """Format TODO issues."""
        if not todos:
            return "- No TODO comments found"
        return "\n".join(
            f"- {i+1}. {todo.get('title', 'Unknown')} - {todo.get('description', 'N/A')[:50]}"
            for i, todo in enumerate(todos[:5])
        )

    def _format_top_security_and_todo_issues(
        self, security: List[Dict], todos: List[Dict]
    ) -> str:
        """Format top priority security and TODO issues."""
        issues = []
        for i, sec in enumerate(security[:3], 1):
            issues.append(
                f"{i}. **Security**: {sec.get('description', 'Unknown')} (HIGH)"
            )
        return "\n".join(issues) if issues else "- No critical issues found"

    def _generate_generic_response(
        self, prompt_id: str, prompt_text: str, context: Any, repository: str
    ) -> str:
        """Generate a generic response when no specific generator exists."""
        return f"""# Analysis Response: {prompt_id}

## Summary
Analyzed repository at `{repository}` for prompt {prompt_id}.

## Context Provided
{self._format_context(context)}

## Analysis
This prompt requires manual implementation of a specific response generator.
The context data is available but not yet processed by a specialized handler.

## Recommendations
- Implement specific response generator for prompt {prompt_id}
- Use provided context data to generate actionable insights
- Follow the deliverable format specified in the prompt

---
*Note: This is a generic response. Implement a specific generator in mock_llm.py for better results.*
"""

    def _format_context(self, context: Any) -> str:
        """Format context for display."""
        if isinstance(context, dict):
            return f"```json\n{json.dumps(context, indent=2)[:500]}...\n```"
        return f"```\n{str(context)[:500]}...\n```"

    # Placeholder generators for other prompt types
    def _generate_dependency_analysis(
        self, prompt_id, prompt_text, context, repository
    ):
        """Generate dependency analysis response."""
        if isinstance(context, dict):
            deps = context.get("dependencies", [])
            dep_count = context.get("dependencies_count", 0)
            outdated = context.get("outdated_dependencies", [])

            return f"""# Dependency Analysis and Health Check

## Dependency Summary
- **Total Dependencies**: {dep_count}
- **Outdated**: {len(outdated)}
- **Security Vulnerabilities**: 0 (requires security scan)

## Dependency Health
{self._format_dependencies(deps[:10])}

## Outdated Dependencies
{self._format_outdated_deps(outdated)}

## Action Items

### 🔴 CRITICAL: Run Security Audit
**Action**: Scan dependencies for known vulnerabilities
**Priority**: CRITICAL - Vulnerable dependencies are attack vectors

**Step 1**: Install security audit tools
```bash
# For Python projects
pip install pip-audit safety

# For Node.js projects
npm install -g npm-audit

# For Go projects
go install golang.org/x/vuln/cmd/govulncheck@latest
```

**Step 2**: Run security scans
```bash
# Python: Check for vulnerabilities
pip-audit --desc
safety check --full-report

# Node.js: Check for vulnerabilities
npm audit
npm audit --json > npm-audit.json

# Go: Check for vulnerabilities
govulncheck ./...

# Generate report
pip-audit --format json > security-audit.json
```

**Step 3**: Fix critical vulnerabilities immediately
```bash
# Python: Update vulnerable packages
pip install --upgrade <package-name>

# Node.js: Auto-fix vulnerabilities
npm audit fix
npm audit fix --force  # For breaking changes

# Verify fixes
pip-audit  # Should show 0 vulnerabilities
```

**Success Criteria**:
- [ ] Zero critical/high severity vulnerabilities
- [ ] All medium severity vulnerabilities reviewed
- [ ] Security audit runs in CI/CD
- [ ] Vulnerability report generated

### 🟠 HIGH: Update Outdated Dependencies
**Action**: Update {len(outdated)} outdated dependencies
**Priority**: HIGH - Outdated packages miss security patches

**Step 1**: List all outdated dependencies
```bash
# Python: Check for updates
pip list --outdated
pip-review --local --interactive

# Node.js: Check for updates
npm outdated
npx npm-check-updates

# Go: Check for updates
go list -u -m all
```

**Step 2**: Update dependencies safely
```bash
# Python: Update one at a time
pip install --upgrade <package-name>
pytest  # Run tests after each update

# Or use pip-review for interactive updates
pip install pip-review
pip-review --local --interactive

# Node.js: Update dependencies
npx npm-check-updates -u
npm install
npm test

# Go: Update dependencies
go get -u ./...
go mod tidy
go test ./...
```

**Step 3**: Update requirements files
```bash
# Python: Freeze updated versions
pip freeze > requirements.txt

# Or use pip-compile for better control
pip install pip-tools
pip-compile requirements.in > requirements.txt

# Node.js: package.json already updated
# Commit package.json and package-lock.json

# Go: go.mod already updated
# Commit go.mod and go.sum
```

**Success Criteria**:
- [ ] All dependencies updated to latest stable versions
- [ ] All tests pass after updates
- [ ] No breaking changes introduced
- [ ] Requirements files updated and committed

### 🟠 HIGH: Pin Dependencies for Production
**Action**: Lock dependency versions for reproducible builds
**Location**: Update requirements.txt / package-lock.json

**Python Approach**:
```bash
# Create requirements.in with loose versions
cat > requirements.in << 'EOF'
flask>=2.3.0
pyyaml>=6.0
click>=8.1.0
EOF

# Generate pinned requirements.txt
pip-compile requirements.in > requirements.txt

# This creates:
# flask==2.3.2
# pyyaml==6.0.1
# click==8.1.3
# ... (with all transitive dependencies pinned)
```

**Node.js Approach**:
```bash
# Use package-lock.json (automatically created)
npm install

# Or use exact versions in package.json
npm config set save-exact true
npm install <package>

# Verify lock file
npm ci  # Install from lock file exactly
```

**Go Approach**:
```bash
# go.mod and go.sum already provide pinning
go mod download
go mod verify
```

### 🟡 MEDIUM: Remove Unused Dependencies
**Action**: Clean up unused packages
**Effort**: 1-2 hours

**Step 1**: Find unused dependencies
```bash
# Python: Use pip-autoremove
pip install pip-autoremove
pip-autoremove <package> --list

# Or use pipdeptree to visualize
pip install pipdeptree
pipdeptree --warn silence

# Node.js: Use depcheck
npx depcheck

# Go: Use go mod tidy
go mod tidy
```

**Step 2**: Remove unused packages
```bash
# Python: Remove package
pip uninstall <package>
pip freeze > requirements.txt

# Node.js: Remove package
npm uninstall <package>

# Go: Automatic with go mod tidy
go mod tidy
```

**Success Criteria**:
- [ ] All unused dependencies removed
- [ ] Application still works correctly
- [ ] Build size reduced
- [ ] Faster installation time

### 🟡 MEDIUM: Add Automated Dependency Updates
**Action**: Set up Dependabot or Renovate
**Location**: Create `.github/dependabot.yml`

**Configuration**:
```yaml
# .github/dependabot.yml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "your-team"
    labels:
      - "dependencies"
      - "python"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Alternative: Renovate**:
```json
// renovate.json
{{
  "extends": ["config:base"],
  "packageRules": [
    {{
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    }}
  ],
  "schedule": ["before 3am on Monday"]
}}
```

## Verification Commands

```bash
# Check for vulnerabilities
pip-audit
safety check

# Check for outdated packages
pip list --outdated

# Verify pinned versions
pip install -r requirements.txt
pip freeze | diff - requirements.txt  # Should be identical

# Test installation from scratch
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
pytest
```

## Priority Summary
- 🔴 **CRITICAL**: Run security audit (30 min), Fix vulnerabilities (2-4 hours) - **DO TODAY**
- 🟠 **HIGH**: Update outdated deps (2 hours), Pin dependencies (1 hour) - **This week**
- 🟡 **MEDIUM**: Remove unused deps (1 hour), Add Dependabot (30 min) - **This month**
- 🟢 **LOW**: Document dependency policy

**Total Effort**: ~7 hours for critical/high priority items

## Risk Assessment
- 🔴 **High Risk**: {len([d for d in outdated if 'major' in str(d)])} major version updates needed
- 🟠 **Medium Risk**: {len(outdated)} outdated dependencies may have security issues
- 🟢 **Low Risk**: {"Most dependencies appear current" if len(outdated) < 5 else "Dependency hygiene needs improvement"}
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_testing_review(self, prompt_id, prompt_text, context, repository):
        """Generate testing strategy review response."""
        if isinstance(context, dict):
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

### 🟠 HIGH: Add Coverage Reporting
**Action**: Set up automated coverage tracking
**Location**: Add `.coveragerc` and update CI/CD

**Step 1**: Create coverage configuration
```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */test_*.py
    */__pycache__/*
    */venv/*

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov
```

**Step 2**: Add coverage badge to README
```markdown
# Add to README.md
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](htmlcov/index.html)
```

**Step 3**: Add to CI/CD pipeline
```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install -e .[dev]
      - run: pytest --cov=src --cov-report=xml --cov-fail-under=80
      - uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### 🟡 MEDIUM: Add Integration Tests
**Action**: Create integration test suite
**Location**: Create `tests/integration/` directory

**Test Structure**:
```bash
tests/
├── unit/              # Fast, isolated tests
│   ├── test_analyzers.py
│   ├── test_models.py
│   └── test_utils.py
├── integration/       # Multi-component tests
│   ├── test_workflow.py
│   ├── test_cli.py
│   └── test_end_to_end.py
└── fixtures/          # Test data
    └── sample_repos/
```

**Example Integration Test**:
```python
# tests/integration/test_workflow.py
import pytest
from codebase_reviewer.orchestrator import AnalysisOrchestrator

def test_full_analysis_workflow(tmp_path):
    # Create sample repository
    (tmp_path / "README.md").write_text("# Test Project")
    (tmp_path / "src" / "main.py").write_text("print('hello')")

    # Run full analysis
    orchestrator = AnalysisOrchestrator()
    result = orchestrator.analyze(str(tmp_path))

    # Verify all phases completed
    assert result.documentation_analysis is not None
    assert result.code_analysis is not None
    assert result.validation_results is not None
    assert len(result.prompts) > 0
```

### 🟡 MEDIUM: Add Performance Tests
**Action**: Test performance of critical operations
**Location**: Create `tests/performance/` directory

**Example Performance Test**:
```python
# tests/performance/test_analyzer_performance.py
import pytest
import time
from codebase_reviewer.analyzers.code import CodeAnalyzer

def test_large_repository_analysis_performance(large_test_repo):
    analyzer = CodeAnalyzer()

    start = time.time()
    result = analyzer.analyze(large_test_repo)
    duration = time.time() - start

    # Should complete within 30 seconds for 1000 files
    assert duration < 30.0
    assert result is not None

@pytest.mark.benchmark
def test_file_parsing_performance(benchmark):
    analyzer = CodeAnalyzer()

    # Benchmark should complete in <100ms
    result = benchmark(analyzer.parse_file, "sample.py")
    assert result is not None
```

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

# Run performance tests
pytest tests/performance/ -v --benchmark-only

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
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_security_assessment(
        self, prompt_id, prompt_text, context, repository
    ):
        """Generate security assessment response."""
        if isinstance(context, dict):
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
          safety check --json

      - name: Upload Security Reports
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: security-reports
          path: |
            bandit-report.json
            dependency_vulnerabilities.json
```

**Step 4**: Configure bandit
```yaml
# .bandit
exclude_dirs:
  - /tests/
  - /venv/
  - /.venv/

tests:
  - B102  # exec_used
  - B307  # eval_used
  - B301  # pickle
  - B303  # insecure_hash (MD5, SHA1)
  - B201  # flask_debug_true
  - B501  # request_with_no_cert_validation
```

### 🟠 HIGH: Add Pre-Commit Security Hooks
**Action**: Block dangerous code before it's committed
**Location**: Create `.pre-commit-config.yaml`

**Configuration**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-ll', '-i']  # Low severity, ignore info
        files: \\.py$

  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.1
    hooks:
      - id: python-safety-dependencies-check

  - repo: local
    hooks:
      - id: block-dangerous-functions
        name: Block eval/exec/pickle
        entry: 'eval\\(|exec\\(|pickle\\.loads'
        language: pygrep
        types: [python]
        exclude: ^tests/
```

**Installation**:
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Test on all files
pre-commit run --all-files
```

### 🟠 HIGH: Create Security Code Review Checklist
**Action**: Standardize security reviews
**Location**: Create `docs/security-checklist.md`

**Checklist Template**:
```markdown
# Security Code Review Checklist

## Input Validation
- [ ] All user input is validated and sanitized
- [ ] No eval()/exec() on user input
- [ ] SQL queries use parameterized statements
- [ ] File paths are validated (no path traversal)
- [ ] File uploads have type/size restrictions

## Authentication & Authorization
- [ ] Authentication required for sensitive operations
- [ ] Authorization checks before data access
- [ ] No hardcoded credentials
- [ ] Secrets stored in environment variables or vault

## Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit (HTTPS)
- [ ] No sensitive data in logs
- [ ] PII handled according to privacy policy

## Dependencies
- [ ] All dependencies up to date
- [ ] No known vulnerabilities (safety check passes)
- [ ] Dependencies from trusted sources only

## Error Handling
- [ ] No sensitive info in error messages
- [ ] Errors logged securely
- [ ] Graceful degradation on errors

## Code Quality
- [ ] Bandit scan passes
- [ ] No TODO comments about security
- [ ] Security tests added for new features
```

### 🟡 MEDIUM: Dependency Vulnerability Scanning
**Action**: Regularly scan dependencies for vulnerabilities
**Schedule**: Weekly automated scans

**Setup**:
```bash
# Add to package.json or requirements.txt
# requirements-dev.txt
safety==2.3.5
pip-audit==2.6.1

# Run scans
safety check --full-report
pip-audit --desc

# Add to cron or CI/CD
# .github/workflows/dependency-scan.yml (runs weekly)
```

### 🟡 MEDIUM: Security Training
**Action**: Train team on secure coding practices
**Resources**:
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Python Security Best Practices
- Secure Code Review Guidelines

**Training Plan**:
1. **Week 1**: OWASP Top 10 overview
2. **Week 2**: Input validation and injection prevention
3. **Week 3**: Authentication and authorization
4. **Week 4**: Secure dependency management

## Verification Commands

```bash
# Verify no dangerous functions
grep -rn "eval(\|exec(" src/ --include="*.py" && echo "❌ FAIL" || echo "✅ PASS"

# Run security scan
bandit -r src/ -ll

# Check dependencies
safety check

# Verify pre-commit hooks
pre-commit run --all-files

# Run security tests
pytest tests/security/ -v
```

## Priority Summary
- 🔴 **CRITICAL**: Fix eval/exec usage (4 hours), Add security scanning (2 hours) - **DO IMMEDIATELY**
- 🟠 **HIGH**: Add pre-commit hooks (1 hour), Create security checklist (1 hour) - **This week**
- 🟡 **MEDIUM**: Dependency scanning (30 min), Security training (ongoing) - **This month**
- 🟢 **LOW**: Security documentation, Compliance audit

**Total Effort**: ~9 hours for critical/high priority items

## Compliance Notes
- ✅ Ensure compliance with OWASP Top 10
- ✅ Consider SOC 2 / ISO 27001 requirements if applicable
- ✅ GDPR compliance for PII handling
- ✅ Regular security audits (quarterly recommended)
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_test_strategy(self, prompt_id, prompt_text, context, repository):
        """Generate test strategy response."""
        return self._generate_testing_review(
            prompt_id, prompt_text, context, repository
        )

    # Helper methods for new generators
    def _format_dependencies(self, deps: List) -> str:
        """Format dependency list."""
        if not deps:
            return "- No dependencies found"
        return "\n".join(f"- {dep}" for dep in deps[:10])

    def _format_outdated_deps(self, outdated: List) -> str:
        """Format outdated dependencies."""
        if not outdated:
            return "✅ All dependencies are up to date"
        return "\n".join(f"- {dep}" for dep in outdated[:5])

    def _format_test_files(self, test_files: List[str]) -> str:
        """Format test file list."""
        if not test_files:
            return "- No test files found"
        return "\n".join(f"- `{tf}`" for tf in test_files[:10])

    def _estimate_coverage(self, test_count: int) -> str:
        """Estimate test coverage based on test file count."""
        if test_count == 0:
            return "0% (no tests)"
        elif test_count < 5:
            return "Low (~20-40%)"
        elif test_count < 10:
            return "Moderate (~40-60%)"
        else:
            return "Good (~60-80%)"

    def _detect_test_types(self, test_files: List[str]) -> str:
        """Detect test types from file names."""
        types = set()
        for tf in test_files:
            if "integration" in tf.lower():
                types.add("Integration")
            elif "e2e" in tf.lower() or "end_to_end" in tf.lower():
                types.add("End-to-End")
            else:
                types.add("Unit")
        return ", ".join(types) if types else "Unit (assumed)"

    # Remaining placeholder generators
    def _generate_call_graph(self, prompt_id, prompt_text, context, repository):
        """Generate call graph analysis response."""
        if isinstance(context, dict):
            total_files = context.get("total_python_files", 0)
            analyzed = context.get("files_analyzed", 0)
            internal_deps = context.get("internal_dependencies", {})
            most_imported = context.get("most_imported_internal", [])

            return f"""# Call Graph & Dependency Tracing

## Analysis Summary
- **Total Python Files**: {total_files}
- **Files Analyzed**: {analyzed}
- **Internal Dependencies Mapped**: {len(internal_deps)}

## Critical Execution Paths

### Main Entry Points
{self._format_entry_points(internal_deps)}

## Most Imported Modules (Dependency Hubs)
{self._format_most_imported(most_imported)}

## Dependency Map

### High-Fan-In Modules (Many Dependents)
{self._format_high_fan_in(most_imported[:5])}

### Sample Dependencies
{self._format_sample_dependencies(internal_deps)}

## Coupling Analysis
- **Tightly Coupled**: `codebase_reviewer.models` (imported by {most_imported[0]['count'] if most_imported else 0} modules)
- **Loosely Coupled**: Analyzer modules (focused responsibilities)

## Action Items

### 🔴 CRITICAL: Detect and Fix Circular Dependencies
**Action**: Find and eliminate circular import dependencies
**Priority**: CRITICAL - Circular dependencies cause import errors and tight coupling
**Effort**: 3-4 hours

**Step 1**: Install dependency analysis tools
```bash
pip install pydeps
pip install graphviz  # Required for visualization
```

**Step 2**: Generate dependency graph
```bash
# Create full dependency graph
pydeps src/codebase_reviewer --max-bacon=2 -o dependencies.svg

# Find circular dependencies
pydeps src/codebase_reviewer --show-cycles

# Export to JSON for analysis
pydeps src/codebase_reviewer --format json > deps.json
```

**Step 3**: Fix circular dependencies

**Before** (❌ Circular dependency):
```python
# File: models.py
from codebase_reviewer.analyzer import analyze_file

class CodeModel:
    def process(self):
        return analyze_file(self.path)

# File: analyzer.py
from codebase_reviewer.models import CodeModel  # ❌ Circular!

def analyze_file(path):
    model = CodeModel(path)
    return model.data
```

**After** (✅ Dependency injection):
```python
# File: models.py
class CodeModel:
    def process(self, analyzer_func):  # ✅ Inject dependency
        return analyzer_func(self.path)

# File: analyzer.py
# No import of models needed!

def analyze_file(path):
    # Work with path directly
    return parse_and_analyze(path)

# File: main.py
from codebase_reviewer.models import CodeModel
from codebase_reviewer.analyzer import analyze_file

model = CodeModel(path)
result = model.process(analyze_file)  # Inject at runtime
```

**Success Criteria**:
- [ ] Zero circular dependencies (run `pydeps --show-cycles`)
- [ ] Dependency graph generated
- [ ] All imports work without errors

### 🟠 HIGH: Reduce Coupling to High-Fan-In Modules
**Action**: Break up modules with too many dependents
**Priority**: HIGH - Reduces blast radius of changes
**Effort**: 6-8 hours

**Step 1**: Identify high-fan-in modules
```bash
# Find modules imported by many others
pydeps src/codebase_reviewer --max-bacon=1 | grep "imported by"

# Count imports per module
grep -r "^from codebase_reviewer" src/ --include="*.py" | \\
    cut -d: -f2 | sort | uniq -c | sort -rn | head -10
```

**Step 2**: Split large modules

**Example: Split models.py into focused modules**:
```bash
# Before: One large models.py
src/codebase_reviewer/models.py  # 500 lines, 20+ classes

# After: Split by domain
src/codebase_reviewer/models/
    __init__.py           # Re-export for backward compatibility
    analysis_models.py    # Analysis-related models
    workflow_models.py    # Workflow-related models
    report_models.py      # Report-related models
```

**Create `models/__init__.py` for backward compatibility**:
```python
'''Models package.

Maintains backward compatibility while organizing models by domain.
'''

# Re-export all models for backward compatibility
from codebase_reviewer.models.analysis_models import (
    AnalysisResult,
    CodeMetrics,
)
from codebase_reviewer.models.workflow_models import (
    Workflow,
    WorkflowStep,
)
from codebase_reviewer.models.report_models import (
    Report,
    ReportSection,
)

__all__ = [
    'AnalysisResult',
    'CodeMetrics',
    'Workflow',
    'WorkflowStep',
    'Report',
    'ReportSection',
]
```

**Step 3**: Update imports gradually
```bash
# Find all imports of the old module
grep -r "from codebase_reviewer.models import" src/ --include="*.py"

# Update to new structure (can be done incrementally)
# Old: from codebase_reviewer.models import AnalysisResult
# New: from codebase_reviewer.models.analysis_models import AnalysisResult
# Or keep old import (works via __init__.py)
```

**Success Criteria**:
- [ ] No module imported by >10 other modules
- [ ] Large modules split into focused components
- [ ] All tests still pass

### 🟠 HIGH: Document Critical Execution Paths
**Action**: Create architecture diagrams showing main flows
**Priority**: HIGH - Essential for onboarding and maintenance
**Effort**: 3-4 hours

**Step 1**: Identify critical paths
```bash
# Find entry points
grep -r "if __name__ == '__main__'" src/ --include="*.py"
grep -r "@cli.command" src/ --include="*.py"
grep -r "def main" src/ --include="*.py"
```

**Step 2**: Create flow diagrams

**Create `docs/architecture/execution-flows.md`**:
```markdown
# Critical Execution Paths

## 1. CLI Review Flow

\`\`\`mermaid
graph TD
    A[CLI Entry] --> B[Load Workflow]
    B --> C[Initialize Analyzers]
    C --> D[Run Analysis]
    D --> E[Generate Report]
    E --> F[Save Output]

    D --> D1[Phase 0: README]
    D --> D2[Phase 1: Architecture]
    D --> D3[Phase 2: Code Quality]
    D --> D4[Phase 3: Testing]
\`\`\`

## 2. Analysis Pipeline

\`\`\`mermaid
sequenceDiagram
    participant CLI
    participant Workflow
    participant Analyzer
    participant LLM
    participant Report

    CLI->>Workflow: load_workflow()
    Workflow->>Analyzer: initialize()
    CLI->>Analyzer: analyze_repository()
    Analyzer->>LLM: generate_response()
    LLM-->>Analyzer: response
    Analyzer->>Report: add_section()
    Report-->>CLI: final_report
\`\`\`
```

**Step 3**: Generate call graphs for key functions
```bash
# Generate call graph for main entry point
pydeps src/codebase_reviewer/cli.py --only codebase_reviewer -o cli_callgraph.svg

# Generate for core analyzer
pydeps src/codebase_reviewer/analyzer.py --only codebase_reviewer -o analyzer_callgraph.svg
```

**Success Criteria**:
- [ ] All entry points documented
- [ ] Flow diagrams created
- [ ] Call graphs generated
- [ ] Documentation reviewed by team

### 🟡 MEDIUM: Implement Dependency Injection
**Action**: Reduce tight coupling through DI
**Priority**: MEDIUM - Improves testability and flexibility
**Effort**: 8-12 hours

**Step 1**: Identify tightly coupled components
```bash
# Find direct instantiation of dependencies
grep -r "= [A-Z][a-zA-Z]*(" src/ --include="*.py" | grep -v "test"
```

**Step 2**: Refactor to use dependency injection

**Before** (❌ Tight coupling):
```python
class Analyzer:
    def __init__(self, repo_path):
        self.llm = OpenAIClient()  # ❌ Hard-coded dependency
        self.parser = CodeParser()  # ❌ Hard-coded dependency

    def analyze(self):
        code = self.parser.parse(self.repo_path)
        return self.llm.analyze(code)
```

**After** (✅ Dependency injection):
```python
class Analyzer:
    def __init__(self, repo_path, llm_client=None, parser=None):
        self.llm = llm_client or OpenAIClient()  # ✅ Injectable
        self.parser = parser or CodeParser()      # ✅ Injectable

    def analyze(self):
        code = self.parser.parse(self.repo_path)
        return self.llm.analyze(code)

# Usage in production
analyzer = Analyzer('/path', llm_client=OpenAIClient())

# Usage in tests
mock_llm = MockLLM()
mock_parser = MockParser()
analyzer = Analyzer('/path', llm_client=mock_llm, parser=mock_parser)
```

**Step 3**: Consider using a DI framework for complex cases
```bash
pip install dependency-injector
```

```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    llm_client = providers.Singleton(
        OpenAIClient,
        api_key=config.api_key,
    )

    parser = providers.Factory(CodeParser)

    analyzer = providers.Factory(
        Analyzer,
        llm_client=llm_client,
        parser=parser,
    )
```

**Success Criteria**:
- [ ] Core dependencies injectable
- [ ] Tests use mock dependencies
- [ ] No hard-coded instantiation in core logic

## Verification Commands

```bash
# Check for circular dependencies
pydeps src/codebase_reviewer --show-cycles && echo "❌ Circular deps found" || echo "✅ No circular deps"

# Generate dependency graph
pydeps src/codebase_reviewer -o deps.svg && echo "✅ Graph generated"

# Count imports per module
grep -r "^from codebase_reviewer" src/ --include="*.py" | \\
    cut -d: -f2 | cut -d' ' -f2 | sort | uniq -c | sort -rn | head -5

# Visualize specific module
pydeps src/codebase_reviewer/cli.py --only codebase_reviewer
```

## Priority Summary
- 🔴 **CRITICAL**: Fix circular dependencies (3-4 hours) - **DO IMMEDIATELY**
- 🟠 **HIGH**: Reduce coupling (6-8 hours), Document flows (3-4 hours) - **This sprint**
- 🟡 **MEDIUM**: Dependency injection (8-12 hours) - **Next sprint**

**Total Effort**: ~12-16 hours for critical/high priority items

## Risk Assessment
- **High Risk**: Changes to `codebase_reviewer.models` affect {most_imported[0]['count'] if most_imported else 0}+ modules
- **Medium Risk**: Workflow loader changes impact multiple components
- **Low Risk**: Analyzer modules are well-isolated
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_git_hotspots(self, prompt_id, prompt_text, context, repository):
        """Generate git hotspots analysis response."""
        if isinstance(context, dict):
            total_commits = context.get("total_commits_analyzed", 0)
            hotspots = context.get("hotspot_files", [])
            bug_fixes = context.get("bug_fix_commit_count", 0)
            refactors = context.get("refactor_commit_count", 0)

            return f"""# Git Hotspots & Change Analysis

## Analysis Summary
- **Total Commits Analyzed**: {total_commits}
- **Bug Fix Commits**: {bug_fixes}
- **Refactor Commits**: {refactors}

## High-Churn Files (Top 10)
{self._format_hotspots(hotspots[:10])}

## Change Pattern Analysis
- **Bug Fix Rate**: {(bug_fixes/total_commits*100) if total_commits > 0 else 0:.1f}% of commits
- **Refactor Rate**: {(refactors/total_commits*100) if total_commits > 0 else 0:.1f}% of commits
- **Feature Development**: {((total_commits-bug_fixes-refactors)/total_commits*100) if total_commits > 0 else 0:.1f}% of commits

## Hotspot Risk Assessment

### Critical Hotspots (>10 changes)
{self._format_critical_hotspots(hotspots)}

### Moderate Hotspots (5-10 changes)
{self._format_moderate_hotspots(hotspots)}

## Action Items

### 🔴 CRITICAL: Refactor Top Hotspot Files
**Action**: Break down high-churn files to reduce change frequency
**Priority**: CRITICAL - High churn indicates design issues
**Effort**: 8-12 hours per file

**Step 1**: Analyze why files change frequently
```bash
# Get detailed change history for top hotspot
git log --follow --oneline {hotspots[0]['file'] if hotspots else 'FILE'} | head -20

# See what types of changes are made
git log --follow -p {hotspots[0]['file'] if hotspots else 'FILE'} | grep "^+" | head -50

# Find commit messages for patterns
git log --follow --format="%s" {hotspots[0]['file'] if hotspots else 'FILE'} | \\
    grep -i "fix\\|bug\\|refactor" | wc -l
```

**Step 2**: Identify refactoring opportunities

**Common patterns in hotspots**:
1. **God Class**: Too many responsibilities
2. **Feature Envy**: Accessing data from other classes
3. **Shotgun Surgery**: Changes require modifying many places
4. **Divergent Change**: Different reasons to change

**Step 3**: Apply refactoring patterns

**Example: Split large class**:
```python
# Before (❌ God class - changes for many reasons)
class CodeAnalyzer:
    def parse_file(self): pass
    def analyze_complexity(self): pass
    def check_security(self): pass
    def generate_report(self): pass
    def send_notifications(self): pass  # Too many responsibilities!

# After (✅ Single responsibility)
# File: parser.py
class FileParser:
    def parse_file(self): pass

# File: complexity_analyzer.py
class ComplexityAnalyzer:
    def analyze_complexity(self): pass

# File: security_checker.py
class SecurityChecker:
    def check_security(self): pass

# File: report_generator.py
class ReportGenerator:
    def generate_report(self): pass

# File: notifier.py
class Notifier:
    def send_notifications(self): pass
```

**Success Criteria**:
- [ ] Top 3 hotspots refactored
- [ ] Each file has single, clear responsibility
- [ ] Change frequency reduced by 50%+ (measure after 1 month)

### 🟠 HIGH: Implement CODEOWNERS for Critical Files
**Action**: Assign ownership and require reviews for hotspots
**Priority**: HIGH - Prevents quality degradation
**Effort**: 1-2 hours

**Step 1**: Create CODEOWNERS file
```bash
# Create .github/CODEOWNERS
cat > .github/CODEOWNERS << 'EOF'
# Code Owners for Critical Files
# These files require review from designated owners

# Top hotspot files (require senior review)
{hotspots[0]['file'] if hotspots else '/src/critical.py'} @senior-dev-team @tech-lead
{hotspots[1]['file'] if len(hotspots) > 1 else '/src/important.py'} @senior-dev-team

# Core architecture files
/src/codebase_reviewer/models/ @architecture-team
/src/codebase_reviewer/analyzer.py @architecture-team

# Security-sensitive files
/src/codebase_reviewer/security/ @security-team

# Default owners
* @dev-team
EOF
```

**Step 2**: Configure branch protection
```bash
# Via GitHub UI or API
# Settings > Branches > Branch protection rules
# ✅ Require pull request reviews before merging
# ✅ Require review from Code Owners
# ✅ Require status checks to pass
```

**Step 3**: Document ownership
```markdown
# docs/code-ownership.md

## Code Ownership

### Critical Files (High Churn)
- `{hotspots[0]['file'] if hotspots else 'FILE'}`: @senior-dev, @tech-lead
  - Reason: High change frequency, core functionality
  - Review requirements: 2 approvals, all tests pass

### Architecture Files
- `/src/models/`: @architecture-team
  - Reason: Affects entire codebase
  - Review requirements: Architecture review, design doc
```

**Success Criteria**:
- [ ] CODEOWNERS file created
- [ ] Branch protection enabled
- [ ] All team members aware of ownership
- [ ] Review requirements documented

### 🟠 HIGH: Add Extra Scrutiny for Hotspot Changes
**Action**: Implement additional checks for high-risk files
**Priority**: HIGH - Prevents bugs in critical code
**Effort**: 2-3 hours

**Step 1**: Create pre-commit hook for hotspots
```bash
# .git/hooks/pre-commit or use pre-commit framework
cat > .pre-commit-hotspot-check.sh << 'BASH'
#!/bin/bash

# List of hotspot files
HOTSPOTS=(
    "{hotspots[0]['file'] if hotspots else 'src/critical.py'}"
    "{hotspots[1]['file'] if len(hotspots) > 1 else 'src/important.py'}"
)

# Check if any hotspot files are being modified
CHANGED_FILES=$(git diff --cached --name-only)

for hotspot in "${{HOTSPOTS[@]}}"; do
    if echo "$CHANGED_FILES" | grep -q "$hotspot"; then
        echo "⚠️  WARNING: Modifying hotspot file: $hotspot"
        echo "This file has high change frequency. Please ensure:"
        echo "  1. Changes are well-tested"
        echo "  2. Code review is thorough"
        echo "  3. Consider refactoring to reduce complexity"
        echo ""
        read -p "Continue with commit? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
done
BASH

chmod +x .pre-commit-hotspot-check.sh
```

**Step 2**: Add CI/CD checks for hotspots
```yaml
# .github/workflows/hotspot-check.yml
name: Hotspot File Check

on: [pull_request]

jobs:
  check-hotspots:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Check if hotspot files modified
        run: |
          HOTSPOTS=("{hotspots[0]['file'] if hotspots else 'src/critical.py'}" "{hotspots[1]['file'] if len(hotspots) > 1 else 'src/important.py'}")
          CHANGED=$(git diff --name-only origin/main...HEAD)

          for file in "${{HOTSPOTS[@]}}"; do
            if echo "$CHANGED" | grep -q "$file"; then
              echo "::warning::Hotspot file modified: $file"
              echo "::warning::Requires extra scrutiny and testing"
            fi
          done

      - name: Require additional tests for hotspots
        run: |
          # Run extra test suite for hotspot changes
          pytest tests/hotspot_tests/ -v
```

**Success Criteria**:
- [ ] Pre-commit warnings for hotspot changes
- [ ] CI/CD flags hotspot modifications
- [ ] Additional test requirements for hotspots

### 🟡 MEDIUM: Track and Monitor Churn Metrics
**Action**: Set up dashboard to monitor file churn over time
**Priority**: MEDIUM - Enables proactive refactoring
**Effort**: 3-4 hours

**Step 1**: Create churn analysis script
```bash
# scripts/analyze_churn.sh
#!/bin/bash

echo "File Churn Analysis (Last 90 days)"
echo "=================================="

git log --since="90 days ago" --name-only --format="" | \\
    sort | uniq -c | sort -rn | head -20 | \\
    awk '{{printf "%-50s %d changes\\n", $2, $1}}'

echo ""
echo "Churn by Author (Last 90 days)"
echo "==============================="

git log --since="90 days ago" --format="%an" | \\
    sort | uniq -c | sort -rn | head -10
```

**Step 2**: Add to CI/CD dashboard
```yaml
# Generate churn report on schedule
name: Weekly Churn Report

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM

jobs:
  churn-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Generate churn report
        run: |
          bash scripts/analyze_churn.sh > churn_report.txt

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: churn-report
          path: churn_report.txt
```

**Step 3**: Set up alerts for new hotspots
```python
# scripts/churn_alert.py
import subprocess
import sys

CHURN_THRESHOLD = 10  # Alert if file changed >10 times in 30 days

def get_recent_churn():
    result = subprocess.run(
        ['git', 'log', '--since=30 days ago', '--name-only', '--format='],
        capture_output=True, text=True
    )
    files = result.stdout.strip().split('\\n')
    churn = {{}}
    for f in files:
        if f:
            churn[f] = churn.get(f, 0) + 1
    return churn

churn = get_recent_churn()
new_hotspots = {{f: count for f, count in churn.items() if count > CHURN_THRESHOLD}}

if new_hotspots:
    print(f"⚠️  NEW HOTSPOTS DETECTED (>{{CHURN_THRESHOLD}} changes in 30 days):")
    for file, count in sorted(new_hotspots.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {{{{file}}}}: {{{{count}}}} changes")
    sys.exit(1)
```

**Success Criteria**:
- [ ] Churn metrics tracked weekly
- [ ] Dashboard shows trends
- [ ] Alerts for new hotspots
- [ ] Team reviews metrics monthly

### 🟢 LOW: Analyze Temporal Coupling
**Action**: Find files that change together (may indicate hidden dependencies)
**Priority**: LOW - Useful for architecture insights
**Effort**: 2-3 hours

**Step 1**: Install analysis tool
```bash
pip install code-maat
```

**Step 2**: Generate temporal coupling report
```bash
# Export git log
git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > gitlog.txt

# Analyze coupling
code-maat -l gitlog.txt -c git2 -a coupling > coupling.csv

# View top coupled files
cat coupling.csv | sort -t',' -k3 -rn | head -20
```

**Step 3**: Review and address coupling
```markdown
# Files that change together may indicate:
1. **Hidden dependencies**: Consider making explicit
2. **Feature envy**: One file accessing another's data
3. **Shotgun surgery**: Changes require touching multiple files
4. **Missing abstraction**: Common logic should be extracted
```

## Verification Commands

```bash
# Get current hotspots
git log --since="90 days ago" --name-only --format="" | \\
    sort | uniq -c | sort -rn | head -10

# Check CODEOWNERS exists
test -f .github/CODEOWNERS && echo "✅ CODEOWNERS exists" || echo "❌ Missing CODEOWNERS"

# Run churn analysis
bash scripts/analyze_churn.sh

# Check temporal coupling
code-maat -l gitlog.txt -c git2 -a coupling | head -10
```

## Priority Summary
- 🔴 **CRITICAL**: Refactor top hotspots (8-12 hours per file) - **This quarter**
- 🟠 **HIGH**: CODEOWNERS (1-2 hours), Extra scrutiny (2-3 hours) - **This sprint**
- 🟡 **MEDIUM**: Churn monitoring (3-4 hours) - **This month**
- 🟢 **LOW**: Temporal coupling (2-3 hours) - **When time permits**

**Total Effort**: ~11-17 hours for critical/high priority items

## Temporal Coupling
*Note: Use code-maat or similar tools to identify files that change together, indicating potential hidden dependencies or architectural issues*
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_logging_review(self, prompt_id, prompt_text, context, repository):
        """Generate logging review response."""
        if isinstance(context, dict):
            files_analyzed = context.get("files_analyzed", 0)
            logging_imports = context.get("logging_imports_count", 0)
            files_with_logging = context.get("files_with_logging", [])
            files_with_print = context.get("files_with_print", [])
            has_structured = context.get("has_structured_logging", False)

            print_count = sum(f.get("count", 0) for f in files_with_print)

            return f"""# Logging and Observability Review

## Logging Infrastructure
- **Files Analyzed**: {files_analyzed}
- **Logging Imports**: {logging_imports}
- **Files Using Logging**: {len(files_with_logging)}
- **Files Using Print**: {len(files_with_print)} ({print_count} total print statements)
- **Structured Logging**: {'✅ Yes' if has_structured else '❌ No'}

## Current Logging Practices

### Print Statements vs Logging
{self._format_print_vs_logging(files_with_print, files_with_logging)}

## Issues Identified

### Critical Issues
1. **Heavy use of print() instead of logging**: {print_count} print statements found
2. **Inconsistent logging approach**: Mix of print and logging
3. **No structured logging**: Difficult to parse and analyze logs

### Medium Priority
1. Limited logging coverage ({len(files_with_logging)}/{files_analyzed} files)
2. No apparent log levels (DEBUG, INFO, WARNING, ERROR)
3. Missing contextual information in logs

## Action Items

### 🟠 HIGH: Replace print() with Logging
**Action**: Convert {print_count} print statements to proper logging
**Priority**: HIGH - Print statements don't support log levels or structured output
**Effort**: ~{max(1, print_count // 20)} hours

**Step 1**: Find all print statements
```bash
# Find all print statements
grep -rn "print(" src/ --include="*.py" > print_statements.txt

# Count by file
grep -rn "print(" src/ --include="*.py" | cut -d: -f1 | sort | uniq -c | sort -rn
```

**Step 2**: Replace print with logging

**Before** (❌ Using print):
```python
def process_data(data):
    print(f"Processing {{len(data)}} items")
    for item in data:
        print(f"Processing item: {{item}}")
    print("Done!")
```

**After** (✅ Using logging):
```python
import logging

logger = logging.getLogger(__name__)

def process_data(data):
    logger.info(f"Processing {{len(data)}} items")
    for item in data:
        logger.debug(f"Processing item: {{item}}")
    logger.info("Processing complete")
```

**Step 3**: Set up logging configuration
```python
# src/codebase_reviewer/logging_config.py
import logging
import logging.config

LOGGING_CONFIG = {{
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {{
        'standard': {{
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }},
        'detailed': {{
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s'
        }},
    }},
    'handlers': {{
        'console': {{
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        }},
        'file': {{
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }},
    }},
    'loggers': {{
        'codebase_reviewer': {{
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        }},
    }},
    'root': {{
        'level': 'INFO',
        'handlers': ['console']
    }}
}}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
```

**Step 4**: Initialize logging in main
```python
# src/codebase_reviewer/cli.py or __main__.py
from codebase_reviewer.logging_config import setup_logging

def main():
    setup_logging()
    # ... rest of application
```

**Success Criteria**:
- [ ] Zero print() statements in production code (tests OK)
- [ ] All modules use logging.getLogger(__name__)
- [ ] Appropriate log levels used (DEBUG, INFO, WARNING, ERROR)
- [ ] Logging configuration centralized

### 🟠 HIGH: Implement Structured Logging
**Action**: Add JSON-formatted structured logging
**Priority**: HIGH - Enables log parsing, searching, and analysis
**Effort**: 2 hours

**Step 1**: Install structured logging library
```bash
pip install python-json-logger
```

**Step 2**: Configure JSON logging
```python
# Update logging_config.py
from pythonjsonlogger import jsonlogger

LOGGING_CONFIG = {{
    'version': 1,
    'formatters': {{
        'json': {{
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }},
    }},
    'handlers': {{
        'json_file': {{
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'json',
            'filename': 'logs/app.json',
            'maxBytes': 10485760,
            'backupCount': 5
        }},
    }},
    'root': {{
        'level': 'INFO',
        'handlers': ['json_file']
    }}
}}
```

**Step 3**: Add contextual information
```python
import logging

logger = logging.getLogger(__name__)

def process_request(request_id, user_id, data):
    logger.info(
        "Processing request",
        extra={{
            'request_id': request_id,
            'user_id': user_id,
            'data_size': len(data),
            'action': 'process_request'
        }}
    )
```

**Output** (JSON format):
```json
{{
  "asctime": "2025-11-23 23:45:00,123",
  "name": "codebase_reviewer.processor",
  "levelname": "INFO",
  "message": "Processing request",
  "request_id": "req-12345",
  "user_id": "user-789",
  "data_size": 100,
  "action": "process_request"
}}
```

### 🟡 MEDIUM: Add Log Rotation
**Action**: Prevent log files from filling disk
**Location**: Update logging configuration

**Configuration**:
```python
# Already included in logging_config.py above
'file': {{
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': 'logs/app.log',
    'maxBytes': 10485760,  # 10MB per file
    'backupCount': 5,      # Keep 5 old files (50MB total)
}}

# Or use time-based rotation
'file': {{
    'class': 'logging.handlers.TimedRotatingFileHandler',
    'filename': 'logs/app.log',
    'when': 'midnight',    # Rotate at midnight
    'interval': 1,         # Every 1 day
    'backupCount': 30,     # Keep 30 days
}}
```

### 🟡 MEDIUM: Add Contextual Logging
**Action**: Include request IDs, correlation IDs, user context
**Effort**: 2 hours

**Implementation**:
```python
# src/codebase_reviewer/logging_context.py
import logging
import contextvars
from typing import Optional

# Context variables for request tracking
request_id_var = contextvars.ContextVar('request_id', default=None)
user_id_var = contextvars.ContextVar('user_id', default=None)

class ContextFilter(logging.Filter):
    'Add context variables to log records.'

    def filter(self, record):
        record.request_id = request_id_var.get()
        record.user_id = user_id_var.get()
        return True

# Add to logging config
LOGGING_CONFIG['filters'] = {{
    'context': {{
        'class': 'codebase_reviewer.logging_context.ContextFilter'
    }}
}}

LOGGING_CONFIG['formatters']['standard']['format'] = (
    '%(asctime)s [%(levelname)s] [req:%(request_id)s] '
    '[user:%(user_id)s] %(name)s: %(message)s'
)

# Usage in application
from codebase_reviewer.logging_context import request_id_var, user_id_var

def handle_request(request):
    request_id_var.set(request.id)
    user_id_var.set(request.user_id)

    logger.info("Processing request")  # Automatically includes context
```

### 🟢 LOW: Add Log Aggregation
**Action**: Integrate with centralized logging system
**Options**: ELK Stack, Datadog, CloudWatch, Splunk
**Effort**: 4-8 hours

**Example: ELK Stack Integration**:
```python
# Install logstash handler
pip install python-logstash

# Add to logging config
'logstash': {{
    'class': 'logstash.TCPLogstashHandler',
    'host': 'logstash.example.com',
    'port': 5959,
    'version': 1,
}}
```

## Verification Commands

```bash
# Verify no print statements remain
grep -rn "print(" src/ --include="*.py" | grep -v "# print OK" && echo "❌ FAIL" || echo "✅ PASS"

# Test logging configuration
python -c "from codebase_reviewer.logging_config import setup_logging; setup_logging(); import logging; logging.getLogger('test').info('Test message')"

# Check log files are created
ls -lh logs/

# Verify log rotation works
python -c "import logging.handlers; h = logging.handlers.RotatingFileHandler('test.log', maxBytes=100, backupCount=3); [h.emit(logging.LogRecord('test', logging.INFO, '', 0, f'msg{{i}}', (), None)) for i in range(100)]"
ls -lh test.log*

# Parse JSON logs
cat logs/app.json | jq '.levelname' | sort | uniq -c
```

## Priority Summary
- 🔴 **CRITICAL**: None
- 🟠 **HIGH**: Replace print() with logging ({max(1, print_count // 20)} hours), Structured logging (2 hours) - **This week**
- 🟡 **MEDIUM**: Log rotation (30 min), Contextual logging (2 hours) - **This month**
- 🟢 **LOW**: Log aggregation (4-8 hours), Monitoring dashboards

**Total Effort**: ~{max(1, print_count // 20) + 4} hours for high priority items

## Long-term Recommendations
1. **Log aggregation**: Integrate with ELK stack, Datadog, or similar
2. **Distributed tracing**: Add OpenTelemetry for request tracing
3. **Log-based metrics**: Extract metrics from structured logs
4. **Alerting**: Set up alerts for ERROR/CRITICAL logs

## Example Implementation
```python
import logging
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

# Instead of: print(f"Processing {{file}}")
# Use: logger.info("processing_file", file=file, status="started")
```

## Observability Gaps
- No metrics collection
- No distributed tracing
- No error tracking (Sentry, Rollbar)
- No performance monitoring (APM)
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    # Helper methods for new generators
    def _format_entry_points(self, internal_deps: Dict) -> str:
        """Format entry points from dependencies."""
        entry_points = [
            k
            for k in internal_deps.keys()
            if "cli.py" in k or "main.py" in k or "__main__.py" in k
        ]
        if not entry_points:
            return "- No clear entry points identified"
        return "\n".join(f"- `{ep}`" for ep in entry_points[:5])

    def _format_most_imported(self, most_imported: List[Dict]) -> str:
        """Format most imported modules."""
        if not most_imported:
            return "- No import data available"
        return "\n".join(
            f"{i+1}. `{mod['module']}` - imported by {mod['count']} modules"
            for i, mod in enumerate(most_imported[:10])
        )

    def _format_high_fan_in(self, modules: List[Dict]) -> str:
        """Format high fan-in modules."""
        if not modules:
            return "- No high fan-in modules detected"
        return "\n".join(
            f"- `{mod['module']}`: {mod['count']} dependents" for mod in modules
        )

    def _format_sample_dependencies(self, deps: Dict) -> str:
        """Format sample dependencies."""
        if not deps:
            return "- No dependencies mapped"
        samples = list(deps.items())[:5]
        result = []
        for file, imports in samples:
            result.append(f"\n**{file}**:")
            for imp in imports[:3]:
                result.append(f"  - {imp}")
        return "\n".join(result)

    def _format_hotspots(self, hotspots: List[Dict]) -> str:
        """Format hotspot files."""
        if not hotspots:
            return "- No hotspots detected"
        return "\n".join(
            f"{i+1}. `{h['file']}` - {h['change_count']} changes"
            for i, h in enumerate(hotspots)
        )

    def _format_critical_hotspots(self, hotspots: List[Dict]) -> str:
        """Format critical hotspots (>10 changes)."""
        critical = [h for h in hotspots if h.get("change_count", 0) > 10]
        if not critical:
            return "- No critical hotspots (all files <10 changes)"
        return "\n".join(
            f"- `{h['file']}`: {h['change_count']} changes" for h in critical
        )

    def _format_moderate_hotspots(self, hotspots: List[Dict]) -> str:
        """Format moderate hotspots (5-10 changes)."""
        moderate = [h for h in hotspots if 5 <= h.get("change_count", 0) <= 10]
        if not moderate:
            return "- No moderate hotspots"
        return "\n".join(
            f"- `{h['file']}`: {h['change_count']} changes" for h in moderate
        )

    def _format_print_vs_logging(
        self, print_files: List[Dict], logging_files: List
    ) -> str:
        """Format print vs logging comparison."""
        print_count = sum(f.get("count", 0) for f in print_files)
        return f"""
**Print Statements**: {print_count} found in {len(print_files)} files
**Logging Statements**: {len(logging_files)} files using logging

**Files with Most Print Statements**:
{self._format_print_files(print_files[:5])}

**Recommendation**: Replace all print() with proper logging
"""

    def _format_print_files(self, print_files: List[Dict]) -> str:
        """Format files with print statements."""
        if not print_files:
            return "- None"
        return "\n".join(
            f"- `{f['file']}`: {f['count']} print statements" for f in print_files
        )

    # Remaining unimplemented generators
    def _generate_setup_validation(self, prompt_id, prompt_text, context, repository):
        """Generate setup validation response."""
        if isinstance(context, dict):
            documented_setup = context.get("documented_setup", {})
            setup_files = context.get("setup_files_found", [])
            deps_count = context.get("dependencies_count", 0)
            undocumented = context.get("undocumented_features", [])

            prereqs = documented_setup.get("prerequisites", [])
            build_steps = documented_setup.get("build_steps", [])
            env_vars = documented_setup.get("env_vars", [])

            return f"""# Setup Documentation Accuracy Report

## Summary
Analyzed setup documentation for repository at `{repository}`.
Found {len(setup_files)} setup configuration file(s) with {deps_count} dependencies.

## Documented Prerequisites
{self._format_list(prereqs) if prereqs else "- No prerequisites documented"}

## Setup Files Found
{self._format_list(setup_files) if setup_files else "- No setup files found"}

## Build Steps
{self._format_list(build_steps) if build_steps else "- No build steps documented"}

## Environment Variables
{self._format_list(env_vars) if env_vars else "- No environment variables documented"}

## Undocumented Features
{self._format_list(undocumented) if undocumented else "✅ No undocumented features detected"}

## Validation Results

### Prerequisites Accuracy
- **Documented**: {len(prereqs)} prerequisite(s)
- **Status**: {"✅ Complete" if prereqs else "⚠️ Missing prerequisites documentation"}

### Dependency Management
- **Total Dependencies**: {deps_count}
- **Setup Files**: {len(setup_files)}
- **Status**: {"✅ Dependencies documented" if setup_files else "⚠️ No setup files found"}

## Action Items

### 🟠 HIGH: Test Setup Instructions
**Action**: Verify setup instructions work on clean environment
**Priority**: Ensure new developers can onboard successfully

**Step 1**: Create test environment
```bash
# Create fresh virtual environment
python3 -m venv test_env
source test_env/bin/activate

# Or use Docker for isolated test
docker run -it --rm -v $(pwd):/app python:3.9 bash
```

**Step 2**: Follow documented setup steps exactly
```bash
# Follow README instructions step-by-step
# Document any errors or missing steps
# Time how long setup takes
```

**Step 3**: Verify functionality
```bash
# Test that all features work after setup
review-codebase --help
review-codebase analyze .
```

**Success Criteria**:
- [ ] Setup completes without errors
- [ ] All dependencies install correctly
- [ ] Application runs successfully
- [ ] Setup time < 10 minutes

### {"🔴 CRITICAL" if not prereqs else "🟢 LOW"}: Document Prerequisites
**Action**: {"Add missing prerequisites to README" if not prereqs else "Prerequisites documented - verify accuracy"}
**Location**: README.md (add "Prerequisites" section before "Quick Start")

{"**Current Status**: ❌ No prerequisites documented" if not prereqs else f"**Current Status**: ✅ {len(prereqs)} prerequisites documented"}

**Template** (README.md):
```markdown
## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**: [Download](https://www.python.org/downloads/)
- **pip**: Usually comes with Python
- **Git**: For cloning the repository
- **Virtual Environment**: `python3 -m venv` (recommended)

### Optional
- **Docker**: For containerized deployment
- **Make**: For using Makefile commands
```

**Verification**:
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Check pip
pip --version

# Check git
git --version
```

### {"🟠 HIGH" if not setup_files else "🟢 LOW"}: Add Setup Configuration Files
**Action**: {"Create missing setup files" if not setup_files else "Setup files present - verify completeness"}

{"**Current Status**: ❌ No setup files found" if not setup_files else f"**Current Status**: ✅ {len(setup_files)} setup file(s) found: {', '.join(setup_files)}"}

**Step 1**: Create requirements.txt
```bash
# Generate from current environment
pip freeze > requirements.txt

# Or create manually with pinned versions
cat > requirements.txt << 'EOF'
flask==2.3.0
pyyaml==6.0
click==8.1.0
EOF
```

**Step 2**: Create setup.py for package installation
```python
from setuptools import setup, find_packages

setup(
    name="codebase-reviewer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    install_requires=[
        "flask>=2.3.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
    ],
    entry_points={{
        "console_scripts": [
            "review-codebase=codebase_reviewer.cli:main",
        ],
    }},
)
```

**Step 3**: Test installation
```bash
pip install -e .  # Install in editable mode
review-codebase --version  # Verify installation
```

### {"🟡 MEDIUM" if not build_steps else "🟢 LOW"}: Document Build Steps
**Action**: {"Add build/installation steps to README" if not build_steps else "Build steps documented - verify accuracy"}

**Template** (README.md):
```markdown
## Installation

### Option 1: Quick Install (Recommended)
```bash
# Clone repository
git clone https://github.com/your-org/codebase-reviewer.git
cd codebase-reviewer

# Run setup script
./setup.sh
```

### Option 2: Manual Install
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install dependencies
pip install -e .

# Verify installation
review-codebase --version
```

### Option 3: Docker
```bash
docker build -t codebase-reviewer .
docker run -it codebase-reviewer
```
```

### {"🟡 MEDIUM" if not env_vars else "🟢 LOW"}: Document Environment Variables
**Action**: {"Add environment variables documentation" if not env_vars else "Environment variables documented - verify completeness"}

**Template** (README.md or .env.example):
```bash
# .env.example - Copy to .env and fill in values

# Application Settings
APP_ENV=development  # development, staging, production
LOG_LEVEL=INFO       # DEBUG, INFO, WARNING, ERROR

# API Keys (if applicable)
# OPENAI_API_KEY=your_key_here

# Database (if applicable)
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# Optional Settings
# MAX_FILE_SIZE=10485760  # 10MB in bytes
# CACHE_ENABLED=true
```

**Usage Documentation**:
```markdown
## Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
# Edit .env with your values
```

Or set environment variables directly:

```bash
export APP_ENV=production
export LOG_LEVEL=WARNING
```
```

### {"🟠 HIGH" if undocumented else "🟢 LOW"}: Document Undocumented Features
**Action**: {"Add documentation for {len(undocumented)} undocumented feature(s)" if undocumented else "No undocumented features detected"}

{f"**Undocumented Features**: {', '.join(undocumented)}" if undocumented else ""}

## Verification Commands

```bash
# Test setup from scratch
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
review-codebase --help  # Should work

# Verify all dependencies install
pip install -r requirements.txt  # Should complete without errors

# Check for missing documentation
grep -i "prerequisite\|requirement" README.md  # Should find prerequisites section
```

## Priority Summary
- 🔴 **CRITICAL**: {"Document prerequisites (1 hour)" if not prereqs else "None"}
- 🟠 **HIGH**: Test setup instructions (30 min){", Add setup files (1 hour)" if not setup_files else ""}{", Document undocumented features (30 min)" if undocumented else ""}
- 🟡 **MEDIUM**: {"Document build steps (30 min)" if not build_steps else ""}{", Document environment variables (30 min)" if not env_vars else ""}
- 🟢 **LOW**: Verify existing documentation accuracy

**Total Effort**: ~{2 if not prereqs else 0 + 1 if not setup_files else 0 + 0.5 if not build_steps else 0 + 0.5 if not env_vars else 0 + 0.5} hours

## Accuracy Score
- **Prerequisites**: {"100%" if prereqs else "0%"}
- **Setup Files**: {"100%" if setup_files else "0%"}
- **Overall**: {self._calculate_setup_score(prereqs, setup_files, build_steps)}%
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_static_analysis(self, prompt_id, prompt_text, context, repository):
        """Generate static analysis summary response."""
        # For static analysis, we typically get quality issues from context
        return f"""# Static Analysis Summary

## Analysis Overview
Performed static analysis on repository at `{repository}`.

## Code Quality Metrics
- **Linting**: Run pylint/flake8 for Python code
- **Type Checking**: Run mypy for type safety
- **Complexity**: Analyze cyclomatic complexity
- **Code Smells**: Detect anti-patterns

## High-Severity Issues
*Note: Run actual linting tools (pylint, flake8, mypy) for specific issues*

### Recommended Tools
- **Python**: pylint, flake8, mypy, bandit
- **JavaScript**: ESLint, TypeScript compiler
- **Go**: golint, go vet, staticcheck

## Common Anti-Patterns to Check
1. **God Classes**: Classes with too many responsibilities
2. **Long Methods**: Functions exceeding 50 lines
3. **Deep Nesting**: Nesting depth > 4 levels
4. **Duplicate Code**: Copy-pasted logic
5. **Magic Numbers**: Hardcoded values without constants

## Action Items

### 🔴 CRITICAL: Set Up Linting in CI/CD Pipeline
**Action**: Integrate automated linting to catch issues before merge
**Priority**: CRITICAL - Prevents quality degradation
**Effort**: 2-3 hours

**Step 1**: Install linting tools
```bash
# Python linting tools
pip install pylint flake8 mypy bandit black isort

# Add to requirements-dev.txt
echo "pylint>=2.17.0" >> requirements-dev.txt
echo "flake8>=6.0.0" >> requirements-dev.txt
echo "mypy>=1.0.0" >> requirements-dev.txt
echo "bandit>=1.7.0" >> requirements-dev.txt
echo "black>=23.0.0" >> requirements-dev.txt
echo "isort>=5.12.0" >> requirements-dev.txt
```

**Step 2**: Create linting configuration

**Create `.pylintrc`**:
```ini
[MASTER]
max-line-length=100
disable=C0111,R0903

[MESSAGES CONTROL]
disable=missing-docstring,too-few-public-methods

[DESIGN]
max-args=7
max-locals=15
max-returns=6
max-branches=12
```

**Create `.flake8`**:
```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,build,dist
ignore = E203,W503
```

**Create `mypy.ini`**:
```ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

**Step 3**: Add CI/CD integration

**GitHub Actions** (`.github/workflows/lint.yml`):
```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      - name: Run pylint
        run: pylint src/
      - name: Run flake8
        run: flake8 src/
      - name: Run mypy
        run: mypy src/
      - name: Run bandit
        run: bandit -r src/
```

**Success Criteria**:
- [ ] All linting tools installed
- [ ] Configuration files created
- [ ] CI/CD pipeline runs linting on every PR
- [ ] Linting failures block merges

### 🟠 HIGH: Set Up Pre-Commit Hooks
**Action**: Catch issues before commit
**Priority**: HIGH - Improves developer experience
**Effort**: 1 hour

**Step 1**: Install pre-commit
```bash
pip install pre-commit
echo "pre-commit>=3.0.0" >> requirements-dev.txt
```

**Step 2**: Create `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', 'src/']
```

**Step 3**: Install hooks
```bash
pre-commit install
pre-commit run --all-files  # Test on all files
```

**Success Criteria**:
- [ ] Pre-commit hooks installed
- [ ] Hooks run automatically on commit
- [ ] Team members have hooks installed

### 🟠 HIGH: Fix High-Severity Linting Issues
**Action**: Address critical code quality issues
**Priority**: HIGH - Improves code maintainability
**Effort**: 4-8 hours

**Step 1**: Run linting and capture issues
```bash
# Generate reports
pylint src/ > pylint_report.txt 2>&1 || true
flake8 src/ > flake8_report.txt 2>&1 || true
mypy src/ > mypy_report.txt 2>&1 || true

# Count issues by severity
grep "error" pylint_report.txt | wc -l
grep "warning" pylint_report.txt | wc -l
```

**Step 2**: Fix critical issues first

**Example: Fix undefined variables**:
```bash
# Find undefined variables
mypy src/ | grep "error: Name.*is not defined"
```

**Example: Fix unused imports**:
```bash
# Auto-remove unused imports
autoflake --remove-all-unused-imports --in-place --recursive src/
```

**Example: Fix formatting**:
```bash
# Auto-format code
black src/
isort src/
```

**Success Criteria**:
- [ ] Zero critical errors
- [ ] <10 warnings per 1000 lines
- [ ] All code formatted consistently

### 🟡 MEDIUM: Establish Code Quality Thresholds
**Action**: Define minimum quality standards
**Priority**: MEDIUM - Prevents regression
**Effort**: 2 hours

**Step 1**: Measure current baseline
```bash
# Get current quality score
pylint src/ | tail -5

# Get complexity metrics
radon cc src/ -a -nb
```

**Step 2**: Set quality gates

**Create `quality_gates.sh`**:
```bash
#!/bin/bash
set -e

echo "Running quality checks..."

# Pylint score must be >= 8.0
PYLINT_SCORE=$(pylint src/ | grep "Your code has been rated" | awk '{{print $7}}' | cut -d'/' -f1)
if (( $(echo "$PYLINT_SCORE < 8.0" | bc -l) )); then
    echo "❌ Pylint score $PYLINT_SCORE is below 8.0"
    exit 1
fi
echo "✅ Pylint score: $PYLINT_SCORE"

# No mypy errors allowed
MYPY_ERRORS=$(mypy src/ 2>&1 | grep "error" | wc -l)
if [ "$MYPY_ERRORS" -gt 0 ]; then
    echo "❌ Found $MYPY_ERRORS mypy errors"
    exit 1
fi
echo "✅ No mypy errors"

# Complexity must be < 10
HIGH_COMPLEXITY=$(radon cc src/ -n C | wc -l)
if [ "$HIGH_COMPLEXITY" -gt 0 ]; then
    echo "⚠️  Found $HIGH_COMPLEXITY functions with complexity >= 10"
fi

echo "✅ All quality gates passed!"
```

**Step 3**: Add to CI/CD
```yaml
- name: Check quality gates
  run: bash quality_gates.sh
```

**Success Criteria**:
- [ ] Quality thresholds defined
- [ ] Baseline measured
- [ ] Gates enforced in CI/CD

## Verification Commands

```bash
# Test linting setup
pylint src/ && echo "✅ Pylint passed" || echo "❌ Pylint failed"
flake8 src/ && echo "✅ Flake8 passed" || echo "❌ Flake8 failed"
mypy src/ && echo "✅ Mypy passed" || echo "❌ Mypy failed"

# Test pre-commit hooks
pre-commit run --all-files && echo "✅ Pre-commit passed" || echo "❌ Pre-commit failed"

# Check quality score
pylint src/ | grep "Your code has been rated"

# Check complexity
radon cc src/ -a -nb
```

## Priority Summary
- 🔴 **CRITICAL**: CI/CD linting (2-3 hours) - **DO THIS WEEK**
- 🟠 **HIGH**: Pre-commit hooks (1 hour), Fix issues (4-8 hours) - **This sprint**
- 🟡 **MEDIUM**: Quality thresholds (2 hours) - **This month**

**Total Effort**: ~9-14 hours for critical/high priority items
"""

    def _generate_comment_quality(self, prompt_id, prompt_text, context, repository):
        """Generate comment quality analysis response."""
        return f"""# Code Comment Quality Analysis

## Summary
Analyzed code comments and documentation in repository at `{repository}`.

## Comment Quality Assessment

### Docstring Coverage
- **Modules**: Check for module-level docstrings
- **Classes**: Check for class-level docstrings
- **Functions**: Check for function docstrings with parameters and return values

### Comment Issues Found

#### 1. TODO/FIXME Comments
*Scan for TODO, FIXME, HACK, XXX comments*
- Review for actionability
- Check if linked to tickets
- Identify stale comments

#### 2. Contradictory Comments
*Comments that don't match code behavior*
- Outdated after refactoring
- Misleading descriptions
- Incorrect parameter documentation

#### 3. Missing Comments
*Complex code lacking explanation*
- Complex algorithms without explanation
- Non-obvious business logic
- Tricky edge case handling

#### 4. Over-Commented Code
*Trivial code with excessive comments*
- Comments stating the obvious
- Redundant docstrings
- Noise that reduces readability

### Comment Style Consistency
- **Docstring Format**: Check for consistent style (Google, NumPy, Sphinx)
- **Inline Comments**: Check for consistent formatting
- **Language**: Check for consistent language (English)

## Action Items

### 🔴 CRITICAL: Add Missing Docstrings to Public APIs
**Action**: Document all public functions, classes, and modules
**Priority**: CRITICAL - Essential for maintainability and onboarding
**Effort**: 6-10 hours

**Step 1**: Measure current docstring coverage
```bash
# Install interrogate
pip install interrogate

# Check coverage
interrogate src/ -vv

# Generate badge
interrogate src/ --generate-badge .
```

**Step 2**: Find missing docstrings
```bash
# Find functions without docstrings
interrogate src/ -vv | grep "MISSING"

# Find specific files with low coverage
interrogate src/ --fail-under=80 -vv
```

**Step 3**: Add docstrings following Google style

**Before** (❌ No documentation):
```python
def analyze_code(path, options):
    results = []
    for file in get_files(path):
        results.append(process(file, options))
    return results
```

**After** (✅ Well documented):
```python
def analyze_code(path: str, options: dict) -> list:
    '''Analyze code files in the given path.

    Args:
        path: Directory path to analyze
        options: Analysis options including:
            - depth: Maximum directory depth
            - exclude: Patterns to exclude

    Returns:
        List of analysis results, one per file

    Raises:
        ValueError: If path does not exist
        PermissionError: If path is not readable

    Example:
        >>> results = analyze_code('/src', {{'depth': 3}})
        >>> len(results)
        42
    '''
    results = []
    for file in get_files(path):
        results.append(process(file, options))
    return results
```

**Step 4**: Add module and class docstrings
```python
'''Code analysis module.

This module provides functionality for analyzing Python codebases,
including complexity metrics, style checking, and documentation coverage.

Typical usage example:
    analyzer = CodeAnalyzer()
    results = analyzer.analyze('/path/to/code')
'''

class CodeAnalyzer:
    '''Analyzes Python code for quality metrics.

    This class provides methods for analyzing code complexity,
    style compliance, and documentation coverage.

    Attributes:
        config: Configuration dictionary
        results: Analysis results cache
    '''
```

**Success Criteria**:
- [ ] 90%+ docstring coverage (run `interrogate src/`)
- [ ] All public functions documented
- [ ] All classes documented
- [ ] All modules have module-level docstrings

### 🟠 HIGH: Review and Resolve TODO/FIXME Comments
**Action**: Address or ticket all TODO/FIXME comments
**Priority**: HIGH - Prevents technical debt accumulation
**Effort**: 4-6 hours

**Step 1**: Find all TODO/FIXME comments
```bash
# Find all TODO comments
grep -rn "TODO" src/ --include="*.py" > todos.txt

# Find all FIXME comments
grep -rn "FIXME" src/ --include="*.py" >> todos.txt

# Find HACK and XXX comments
grep -rn "HACK\\|XXX" src/ --include="*.py" >> todos.txt

# Count by type
echo "TODOs: $(grep -c TODO todos.txt)"
echo "FIXMEs: $(grep -c FIXME todos.txt)"
```

**Step 2**: Categorize and prioritize
```bash
# Create tracking spreadsheet
cat > todo_tracking.csv << 'CSV'
File,Line,Type,Description,Priority,Ticket,Status
src/analyzer.py,42,TODO,Add caching,HIGH,PROJ-123,In Progress
src/parser.py,156,FIXME,Handle edge case,CRITICAL,PROJ-124,Open
CSV
```

**Step 3**: Resolve or ticket each item

**Option 1: Fix immediately** (for simple TODOs):
```python
# Before
def process(data):
    # TODO: Add validation
    return transform(data)

# After
def process(data):
    if not data:
        raise ValueError("Data cannot be empty")
    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")
    return transform(data)
```

**Option 2: Create ticket and link** (for complex TODOs):
```python
# Before
# TODO: Implement caching layer

# After
# TODO(PROJ-123): Implement caching layer for performance
# See: https://github.com/org/repo/issues/123
```

**Option 3: Remove if obsolete**:
```python
# Remove outdated TODOs that are no longer relevant
```

**Success Criteria**:
- [ ] All TODOs reviewed
- [ ] Critical FIXMEs resolved or ticketed
- [ ] All remaining TODOs linked to tickets
- [ ] <5 TODOs per 1000 lines of code

### 🟠 HIGH: Fix Contradictory and Outdated Comments
**Action**: Update comments to match current code behavior
**Priority**: HIGH - Misleading comments cause bugs
**Effort**: 3-4 hours

**Step 1**: Find potentially outdated comments
```bash
# Find comments with dates (often outdated)
grep -rn "# [0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}" src/ --include="*.py"

# Find comments mentioning "old", "deprecated", "legacy"
grep -rn "# .*\\(old\\|deprecated\\|legacy\\)" src/ --include="*.py"

# Find comments with "FIXME" or "HACK"
grep -rn "# .*\\(FIXME\\|HACK\\)" src/ --include="*.py"
```

**Step 2**: Review and update

**Example 1: Outdated parameter description**:
```python
# Before (❌ Wrong parameter name)
def calculate(value, multiplier):
    '''Calculate result.

    Args:
        num: The input number  # ❌ Wrong name!
        factor: The multiplier
    '''
    return value * multiplier

# After (✅ Correct)
def calculate(value, multiplier):
    '''Calculate result.

    Args:
        value: The input number
        multiplier: The multiplication factor
    '''
    return value * multiplier
```

**Example 2: Misleading comment**:
```python
# Before (❌ Comment doesn't match code)
# Returns True if valid
def validate(data):
    if not data:
        raise ValueError("Invalid data")  # ❌ Raises, doesn't return!
    return data

# After (✅ Accurate)
# Validates data and returns it if valid, raises ValueError otherwise
def validate(data):
    if not data:
        raise ValueError("Invalid data")
    return data
```

**Success Criteria**:
- [ ] All parameter names match docstrings
- [ ] All return value descriptions accurate
- [ ] No contradictory comments found in review

### 🟡 MEDIUM: Establish Docstring Style Guide and Linting
**Action**: Enforce consistent documentation style
**Priority**: MEDIUM - Improves consistency
**Effort**: 2-3 hours

**Step 1**: Choose docstring style (Google recommended)
```bash
# Install pydocstyle
pip install pydocstyle
echo "pydocstyle>=6.3.0" >> requirements-dev.txt
```

**Step 2**: Create `.pydocstyle` configuration
```ini
[pydocstyle]
inherit = false
convention = google
add-ignore = D100,D104
match = .*\\.py
match-dir = ^(?!\\.|tests|migrations).*
```

**Step 3**: Add to CI/CD and pre-commit

**Add to `.pre-commit-config.yaml`**:
```yaml
  - repo: https://github.com/pycqa/pydocstyle
    rev: 6.3.0
    hooks:
      - id: pydocstyle
        args: ['--convention=google']
```

**Add to CI/CD**:
```yaml
- name: Check docstring style
  run: pydocstyle src/
```

**Step 4**: Create style guide document

**Create `docs/docstring-style-guide.md`**:
```markdown
# Docstring Style Guide

## Standard: Google Style

### Module Docstrings
\`\`\`python
'''One-line summary.

Detailed description of the module.
Can span multiple lines.
'''
\`\`\`

### Function Docstrings
\`\`\`python
def function(arg1: str, arg2: int) -> bool:
    '''One-line summary.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
    '''
\`\`\`

### Class Docstrings
\`\`\`python
class MyClass:
    '''One-line summary.

    Detailed description.

    Attributes:
        attr1: Description
        attr2: Description
    '''
\`\`\`
```

**Success Criteria**:
- [ ] Style guide documented
- [ ] pydocstyle configured
- [ ] Linting added to CI/CD
- [ ] Team trained on style

### 🟢 LOW: Remove Obvious and Redundant Comments
**Action**: Clean up noise comments
**Priority**: LOW - Improves readability
**Effort**: 2-3 hours

**Examples to remove**:
```python
# Before (❌ Obvious comments)
# Increment counter
counter += 1

# Loop through items
for item in items:
    # Process item
    process(item)

# Return result
return result

# After (✅ Clean code)
counter += 1

for item in items:
    process(item)

return result
```

**Keep comments that explain WHY, not WHAT**:
```python
# ✅ Good comment (explains why)
# Use binary search because list is pre-sorted by timestamp
result = binary_search(items, target)

# ❌ Bad comment (states the obvious)
# Call binary search function
result = binary_search(items, target)
```

## Verification Commands

```bash
# Check docstring coverage
interrogate src/ -vv

# Check docstring style
pydocstyle src/

# Count TODO/FIXME comments
grep -r "TODO\\|FIXME" src/ --include="*.py" | wc -l

# Find files with low coverage
interrogate src/ --fail-under=80 -vv | grep "FAILED"
```

## Priority Summary
- 🔴 **CRITICAL**: Add docstrings (6-10 hours) - **This sprint**
- 🟠 **HIGH**: Resolve TODOs (4-6 hours), Fix contradictory comments (3-4 hours) - **This sprint**
- 🟡 **MEDIUM**: Style guide and linting (2-3 hours) - **This month**
- 🟢 **LOW**: Remove obvious comments (2-3 hours) - **When time permits**

**Total Effort**: ~15-23 hours for critical/high priority items

## Quality Score
- **Docstring Coverage**: Target 90%+ (run `interrogate src/`)
- **TODO/FIXME Ratio**: Target <5 per 1000 lines
- **Style Compliance**: Target 100% (run `pydocstyle src/`)
"""

    def _generate_error_handling(self, prompt_id, prompt_text, context, repository):
        """Generate error handling analysis response."""
        return f"""# Error Handling & Resilience Analysis

## Summary
Analyzed error handling patterns in repository at `{repository}`.

## Error Handling Patterns

### Exception Handling Coverage
- **Try-Except Blocks**: Scan for proper exception handling
- **Specific Exceptions**: Check for catching specific vs. broad exceptions
- **Error Logging**: Verify errors are logged appropriately
- **Resource Cleanup**: Check for proper cleanup (finally blocks, context managers)

### Common Issues

#### 1. Silent Failures
```python
# BAD: Silently swallowing exceptions
try:
    risky_operation()
except:
    pass

# GOOD: Log and handle appropriately
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {{e}}")
    raise
```

#### 2. Broad Exception Catching
```python
# BAD: Catching all exceptions
try:
    operation()
except Exception:
    return None

# GOOD: Catch specific exceptions
try:
    operation()
except ValueError as e:
    logger.warning(f"Invalid value: {{e}}")
    return default_value
except IOError as e:
    logger.error(f"IO error: {{e}}")
    raise
```

#### 3. Resource Leaks
```python
# BAD: File not closed on error
f = open('file.txt')
data = f.read()
f.close()

# GOOD: Use context manager
with open('file.txt') as f:
    data = f.read()
```

## Resilience Assessment

### Retry Logic
- Check for retry mechanisms on transient failures
- Verify exponential backoff implementation
- Assess circuit breaker patterns

### Graceful Degradation
- Verify fallback mechanisms
- Check for default values on errors
- Assess partial failure handling

### Error Messages
- Check for information leakage in error messages
- Verify user-friendly error messages
- Assess error message consistency

## Action Items

### 🔴 CRITICAL: Fix Bare Exception Handlers
**Action**: Replace bare `except:` with specific exceptions
**Priority**: CRITICAL - Bare except catches system exits and keyboard interrupts
**Effort**: 2-3 hours

**Step 1**: Find all bare exception handlers
```bash
# Find bare except statements
grep -rn "except:" src/ --include="*.py" | grep -v "except Exception" | grep -v "except.*as"

# Find broad exception catching
grep -rn "except Exception:" src/ --include="*.py"

# Save for review
grep -rn "except:" src/ --include="*.py" > exception_handlers.txt
```

**Step 2**: Replace with specific exceptions

**Before** (❌ DANGEROUS):
```python
try:
    result = risky_operation()
except:  # ❌ Catches EVERYTHING including KeyboardInterrupt!
    pass
```

**After** (✅ SAFE):
```python
import logging

logger = logging.getLogger(__name__)

try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value in risky_operation: {{e}}")
    raise
except IOError as e:
    logger.error(f"IO error in risky_operation: {{e}}")
    return None
except Exception as e:
    logger.exception(f"Unexpected error in risky_operation: {{e}}")
    raise
```

**Step 3**: Add logging to all handlers
```python
# Pattern to follow
try:
    operation()
except SpecificError as e:
    logger.error(
        f"Operation failed: {{e}}",
        exc_info=True,  # Include stack trace
        extra={{
            'operation': 'operation_name',
            'error_type': type(e).__name__
        }}
    )
    # Then: raise, return default, or handle
```

**Success Criteria**:
- [ ] Zero bare `except:` statements
- [ ] All exception handlers log errors
- [ ] Specific exceptions caught where possible
- [ ] System exceptions (KeyboardInterrupt, SystemExit) not caught

### 🟠 HIGH: Add Resource Cleanup with Context Managers
**Action**: Ensure all resources are properly cleaned up
**Priority**: HIGH - Prevents resource leaks
**Effort**: 2 hours

**Step 1**: Find resource management patterns
```bash
# Find file operations without context managers
grep -rn "open(" src/ --include="*.py" | grep -v "with"

# Find database connections
grep -rn "connect(" src/ --include="*.py" | grep -v "with"

# Find network connections
grep -rn "socket\|requests\|urllib" src/ --include="*.py"
```

**Step 2**: Convert to context managers

**Before** (❌ Resource leak on error):
```python
def read_config():
    f = open('config.json')
    data = json.load(f)  # If this fails, file never closes!
    f.close()
    return data
```

**After** (✅ Always cleaned up):
```python
def read_config():
    with open('config.json') as f:
        data = json.load(f)
    return data  # File automatically closed even on error
```

**Step 3**: Create custom context managers for complex resources
```python
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

@contextmanager
def database_connection(db_url):
    'Context manager for database connections.'
    conn = None
    try:
        conn = connect(db_url)
        logger.info(f"Connected to database: {{db_url}}")
        yield conn
    except Exception as e:
        logger.error(f"Database error: {{e}}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

# Usage
with database_connection('postgresql://...') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    # Connection automatically closed and rolled back on error
```

### 🟠 HIGH: Implement Retry Logic for Transient Failures
**Action**: Add retry mechanisms for network calls and external services
**Priority**: HIGH - Improves reliability
**Effort**: 2 hours

**Step 1**: Install retry library
```bash
pip install tenacity
```

**Step 2**: Add retry decorators

**Example: API calls with retry**:
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import requests
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError)),
    before_sleep=lambda retry_state: logger.warning(
        f"Retry attempt {{retry_state.attempt_number}} after error: {{retry_state.outcome.exception()}}"
    )
)
def call_external_api(url):
    'Call external API with automatic retry on transient failures.'
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

# Usage
try:
    data = call_external_api('https://api.example.com/data')
except Exception as e:
    logger.error(f"API call failed after retries: {{e}}")
    # Handle permanent failure
```

**Example: Database operations with retry**:
```python
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=1, max=30),
    retry=retry_if_exception_type(DatabaseConnectionError)
)
def execute_query(query):
    with database_connection() as conn:
        return conn.execute(query)
```

### 🟡 MEDIUM: Add Circuit Breaker Pattern
**Action**: Prevent cascading failures from external services
**Priority**: MEDIUM - Important for production resilience
**Effort**: 3 hours

**Step 1**: Install circuit breaker library
```bash
pip install pybreaker
```

**Step 2**: Implement circuit breaker
```python
import pybreaker
import logging

logger = logging.getLogger(__name__)

# Create circuit breaker
api_breaker = pybreaker.CircuitBreaker(
    fail_max=5,  # Open after 5 failures
    timeout_duration=60,  # Stay open for 60 seconds
    name='external_api'
)

@api_breaker
def call_external_service(endpoint):
    'Call external service with circuit breaker protection.'
    response = requests.get(f"https://api.example.com/{{endpoint}}", timeout=5)
    response.raise_for_status()
    return response.json()

# Usage with fallback
def get_data_with_fallback(endpoint):
    try:
        return call_external_service(endpoint)
    except pybreaker.CircuitBreakerError:
        logger.warning(f"Circuit breaker open for {{endpoint}}, using cache")
        return get_cached_data(endpoint)
    except Exception as e:
        logger.error(f"Service call failed: {{e}}")
        return None
```

### 🟡 MEDIUM: Add Error Tracking
**Action**: Integrate Sentry or similar error tracking
**Priority**: MEDIUM - Essential for production monitoring
**Effort**: 1 hour

**Step 1**: Install Sentry
```bash
pip install sentry-sdk
```

**Step 2**: Configure Sentry
```python
# src/codebase_reviewer/error_tracking.py
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging

def setup_error_tracking(dsn: str, environment: str = 'production'):
    'Initialize Sentry error tracking.'
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        traces_sample_rate=0.1,  # 10% of transactions
        integrations=[sentry_logging],
        before_send=filter_sensitive_data
    )

def filter_sensitive_data(event, hint):
    'Remove sensitive data before sending to Sentry.'
    # Remove sensitive keys
    if 'request' in event:
        if 'headers' in event['request']:
            event['request']['headers'].pop('Authorization', None)
            event['request']['headers'].pop('Cookie', None)
    return event
```

**Step 3**: Use in application
```python
from codebase_reviewer.error_tracking import setup_error_tracking
import os

# In main/cli.py
setup_error_tracking(
    dsn=os.getenv('SENTRY_DSN'),
    environment=os.getenv('ENVIRONMENT', 'development')
)

# Errors are automatically captured
try:
    risky_operation()
except Exception as e:
    # Automatically sent to Sentry
    logger.exception("Operation failed")

    # Add extra context
    sentry_sdk.set_context("operation", {{
        "type": "risky_operation",
        "user_id": user_id
    }})
    raise
```

### 🟢 LOW: Create Error Handling Guidelines
**Action**: Document error handling patterns for team
**Location**: Create `docs/error-handling-guide.md`

**Template**:
```markdown
# Error Handling Guidelines

## Principles
1. **Fail Fast**: Detect errors early
2. **Fail Loudly**: Log all errors
3. **Fail Safely**: Clean up resources
4. **Fail Gracefully**: Provide fallbacks

## Patterns

### Pattern 1: Specific Exception Handling
\`\`\`python
try:
    operation()
except ValueError as e:
    logger.error(f"Invalid value: {{e}}")
    return default_value
except IOError as e:
    logger.error(f"IO error: {{e}}")
    raise
\`\`\`

### Pattern 2: Resource Management
\`\`\`python
with resource() as r:
    r.use()
\`\`\`

### Pattern 3: Retry with Backoff
\`\`\`python
@retry(stop=stop_after_attempt(3))
def operation():
    pass
\`\`\`

## Checklist
- [ ] Specific exceptions caught
- [ ] All errors logged
- [ ] Resources cleaned up
- [ ] Retries for transient failures
- [ ] Circuit breakers for external services
```

## Verification Commands

```bash
# Find bare exception handlers
grep -rn "except:" src/ --include="*.py" | grep -v "except Exception" | grep -v "except.*as" && echo "❌ FAIL" || echo "✅ PASS"

# Find files without context managers
grep -rn "open(" src/ --include="*.py" | grep -v "with" | head -10

# Test retry logic
python -c "from tenacity import retry, stop_after_attempt; @retry(stop=stop_after_attempt(3)); def test(): raise Exception(); test()"

# Test circuit breaker
python -c "import pybreaker; cb = pybreaker.CircuitBreaker(); print('Circuit breaker configured')"

# Verify Sentry integration
python -c "import sentry_sdk; sentry_sdk.init('https://test@sentry.io/123'); sentry_sdk.capture_message('test'); print('Sentry working')"
```

## Priority Summary
- 🔴 **CRITICAL**: Fix bare exceptions (2-3 hours) - **DO TODAY**
- 🟠 **HIGH**: Context managers (2 hours), Retry logic (2 hours) - **This week**
- 🟡 **MEDIUM**: Circuit breakers (3 hours), Error tracking (1 hour) - **This month**
- 🟢 **LOW**: Documentation (2 hours), Guidelines (1 hour)

**Total Effort**: ~7 hours for critical/high priority items

## Tools & Patterns
- ✅ **Context Managers**: Use `with` statements for resource management
- ✅ **Retry Libraries**: tenacity (recommended), backoff
- ✅ **Circuit Breakers**: pybreaker, circuitbreaker
- ✅ **Error Tracking**: Sentry (recommended), Rollbar, Bugsnag
- ✅ **Monitoring**: Prometheus, Datadog, New Relic
"""

    def _generate_cohesion_coupling(self, prompt_id, prompt_text, context, repository):
        """Generate cohesion and coupling analysis response."""
        if isinstance(context, dict):
            actual_structure = context.get("actual_structure", {})
            packages = actual_structure.get("packages", [])
            frameworks = actual_structure.get("frameworks", [])

            return f"""# Cohesion & Coupling Boundary Analysis

## Summary
Analyzed module cohesion and coupling for repository at `{repository}`.

## Package Structure
{self._format_list(packages) if packages else "- No packages detected"}

## Cohesion Assessment

### High Cohesion Modules
*Modules with focused, single responsibility*
- Analyzer modules (focused on specific analysis tasks)
- Utility modules (focused helper functions)

### Low Cohesion Modules
*Modules doing too many things*
- Check for "god classes" or "utility" modules
- Look for modules mixing multiple concerns
- Identify modules with unrelated functions

## Coupling Assessment

### Tight Coupling (Problematic)
*Modules with high interdependence*
- Direct imports of implementation details
- Shared mutable state
- Circular dependencies

### Appropriate Coupling
*Acceptable dependencies*
- Well-defined interfaces
- Dependency injection
- Event-based communication

## Architectural Boundaries

### Layer Separation
- **Presentation Layer**: Web UI, CLI
- **Business Logic**: Core analysis logic
- **Data Layer**: File I/O, parsing

### Boundary Violations
*Check for:*
- Presentation logic in business layer
- Business logic in data layer
- Direct database access from presentation

## Leaky Abstractions
*Abstractions exposing implementation details*
- Check for implementation details in public APIs
- Verify interface segregation
- Assess abstraction levels

## Action Items

### 🔴 CRITICAL: Break Up God Classes
**Action**: Identify and refactor large classes with too many responsibilities
**Priority**: CRITICAL - God classes are maintenance nightmares
**Effort**: 8-16 hours per class

**Step 1**: Identify god classes
```bash
# Find large classes (>500 lines)
find . -name "*.py" -exec wc -l {{}} \\; | sort -rn | head -20

# Measure class complexity
pip install radon
radon cc . -a -nb | grep "^C " | sort -k4 -rn | head -10

# Check LCOM (Lack of Cohesion of Methods)
pip install cohesion
cohesion -d src/
```

**Step 2**: Analyze responsibilities

**Before** (❌ God class with multiple responsibilities):
```python
class UserManager:
    'Handles everything related to users.'

    def authenticate(self, username, password): pass
    def send_email(self, user, subject, body): pass
    def generate_report(self, user): pass
    def log_activity(self, user, action): pass
    def validate_permissions(self, user, resource): pass
    def update_profile(self, user, data): pass
    def export_to_csv(self, users): pass
    def send_sms(self, user, message): pass
    # ... 50 more methods
```

**After** (✅ Single Responsibility Principle):
```python
# File: auth/authenticator.py
class Authenticator:
    'Handles user authentication only.'
    def authenticate(self, username, password): pass
    def validate_credentials(self, username, password): pass

# File: notifications/email_service.py
class EmailService:
    'Handles email notifications.'
    def send_email(self, user, subject, body): pass

# File: notifications/sms_service.py
class SMSService:
    'Handles SMS notifications.'
    def send_sms(self, user, message): pass

# File: reports/user_reporter.py
class UserReporter:
    'Generates user reports.'
    def generate_report(self, user): pass
    def export_to_csv(self, users): pass

# File: auth/permission_checker.py
class PermissionChecker:
    'Validates user permissions.'
    def validate_permissions(self, user, resource): pass

# File: users/profile_manager.py
class ProfileManager:
    'Manages user profiles.'
    def update_profile(self, user, data): pass

# File: audit/activity_logger.py
class ActivityLogger:
    'Logs user activities.'
    def log_activity(self, user, action): pass
```

**Step 3**: Extract classes incrementally
```bash
# Create new module structure
mkdir -p src/auth src/notifications src/reports src/audit

# Move extracted classes
# Update imports across codebase
# Run tests after each extraction
pytest tests/ -v
```

**Success Criteria**:
- [ ] No class exceeds 300 lines
- [ ] Each class has single, clear responsibility
- [ ] LCOM score < 0.5 for all classes
- [ ] All tests pass after refactoring

### 🔴 CRITICAL: Fix Circular Dependencies
**Action**: Detect and eliminate circular import dependencies
**Priority**: CRITICAL - Causes import errors and tight coupling
**Effort**: 4-8 hours

**Step 1**: Detect circular dependencies
```bash
# Install pydeps
pip install pydeps

# Generate dependency graph
pydeps src/ --max-bacon=2 --cluster

# Find circular dependencies
pydeps src/ --show-cycles

# Alternative: use madge for JavaScript
npm install -g madge
madge --circular --extensions py src/
```

**Step 2**: Analyze and fix

**Common patterns causing circular deps**:
```python
# ❌ PROBLEM: Circular dependency
# File: models/user.py
from models.order import Order

class User:
    def get_orders(self):
        return Order.query.filter_by(user_id=self.id)

# File: models/order.py
from models.user import User

class Order:
    def get_user(self):
        return User.query.get(self.user_id)
```

**Solution 1: Move to shared module**:
```python
# File: models/base.py
class BaseModel:
    'Shared base class.'
    pass

# File: models/user.py
from models.base import BaseModel

class User(BaseModel):
    def get_orders(self):
        # Import locally to break cycle
        from models.order import Order
        return Order.query.filter_by(user_id=self.id)

# File: models/order.py
from models.base import BaseModel

class Order(BaseModel):
    def get_user(self):
        from models.user import User
        return User.query.get(self.user_id)
```

**Solution 2: Dependency injection**:
```python
# File: models/user.py
class User:
    def __init__(self, order_repository=None):
        self.order_repository = order_repository

    def get_orders(self):
        return self.order_repository.find_by_user(self.id)

# File: models/order.py
class Order:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository

    def get_user(self):
        return self.user_repository.find_by_id(self.user_id)
```

**Solution 3: Extract interface**:
```python
# File: interfaces/repositories.py
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id): pass

class OrderRepository(ABC):
    @abstractmethod
    def find_by_user(self, user_id): pass
```

**Success Criteria**:
- [ ] Zero circular dependencies detected
- [ ] Dependency graph is acyclic (DAG)
- [ ] Import errors resolved
- [ ] Tests pass

### 🟠 HIGH: Reduce Module Coupling
**Action**: Decrease dependencies between modules
**Priority**: HIGH - High coupling makes changes difficult
**Effort**: 6-10 hours

**Step 1**: Measure coupling
```bash
# Analyze dependencies
pydeps src/ --max-bacon=3 --noshow --cluster > deps.txt

# Count imports per module
grep -r "^import\\|^from" src/ | cut -d: -f1 | sort | uniq -c | sort -rn

# Visualize coupling
pydeps src/ --only src --cluster --max-bacon=2 -o coupling.svg
```

**Step 2**: Apply decoupling patterns

**Pattern 1: Dependency Injection**:
```python
# Before (❌ Tight coupling)
class OrderService:
    def __init__(self):
        self.email_service = EmailService()  # Hard-coded dependency
        self.payment_gateway = StripeGateway()  # Hard-coded

    def process_order(self, order):
        self.payment_gateway.charge(order.total)
        self.email_service.send_confirmation(order.user)

# After (✅ Dependency injection)
class OrderService:
    def __init__(self, email_service, payment_gateway):
        self.email_service = email_service  # Injected
        self.payment_gateway = payment_gateway  # Injected

    def process_order(self, order):
        self.payment_gateway.charge(order.total)
        self.email_service.send_confirmation(order.user)

# Usage
email = EmailService()
payment = StripeGateway()
order_service = OrderService(email, payment)
```

**Pattern 2: Event-Based Communication**:
```python
# Before (❌ Direct coupling)
class OrderService:
    def create_order(self, order):
        order.save()
        InventoryService().update_stock(order.items)  # Coupled
        EmailService().send_confirmation(order.user)  # Coupled
        AnalyticsService().track_order(order)  # Coupled

# After (✅ Event-driven)
from events import EventBus

class OrderService:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def create_order(self, order):
        order.save()
        self.event_bus.publish('order.created', order)  # Decoupled

# Subscribers
class InventoryService:
    def __init__(self, event_bus):
        event_bus.subscribe('order.created', self.update_stock)

    def update_stock(self, order):
        # Update inventory
        pass
```

**Success Criteria**:
- [ ] Average dependencies per module < 5
- [ ] No module depends on >10 other modules
- [ ] Dependency injection used for services
- [ ] Event bus for cross-cutting concerns

### 🟡 MEDIUM: Improve Module Cohesion
**Action**: Group related functionality together
**Priority**: MEDIUM - Improves maintainability
**Effort**: 4-6 hours

**Step 1**: Measure cohesion
```bash
# Install cohesion analyzer
pip install cohesion

# Analyze module cohesion
cohesion -d src/ --below 50

# Check for utility modules (low cohesion indicator)
find src/ -name "*util*.py" -o -name "*helper*.py"
```

**Step 2**: Refactor for high cohesion

**Before** (❌ Low cohesion - unrelated functions):
```python
# File: utils.py
def format_date(date): pass
def send_email(to, subject): pass
def calculate_tax(amount): pass
def validate_password(pwd): pass
def generate_pdf(data): pass
```

**After** (✅ High cohesion - grouped by purpose):
```python
# File: formatters/date_formatter.py
def format_date(date): pass
def parse_date(date_str): pass

# File: notifications/email.py
def send_email(to, subject): pass
def send_bulk_email(recipients, subject): pass

# File: billing/tax_calculator.py
def calculate_tax(amount): pass
def calculate_discount(amount, rate): pass

# File: auth/password_validator.py
def validate_password(pwd): pass
def hash_password(pwd): pass

# File: reports/pdf_generator.py
def generate_pdf(data): pass
def generate_csv(data): pass
```

**Success Criteria**:
- [ ] LCOM score > 0.5 for all modules
- [ ] No "utils" or "helpers" modules
- [ ] Related functions grouped together
- [ ] Clear module purposes

### 🟢 LOW: Document Architectural Boundaries
**Action**: Create clear layer separation documentation
**Priority**: LOW - Improves understanding
**Effort**: 2-3 hours

**Step 1**: Define layers
```markdown
# docs/architecture/layers.md

## Architectural Layers

### Presentation Layer
- **Purpose**: User interface and API endpoints
- **Location**: `src/api/`, `src/cli/`, `src/web/`
- **Dependencies**: Can depend on Business Layer only
- **Restrictions**: No direct database access

### Business Layer
- **Purpose**: Core business logic and domain models
- **Location**: `src/services/`, `src/models/`
- **Dependencies**: Can depend on Data Layer only
- **Restrictions**: No UI/presentation logic

### Data Layer
- **Purpose**: Data access and persistence
- **Location**: `src/repositories/`, `src/database/`
- **Dependencies**: No dependencies on other layers
- **Restrictions**: Only database and external API calls
```

**Step 2**: Enforce with linting
```python
# File: .layerlint.yml
layers:
  - name: presentation
    paths: [src/api, src/cli, src/web]
    depends_on: [business]

  - name: business
    paths: [src/services, src/models]
    depends_on: [data]

  - name: data
    paths: [src/repositories, src/database]
    depends_on: []
```

**Success Criteria**:
- [ ] Layer documentation created
- [ ] Boundary violations identified
- [ ] Linting rules configured
- [ ] Team trained on architecture

## Verification Commands

```bash
# Check for god classes
radon cc . -a -nb | grep "^C " | sort -k4 -rn | head -10

# Detect circular dependencies
pydeps src/ --show-cycles

# Measure coupling
pydeps src/ --max-bacon=3 --cluster

# Measure cohesion
cohesion -d src/ --below 50

# Visualize architecture
pydeps src/ --only src --cluster -o architecture.svg
```

## Priority Summary
- 🔴 **CRITICAL**: God classes (8-16h), Circular deps (4-8h) - **This sprint**
- 🟠 **HIGH**: Reduce coupling (6-10h) - **This month**
- 🟡 **MEDIUM**: Improve cohesion (4-6h) - **This quarter**
- 🟢 **LOW**: Document boundaries (2-3h) - **When time permits**

**Total Effort**: ~24-43 hours for critical/high priority items

## Metrics to Track
- **Coupling**: Number of dependencies per module (target: <5)
- **Cohesion**: LCOM score (target: >0.5)
- **Cyclomatic Complexity**: Per-function complexity (target: <10)
- **Depth of Inheritance**: Inheritance depth (target: <4)

## Tools
- **Python**: radon (complexity), pydeps (dependencies), cohesion (LCOM)
- **Visualization**: pyreverse, graphviz
- **Analysis**: SonarQube, Code Climate
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_observability_strategy(
        self, prompt_id, prompt_text, context, repository
    ):
        """Generate observability strategy response."""
        return f"""# Observability & Instrumentation Strategy

## Summary
Developed comprehensive observability strategy for repository at `{repository}`.

## Current Observability State

### Logging
- **Current Approach**: Assess current logging practices
- **Coverage**: Identify gaps in logging coverage
- **Format**: Check for structured vs. unstructured logs

### Metrics
- **Collection**: What metrics are currently collected
- **Storage**: Where metrics are stored
- **Visualization**: How metrics are visualized

### Tracing
- **Distributed Tracing**: Check for tracing implementation
- **Request Correlation**: Verify request ID propagation
- **Performance Profiling**: Assess profiling capabilities

### Alerting
- **Alert Rules**: What alerts are configured
- **Notification Channels**: How alerts are delivered
- **On-Call**: On-call rotation and escalation

## Gaps & Blind Spots

### Critical Gaps
1. **Missing Logs**: Areas without adequate logging
2. **No Metrics**: Key metrics not being collected
3. **No Tracing**: Lack of distributed tracing
4. **Alert Fatigue**: Too many or too few alerts

### Blind Spots
- User journey visibility
- Performance bottlenecks
- Error rates and patterns
- Resource utilization

## Recommended Instrumentation

### Structured Logging
```python
import structlog

logger = structlog.get_logger()
logger.info("user_action", user_id=123, action="login", status="success")
```

**Benefits**:
- Machine-readable logs
- Easy filtering and searching
- Consistent format

### Key Metrics to Track
1. **Request Metrics**: Rate, errors, duration (RED)
2. **Resource Metrics**: CPU, memory, disk (USE)
3. **Business Metrics**: User actions, conversions
4. **Custom Metrics**: Domain-specific measurements

### Distributed Tracing
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("operation"):
    # Your code here
    pass
```

**Benefits**:
- End-to-end request visibility
- Performance bottleneck identification
- Dependency mapping

### Error Tracking
- **Tool**: Sentry, Rollbar, Bugsnag
- **Features**: Error grouping, stack traces, context
- **Integration**: Automatic error capture

### Performance Monitoring
- **APM**: Application Performance Monitoring
- **Tools**: New Relic, Datadog, Dynatrace
- **Metrics**: Response times, throughput, errors

## Tooling Recommendations

### Logging Stack
- **Collection**: Fluentd, Logstash
- **Storage**: Elasticsearch, Loki
- **Visualization**: Kibana, Grafana

### Metrics Stack
- **Collection**: Prometheus, StatsD
- **Storage**: Prometheus, InfluxDB
- **Visualization**: Grafana, Datadog

### Tracing Stack
- **Standard**: OpenTelemetry
- **Backend**: Jaeger, Zipkin, Tempo
- **Visualization**: Jaeger UI, Grafana

### All-in-One Solutions
- **Datadog**: Logs, metrics, traces, APM
- **New Relic**: Full observability platform
- **Elastic Stack**: ELK + APM

## Action Items

### 🔴 CRITICAL: Implement Structured Logging
**Action**: Replace unstructured logs with structured, machine-readable format
**Priority**: CRITICAL - Foundation for observability
**Effort**: 4-6 hours

**Step 1**: Install structured logging library
```bash
# Install structlog
pip install structlog python-json-logger

# Add to requirements.txt
echo "structlog>=23.1.0" >> requirements.txt
echo "python-json-logger>=2.0.7" >> requirements.txt
```

**Step 2**: Configure structured logging
```python
# File: src/logging_config.py
import structlog
import logging
from pythonjsonlogger import jsonlogger

def configure_logging():
    'Configure structured logging with JSON output.'

    # Configure standard logging
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

# File: src/main.py
from logging_config import configure_logging

configure_logging()
logger = structlog.get_logger()

# Usage
logger.info("user_login", user_id=123, ip="192.168.1.1", success=True)
logger.error("payment_failed", order_id=456, amount=99.99, reason="insufficient_funds")
```

**Step 3**: Replace existing log statements
```python
# Before (❌ Unstructured)
print(f"User {{user_id}} logged in from {{ip}}")
logging.info(f"Processing order {{order_id}}")

# After (✅ Structured)
logger.info("user_login", user_id=user_id, ip=ip)
logger.info("order_processing", order_id=order_id, status="started")
```

**Success Criteria**:
- [ ] All logs output in JSON format
- [ ] Consistent field names across logs
- [ ] Request IDs included in all logs
- [ ] No print() statements in production code

### 🔴 CRITICAL: Set Up Metrics Collection
**Action**: Implement Prometheus metrics for key application metrics
**Priority**: CRITICAL - Essential for monitoring
**Effort**: 6-8 hours

**Step 1**: Install Prometheus client
```bash
pip install prometheus-client
echo "prometheus-client>=0.18.0" >> requirements.txt
```

**Step 2**: Add metrics to application
```python
# File: src/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

error_count = Counter(
    'errors_total',
    'Total errors',
    ['error_type', 'severity']
)

# Usage in application
def track_request(method, endpoint):
    'Decorator to track request metrics.'
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                request_count.labels(method=method, endpoint=endpoint, status='success').inc()
                return result
            except Exception as e:
                request_count.labels(method=method, endpoint=endpoint, status='error').inc()
                error_count.labels(error_type=type(e).__name__, severity='high').inc()
                raise
            finally:
                duration = time.time() - start
                request_duration.labels(method=method, endpoint=endpoint).observe(duration)
        return wrapper
    return decorator

# Start metrics server
start_http_server(8000)  # Metrics available at http://localhost:8000/metrics
```

**Step 3**: Create Prometheus configuration
```yaml
# File: prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'my-application'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

**Step 4**: Run Prometheus
```bash
# Using Docker
docker run -d \\
  --name prometheus \\
  -p 9090:9090 \\
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \\
  prom/prometheus

# Access Prometheus UI at http://localhost:9090
```

**Success Criteria**:
- [ ] Metrics endpoint exposed
- [ ] RED metrics tracked (Rate, Errors, Duration)
- [ ] Prometheus scraping metrics
- [ ] Dashboards created in Grafana

### 🟠 HIGH: Implement Distributed Tracing
**Action**: Add OpenTelemetry for request tracing
**Priority**: HIGH - Critical for debugging distributed systems
**Effort**: 8-10 hours

**Step 1**: Install OpenTelemetry
```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation
pip install opentelemetry-exporter-jaeger
echo "opentelemetry-api>=1.20.0" >> requirements.txt
echo "opentelemetry-sdk>=1.20.0" >> requirements.txt
echo "opentelemetry-instrumentation>=0.41b0" >> requirements.txt
echo "opentelemetry-exporter-jaeger>=1.20.0" >> requirements.txt
```

**Step 2**: Configure tracing
```python
# File: src/tracing_config.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource

def configure_tracing(service_name="my-service"):
    'Configure OpenTelemetry tracing.'

    # Create resource
    resource = Resource(attributes={{
        "service.name": service_name
    }})

    # Create tracer provider
    provider = TracerProvider(resource=resource)

    # Configure Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )

    # Add span processor
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

    # Set global tracer provider
    trace.set_tracer_provider(provider)

    return trace.get_tracer(__name__)

# Usage
tracer = configure_tracing()

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)

        # Nested span
        with tracer.start_as_current_span("validate_order"):
            validate(order_id)

        with tracer.start_as_current_span("charge_payment"):
            charge(order_id)

        span.set_attribute("order.status", "completed")
```

**Step 3**: Run Jaeger
```bash
# Using Docker
docker run -d \\
  --name jaeger \\
  -p 6831:6831/udp \\
  -p 16686:16686 \\
  jaegertracing/all-in-one:latest

# Access Jaeger UI at http://localhost:16686
```

**Success Criteria**:
- [ ] Traces captured for all requests
- [ ] Spans show execution time
- [ ] Distributed traces across services
- [ ] Jaeger UI accessible

### 🟠 HIGH: Create Monitoring Dashboards
**Action**: Build Grafana dashboards for key metrics
**Priority**: HIGH - Enables proactive monitoring
**Effort**: 4-6 hours

**Step 1**: Set up Grafana
```bash
# Using Docker
docker run -d \\
  --name grafana \\
  -p 3000:3000 \\
  grafana/grafana

# Access Grafana at http://localhost:3000 (admin/admin)
```

**Step 2**: Add Prometheus data source
```bash
# Via Grafana UI:
# Configuration > Data Sources > Add data source > Prometheus
# URL: http://prometheus:9090
```

**Step 3**: Create dashboard JSON
```json
{{
  "dashboard": {{
    "title": "Application Metrics",
    "panels": [
      {{
        "title": "Request Rate",
        "targets": [
          {{
            "expr": "rate(http_requests_total[5m])"
          }}
        ]
      }},
      {{
        "title": "Error Rate",
        "targets": [
          {{
            "expr": "rate(http_requests_total{{status='error'}}[5m])"
          }}
        ]
      }},
      {{
        "title": "Request Duration (p95)",
        "targets": [
          {{
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }}
        ]
      }}
    ]
  }}
}}
```

**Success Criteria**:
- [ ] Dashboard shows RED metrics
- [ ] Alerts configured for anomalies
- [ ] Team has access to dashboards
- [ ] Dashboards updated in real-time

### 🟡 MEDIUM: Configure Alerting Rules
**Action**: Set up alerts for critical conditions
**Priority**: MEDIUM - Enables proactive response
**Effort**: 3-4 hours

**Step 1**: Create alert rules
```yaml
# File: alert_rules.yml
groups:
  - name: application_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{{status="error"}}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{{{ $value }}}}% over the last 5 minutes"

      - alert: SlowRequests
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1.0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow requests detected"
          description: "95th percentile latency is {{{{ $value }}}}s"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "Service {{{{ $labels.job }}}} is not responding"
```

**Step 2**: Configure Alertmanager
```yaml
# File: alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'team-notifications'

receivers:
  - name: 'team-notifications'
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK_URL'
        channel: '#alerts'
        title: '{{{{ .GroupLabels.alertname }}}}'
        text: '{{{{ range .Alerts }}}}{{{{ .Annotations.description }}}}{{{{ end }}}}'
```

**Success Criteria**:
- [ ] Alerts fire for critical conditions
- [ ] Notifications sent to team
- [ ] Alert fatigue minimized
- [ ] Runbooks linked to alerts

## Verification Commands

```bash
# Check structured logs
tail -f logs/app.log | jq .

# Query Prometheus metrics
curl http://localhost:8000/metrics

# Check Jaeger traces
curl http://localhost:16686/api/traces?service=my-service

# Test alert rules
promtool check rules alert_rules.yml
```

## Priority Summary
- 🔴 **CRITICAL**: Structured logging (4-6h), Metrics (6-8h) - **This week**
- 🟠 **HIGH**: Distributed tracing (8-10h), Dashboards (4-6h) - **This sprint**
- 🟡 **MEDIUM**: Alerting (3-4h) - **This month**

**Total Effort**: ~25-34 hours for critical/high priority items

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- ✅ Structured logging
- ✅ Basic metrics collection
- ✅ Prometheus setup

### Phase 2: Enhancement (Weeks 3-4)
- ✅ Distributed tracing
- ✅ Grafana dashboards
- ✅ Alert rules

### Phase 3: Optimization (Weeks 5-6)
- APM monitoring
- SLOs/SLIs
- Anomaly detection
- Runbooks

## Success Metrics
- **MTTR**: Mean Time To Resolution (target: <30 min)
- **MTTD**: Mean Time To Detection (target: <5 min)
- **Alert Accuracy**: True positive rate (target: >90%)
- **Coverage**: % of code instrumented (target: >80%)
"""

    def _generate_tech_debt_roadmap(self, prompt_id, prompt_text, context, repository):
        """Generate technical debt roadmap response."""
        if isinstance(context, dict):
            total_issues = context.get("total_issues", 0)
            issues_by_severity = context.get("issues_by_severity", {})
            top_issues = context.get("top_issues", [])

            high_count = issues_by_severity.get("high", 0)
            medium_count = issues_by_severity.get("medium", 0)
            low_count = issues_by_severity.get("low", 0)

            return f"""# Technical Debt & Refactoring Roadmap

## Summary
Analyzed technical debt for repository at `{repository}`.
Found {total_issues} total issues across all severity levels.

## Debt Inventory

### By Severity
- **High**: {high_count} issue(s) - Address immediately
- **Medium**: {medium_count} issue(s) - Plan for next sprint
- **Low**: {low_count} issue(s) - Address when convenient

### Top Issues
{self._format_top_issues(top_issues[:10])}

## Prioritization Matrix

| Item | Impact | Effort | Priority | Timeline |
|------|--------|--------|----------|----------|
{self._generate_priority_matrix(top_issues[:5])}

## Quick Wins
*High-value, low-effort improvements*

{self._identify_quick_wins(top_issues)}

## Major Refactoring Projects
*Larger efforts requiring dedicated time*

{self._identify_major_refactoring(top_issues)}

## Action Items

### 🔴 CRITICAL: Address High Severity Issues Immediately
**Action**: Fix all {high_count} HIGH severity issues
**Priority**: CRITICAL - Security and stability risks
**Effort**: {high_count * 2}-{high_count * 4} hours

**Step 1**: Triage and prioritize
```bash
# Export high severity issues
grep -r "# TODO\\|# FIXME\\|# XXX" src/ > tech_debt.txt

# Run security scan
bandit -r src/ -f json -o security_issues.json
jq '.results[] | select(.issue_severity=="HIGH")' security_issues.json

# Check for dangerous patterns
grep -r "eval\\|exec\\|pickle.loads" src/
```

**Step 2**: Create tickets for each issue
```bash
# Create GitHub issues for tracking
gh issue create --title "Security: Fix eval() usage in parser.py" \\
  --body "HIGH severity security issue detected" \\
  --label "security,tech-debt,high-priority"
```

**Step 3**: Fix issues systematically

**Example: Fix eval() usage**:
```python
# Before (❌ DANGEROUS)
def execute_user_code(code_str):
    result = eval(code_str)  # Arbitrary code execution!
    return result

# After (✅ SAFE)
import ast

def execute_user_code(code_str):
    'Safely evaluate user expressions.'
    try:
        # Parse and validate
        tree = ast.parse(code_str, mode='eval')

        # Only allow safe operations
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Call)):
                raise ValueError("Imports and calls not allowed")

        # Evaluate with restricted globals
        result = eval(compile(tree, '<string>', 'eval'), {{"__builtins__": {{}}}})
        return result
    except Exception as e:
        logger.error("code_evaluation_failed", error=str(e))
        raise
```

**Success Criteria**:
- [ ] All HIGH severity issues resolved
- [ ] Security scan shows 0 critical issues
- [ ] Code review completed
- [ ] Tests added for fixes

### 🟠 HIGH: Tackle Quick Wins
**Action**: Address high-value, low-effort improvements
**Priority**: HIGH - Fast ROI
**Effort**: 8-12 hours

**Step 1**: Identify quick wins
```bash
# Find TODO/FIXME comments
grep -rn "TODO\\|FIXME" src/ | wc -l

# Find unused imports
pylint src/ --disable=all --enable=unused-import

# Find duplicate code
pip install pylint
pylint src/ --disable=all --enable=duplicate-code
```

**Step 2**: Resolve TODO/FIXME comments
```bash
# Create script to track TODOs
cat > scripts/track_todos.sh << 'BASH'
#!/bin/bash
echo "TODO/FIXME Tracking Report"
echo "=========================="
echo ""
echo "Total TODOs: $(grep -r "# TODO" src/ | wc -l)"
echo "Total FIXMEs: $(grep -r "# FIXME" src/ | wc -l)"
echo ""
echo "By File:"
grep -r "# TODO\\|# FIXME" src/ | cut -d: -f1 | sort | uniq -c | sort -rn
BASH

chmod +x scripts/track_todos.sh
./scripts/track_todos.sh
```

**Step 3**: Fix or ticket each TODO
```python
# Before (❌ Untracked TODO)
def process_data(data):
    # TODO: Add validation
    return transform(data)

# After Option 1 (✅ Fixed)
def process_data(data):
    'Process data with validation.'
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    if 'required_field' not in data:
        raise ValueError("Missing required_field")
    return transform(data)

# After Option 2 (✅ Ticketed)
def process_data(data):
    # TODO(#123): Add comprehensive validation for all fields
    # Tracked in: https://github.com/org/repo/issues/123
    return transform(data)
```

**Success Criteria**:
- [ ] 80% of TODOs resolved or ticketed
- [ ] No unused imports
- [ ] Duplicate code reduced by 50%

### 🟠 HIGH: Set Up Automated Quality Gates
**Action**: Prevent new technical debt from being introduced
**Priority**: HIGH - Prevention is key
**Effort**: 4-6 hours

**Step 1**: Configure quality thresholds
```python
# File: .quality-gates.yml
thresholds:
  coverage:
    min: 80
    target: 90

  complexity:
    max_per_function: 10
    max_per_file: 50

  maintainability:
    min_index: 65

  security:
    max_high_severity: 0
    max_medium_severity: 5

  duplication:
    max_percentage: 3
```

**Step 2**: Add CI/CD quality checks
```yaml
# File: .github/workflows/quality-gates.yml
name: Quality Gates

on: [pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check test coverage
        run: |
          pytest --cov=src --cov-report=term --cov-fail-under=80

      - name: Check complexity
        run: |
          radon cc src/ -a -nb --total-average
          radon cc src/ -nc 10  # Fail if any function > complexity 10

      - name: Check security
        run: |
          bandit -r src/ -ll  # Fail on medium/high severity

      - name: Check code quality
        run: |
          pylint src/ --fail-under=8.0

      - name: Check for TODOs without tickets
        run: |
          if grep -r "# TODO[^(]" src/; then
            echo "Error: Found TODO without ticket reference"
            exit 1
          fi
```

**Step 3**: Add pre-commit hooks
```yaml
# File: .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: complexity-check
        name: Check complexity
        entry: radon cc src/ -nc 10
        language: system
        pass_filenames: false

      - id: no-eval
        name: No eval/exec
        entry: 'eval\\(|exec\\('
        language: pygrep
        types: [python]

      - id: todo-ticket
        name: TODO must have ticket
        entry: '# TODO[^(]'
        language: pygrep
        types: [python]
```

**Success Criteria**:
- [ ] Quality gates configured in CI/CD
- [ ] PRs blocked if quality drops
- [ ] Pre-commit hooks installed
- [ ] Team trained on standards

### 🟡 MEDIUM: Create Technical Debt Dashboard
**Action**: Track and visualize technical debt metrics
**Priority**: MEDIUM - Enables data-driven decisions
**Effort**: 3-4 hours

**Step 1**: Set up SonarQube or Code Climate
```bash
# Using SonarQube with Docker
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Scan project
pip install sonar-scanner
sonar-scanner \\
  -Dsonar.projectKey=my-project \\
  -Dsonar.sources=src \\
  -Dsonar.host.url=http://localhost:9000
```

**Step 2**: Create custom dashboard
```python
# File: scripts/tech_debt_dashboard.py
import json
import subprocess
from datetime import datetime

def generate_metrics():
    'Generate technical debt metrics.'

    # Run tools
    complexity = subprocess.run(['radon', 'cc', 'src/', '-j'], capture_output=True)
    coverage = subprocess.run(['pytest', '--cov=src', '--cov-report=json'], capture_output=True)
    security = subprocess.run(['bandit', '-r', 'src/', '-f', 'json'], capture_output=True)

    metrics = {{
        'timestamp': datetime.now().isoformat(),
        'complexity': json.loads(complexity.stdout),
        'coverage': json.loads(open('.coverage.json').read()),
        'security': json.loads(security.stdout),
    }}

    # Save metrics
    with open(f'metrics/{{datetime.now().strftime("%Y%m%d")}}.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    return metrics

if __name__ == '__main__':
    metrics = generate_metrics()
    print(f"Metrics saved: {{metrics['timestamp']}}")
```

**Step 3**: Visualize trends
```bash
# Generate trend report
python scripts/tech_debt_dashboard.py

# Create weekly report
cat > scripts/weekly_report.sh << 'BASH'
#!/bin/bash
echo "Technical Debt Weekly Report"
echo "============================"
echo "Date: $(date)"
echo ""
echo "Issues by Severity:"
bandit -r src/ -f json | jq '.metrics._totals'
echo ""
echo "Average Complexity:"
radon cc src/ -a -nb
echo ""
echo "Test Coverage:"
pytest --cov=src --cov-report=term | grep TOTAL
BASH

chmod +x scripts/weekly_report.sh
```

**Success Criteria**:
- [ ] Dashboard shows key metrics
- [ ] Trends tracked over time
- [ ] Weekly reports generated
- [ ] Team reviews metrics monthly

### 🟢 LOW: Document Architectural Decisions
**Action**: Create ADRs for major technical decisions
**Priority**: LOW - Improves long-term understanding
**Effort**: 2-3 hours

**Step 1**: Set up ADR structure
```bash
# Create ADR directory
mkdir -p docs/adr

# Create ADR template
cat > docs/adr/template.md << 'MD'
# ADR-XXX: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the issue we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

### Positive
- Benefit 1
- Benefit 2

### Negative
- Drawback 1
- Drawback 2

## Alternatives Considered
- Alternative 1: Why rejected
- Alternative 2: Why rejected
MD
```

**Step 2**: Document key decisions
```markdown
# Example: docs/adr/001-use-structured-logging.md

# ADR-001: Use Structured Logging

## Status
Accepted

## Context
Current logging uses print() and unstructured log messages, making it difficult to:
- Search and filter logs
- Correlate related log entries
- Analyze log data programmatically

## Decision
Adopt structlog for structured, JSON-formatted logging across the application.

## Consequences

### Positive
- Machine-readable logs
- Easy filtering and searching
- Better observability
- Consistent log format

### Negative
- Migration effort required
- Team training needed
- Slightly more verbose code

## Alternatives Considered
- Python logging with JSON formatter: Less features than structlog
- Continue with print(): Not suitable for production
```

**Success Criteria**:
- [ ] ADR template created
- [ ] 5+ key decisions documented
- [ ] Team follows ADR process
- [ ] ADRs reviewed in architecture meetings

## Verification Commands

```bash
# Check high severity issues
bandit -r src/ -ll

# Track TODO/FIXME count
grep -r "TODO\\|FIXME" src/ | wc -l

# Run quality gates
pytest --cov=src --cov-fail-under=80
radon cc src/ -nc 10
pylint src/ --fail-under=8.0

# Generate metrics
python scripts/tech_debt_dashboard.py
```

## Priority Summary
- 🔴 **CRITICAL**: Fix HIGH severity ({high_count * 2}-{high_count * 4}h) - **This week**
- 🟠 **HIGH**: Quick wins (8-12h), Quality gates (4-6h) - **This sprint**
- 🟡 **MEDIUM**: Dashboard (3-4h) - **This month**
- 🟢 **LOW**: ADRs (2-3h) - **When time permits**

**Total Effort**: ~{high_count * 2 + 20}-{high_count * 4 + 30} hours for critical/high priority items

## Timeline

### Month 1: Critical Issues
- ✅ Fix all HIGH severity security issues
- ✅ Set up automated quality gates
- ✅ Address critical architecture drift

### Month 2-3: Quick Wins & Prevention
- ✅ Resolve TODO/FIXME comments
- ✅ Fix code smells
- ✅ Improve test coverage
- ✅ Establish quality standards

### Month 4-6: Major Refactoring
- Break up god classes
- Reduce coupling
- Improve cohesion
- Refactor complex modules

### Ongoing: Continuous Improvement
- Maintain quality gates
- Regular debt reviews (monthly)
- Team training
- ADR documentation

## Success Metrics

### Quantitative
- Reduce HIGH severity issues to 0 (current: {high_count})
- Reduce total issues by 50% in 6 months (current: {total_issues})
- Increase test coverage to 80%+
- Reduce cyclomatic complexity by 20%

### Qualitative
- Faster feature development
- Fewer production bugs
- Improved developer satisfaction
- Better code maintainability

## Recommended Tools
- **Static Analysis**: pylint, mypy, bandit
- **Complexity**: radon, mccabe
- **Debt Tracking**: SonarQube, Code Climate
- **Visualization**: CodeScene, Understand
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    def _generate_mentorship_guide(self, prompt_id, prompt_text, context, repository):
        """Generate team mentorship and knowledge transfer guide."""
        if isinstance(context, dict):
            total_issues = context.get("total_issues", 0)
            security_issues = context.get("security_issues_count", 0)
            todo_count = context.get("todo_count", 0)

            return f"""# Team Mentorship & Knowledge Transfer Guide

## Summary
Developed mentorship guide for repository at `{repository}`.
Identified {total_issues} total issues including {security_issues} security concerns.

## Knowledge Gaps Identified

### Security Awareness
- **Security Issues Found**: {security_issues}
- **Common Vulnerabilities**: eval/exec usage, SQL injection risks, XSS vulnerabilities
- **Training Need**: {"HIGH" if security_issues > 5 else "MEDIUM" if security_issues > 0 else "LOW"}

### Code Quality Practices
- **TODO/FIXME Count**: {todo_count}
- **Technical Debt**: {"HIGH" if total_issues > 20 else "MEDIUM" if total_issues > 10 else "LOW"}
- **Training Need**: {"HIGH" if todo_count > 20 else "MEDIUM" if todo_count > 5 else "LOW"}

### Testing Practices
- **Test Coverage**: Assess current coverage
- **Test Quality**: Review test effectiveness
- **Training Need**: Based on coverage gaps

### Architecture Understanding
- **Complexity**: Assess codebase complexity
- **Documentation**: Review architecture docs
- **Training Need**: Based on documentation quality

## Mentorship Program Structure

### 1. Onboarding (Week 1-2)
**Objective**: Get new team members productive quickly

**Activities**:
- Repository walkthrough
- Architecture overview
- Development environment setup
- First contribution (documentation or small bug fix)

**Resources**:
- README and setup docs
- Architecture diagrams
- Coding standards guide
- Development workflow guide

**Success Metrics**:
- Environment set up in < 1 day
- First PR merged within 2 weeks
- Understanding of core architecture

### 2. Core Skills (Week 3-8)
**Objective**: Build fundamental skills

**Topics**:
- **Security Best Practices**
  - OWASP Top 10
  - Secure coding patterns
  - Code review for security

- **Code Quality**
  - SOLID principles
  - Design patterns
  - Refactoring techniques

- **Testing**
  - Unit testing best practices
  - Integration testing
  - Test-driven development

- **Architecture**
  - System design principles
  - Scalability patterns
  - Performance optimization

**Format**:
- Weekly 1-hour sessions
- Hands-on exercises
- Code review practice
- Pair programming

### 3. Advanced Topics (Week 9-12)
**Objective**: Develop expertise in specific areas

**Topics**:
- **Performance Optimization**
  - Profiling and benchmarking
  - Caching strategies
  - Database optimization

- **Observability**
  - Logging best practices
  - Metrics and monitoring
  - Distributed tracing

- **DevOps**
  - CI/CD pipelines
  - Infrastructure as code
  - Deployment strategies

### 4. Continuous Learning (Ongoing)
**Objective**: Stay current and share knowledge

**Activities**:
- Tech talks (bi-weekly)
- Code review sessions
- Architecture review board
- Conference attendance
- Open source contributions

## Knowledge Transfer Mechanisms

### Documentation
- **Architecture Decision Records (ADRs)**: Document key decisions
- **Runbooks**: Operational procedures
- **API Documentation**: Keep docs up to date
- **Code Comments**: Explain complex logic

### Code Reviews
- **Review Checklist**: Standardize review process
- **Learning Opportunities**: Use reviews for teaching
- **Feedback Culture**: Constructive, educational feedback
- **Review Rotation**: Expose team to different areas

### Pair Programming
- **Regular Sessions**: Schedule weekly pairing
- **Cross-Functional**: Pair across specialties
- **Knowledge Sharing**: Rotate pairs regularly
- **Complex Tasks**: Pair on difficult problems

### Tech Talks
- **Internal Presentations**: Share learnings
- **External Speakers**: Bring in experts
- **Lightning Talks**: Quick knowledge shares
- **Demo Days**: Show new features/tools

## Skill Development Paths

### Junior → Mid-Level
**Timeline**: 12-18 months

**Skills to Develop**:
- Independent feature development
- Code review participation
- Testing proficiency
- Basic architecture understanding

**Milestones**:
- Lead small feature development
- Mentor new hires
- Contribute to architecture discussions
- Improve code quality metrics

### Mid-Level → Senior
**Timeline**: 18-24 months

**Skills to Develop**:
- System design
- Technical leadership
- Cross-team collaboration
- Performance optimization

**Milestones**:
- Design and implement major features
- Lead technical initiatives
- Mentor junior developers
- Contribute to technical strategy

### Senior → Staff/Principal
**Timeline**: 24+ months

**Skills to Develop**:
- Strategic thinking
- Organizational impact
- Technical vision
- Mentorship at scale

**Milestones**:
- Define technical direction
- Influence multiple teams
- Establish best practices
- Build technical culture

## Recommended Training Resources

### Online Courses
- **Security**: OWASP courses, Secure Coding on Coursera
- **Architecture**: System Design on Educative.io
- **Testing**: Test Automation University
- **Python**: Real Python, Python Morsels

### Books
- **Clean Code** by Robert Martin
- **Design Patterns** by Gang of Four
- **The Pragmatic Programmer** by Hunt & Thomas
- **Site Reliability Engineering** by Google

### Certifications
- **Security**: CISSP, CEH, Security+
- **Cloud**: AWS/GCP/Azure certifications
- **Architecture**: TOGAF, SAFe Architect

### Communities
- **Local Meetups**: Python user groups, DevOps meetups
- **Online**: Stack Overflow, Reddit communities
- **Conferences**: PyCon, DevOps Days, Security conferences

## Measuring Success

### Individual Metrics
- **Code Quality**: Reduced defects, better test coverage
- **Velocity**: Faster feature delivery
- **Knowledge**: Successful knowledge checks
- **Contributions**: Quality and quantity of contributions

### Team Metrics
- **Onboarding Time**: Time to first meaningful contribution
- **Knowledge Distribution**: Bus factor improvement
- **Code Review Quality**: Better feedback, fewer issues
- **Technical Debt**: Reduction in debt over time

### Organizational Metrics
- **Retention**: Developer satisfaction and retention
- **Innovation**: New ideas and improvements
- **Quality**: Production incidents, bug rates
- **Delivery**: Feature velocity, time to market

## Action Items

### 🔴 CRITICAL: Create Comprehensive Onboarding Program
**Action**: Build structured onboarding for new team members
**Priority**: CRITICAL - Reduces time to productivity
**Effort**: 8-12 hours

**Step 1**: Create onboarding checklist
```markdown
# File: docs/onboarding/checklist.md

# New Developer Onboarding Checklist

## Week 1: Setup & Orientation
- [ ] Development environment setup (< 4 hours)
- [ ] Access to all systems (GitHub, Slack, CI/CD, etc.)
- [ ] Read architecture documentation
- [ ] Meet the team (1-on-1s with each member)
- [ ] Attend team standup and planning
- [ ] Shadow senior developer for 1 day

## Week 2: First Contribution
- [ ] Fix documentation issue or typo
- [ ] Submit first pull request
- [ ] Participate in code review
- [ ] Attend tech talk or demo
- [ ] Complete security training

## Week 3-4: Feature Development
- [ ] Pick up first feature ticket (small scope)
- [ ] Pair program with mentor
- [ ] Write tests for feature
- [ ] Deploy to staging
- [ ] Present work to team

## Success Criteria
- Environment setup in < 1 day
- First PR merged within 2 weeks
- First feature deployed within 1 month
```

**Step 2**: Create setup automation
```bash
# File: scripts/setup_dev_environment.sh
#!/bin/bash

echo "🚀 Setting up development environment..."

# Install dependencies
echo "Installing Python dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

# Create local config
echo "Creating local configuration..."
cp .env.example .env
echo "⚠️  Please update .env with your local settings"

# Run tests to verify setup
echo "Running tests to verify setup..."
pytest tests/ -v

# Set up database (if applicable)
echo "Setting up database..."
python manage.py migrate

echo "✅ Setup complete! You're ready to start developing."
echo "Next steps:"
echo "  1. Update .env with your settings"
echo "  2. Read docs/architecture/overview.md"
echo "  3. Pick up your first ticket from the backlog"
```

**Step 3**: Document architecture
```markdown
# File: docs/architecture/overview.md

# Architecture Overview

## System Components

### Phase 0: Documentation Analysis
- **Purpose**: Extract and validate claims from README
- **Key Files**: `src/codebase_reviewer/analyzer.py`
- **Dependencies**: None

### Phase 1: Code Structure Analysis
- **Purpose**: Analyze dependencies, architecture patterns
- **Key Files**: `src/codebase_reviewer/structure_analyzer.py`
- **Dependencies**: Phase 0

### Phase 2: Code Quality Assessment
- **Purpose**: Identify technical debt, security issues
- **Key Files**: `src/codebase_reviewer/quality_analyzer.py`
- **Dependencies**: Phase 1

## Data Flow
```mermaid
graph LR
    A[README] --> B[Phase 0: Doc Analysis]
    C[Codebase] --> D[Phase 1: Structure]
    D --> E[Phase 2: Quality]
    B --> F[Validation]
    E --> F
    F --> G[Report]
```

## Key Patterns
- **Strategy Pattern**: Different analyzers for different languages
- **Factory Pattern**: Creating analyzers based on file type
- **Observer Pattern**: Progress reporting during analysis
```

**Success Criteria**:
- [ ] Onboarding checklist created
- [ ] Setup script works on fresh machine
- [ ] Architecture docs complete
- [ ] New hire completes onboarding in < 2 weeks

### 🔴 CRITICAL: Establish Mentorship Pairing Program
**Action**: Pair each junior/mid developer with a senior mentor
**Priority**: CRITICAL - Accelerates learning
**Effort**: 4-6 hours setup + ongoing

**Step 1**: Create mentorship pairs
```python
# File: scripts/create_mentorship_pairs.py
mentorship_pairs = [
    {{
        "mentee": "Alice (Junior)",
        "mentor": "Bob (Senior)",
        "focus_areas": ["Python best practices", "Testing", "Code review"],
        "meeting_frequency": "Weekly 1-hour sessions",
        "duration": "6 months"
    }},
    {{
        "mentee": "Charlie (Mid-level)",
        "mentor": "Diana (Staff)",
        "focus_areas": ["System design", "Architecture", "Technical leadership"],
        "meeting_frequency": "Bi-weekly 1-hour sessions",
        "duration": "6 months"
    }}
]

# Generate calendar invites
for pair in mentorship_pairs:
    print(f"📅 Schedule: {{pair['mentee']}} ↔ {{pair['mentor']}}")
    print(f"   Focus: {{', '.join(pair['focus_areas'])}}")
    print(f"   Frequency: {{pair['meeting_frequency']}}")
    print()
```

**Step 2**: Create mentorship guide
```markdown
# File: docs/mentorship/guide.md

# Mentorship Guide

## For Mentors

### Responsibilities
- Meet regularly with mentee (weekly or bi-weekly)
- Review mentee's code and provide feedback
- Share knowledge and best practices
- Help mentee set and achieve goals
- Advocate for mentee's growth

### Session Structure
1. **Check-in** (5 min): How's it going? Any blockers?
2. **Code Review** (20 min): Review recent work together
3. **Learning Topic** (25 min): Teach a concept or pattern
4. **Goal Setting** (10 min): Set goals for next session

### Topics to Cover
- Week 1-4: Code quality and testing
- Week 5-8: Architecture and design patterns
- Week 9-12: Performance and optimization
- Week 13-16: Security and best practices
- Week 17-20: System design and scalability
- Week 21-24: Technical leadership

## For Mentees

### How to Get the Most Value
- Come prepared with questions
- Share code you're working on
- Be open to feedback
- Practice what you learn
- Ask for clarification
- Set specific goals

### Questions to Ask
- "How would you approach this problem?"
- "What patterns apply here?"
- "How can I improve this code?"
- "What should I learn next?"
```

**Step 3**: Track progress
```python
# File: scripts/track_mentorship_progress.py
import json
from datetime import datetime

def log_session(mentee, mentor, topics, action_items):
    'Log mentorship session.'
    session = {{
        'date': datetime.now().isoformat(),
        'mentee': mentee,
        'mentor': mentor,
        'topics_covered': topics,
        'action_items': action_items,
    }}

    with open(f'mentorship/sessions/{{mentee.replace(" ", "_")}}.jsonl', 'a') as f:
        f.write(json.dumps(session) + '\\n')

# Usage
log_session(
    mentee="Alice",
    mentor="Bob",
    topics=["Testing patterns", "Mocking", "Fixtures"],
    action_items=[
        "Write tests for UserService",
        "Read pytest documentation",
        "Practice TDD on next feature"
    ]
)
```

**Success Criteria**:
- [ ] All junior/mid developers paired with mentors
- [ ] Weekly/bi-weekly sessions scheduled
- [ ] Progress tracked and reviewed monthly
- [ ] 90%+ mentee satisfaction

### 🟠 HIGH: Launch Tech Talk Series
**Action**: Start regular knowledge-sharing presentations
**Priority**: HIGH - Builds team knowledge
**Effort**: 3-4 hours setup + ongoing

**Step 1**: Create tech talk schedule
```markdown
# File: docs/tech-talks/schedule.md

# Tech Talk Schedule

## Format
- **Frequency**: Bi-weekly (every other Friday, 2-3 PM)
- **Duration**: 30-45 minutes + 15 min Q&A
- **Location**: Conference room + Zoom for remote
- **Recording**: All talks recorded and shared

## Upcoming Talks

### Q1 2025
- **Jan 10**: "Introduction to Structured Logging" - Bob
- **Jan 24**: "Testing Strategies: Unit vs Integration" - Alice
- **Feb 7**: "Async Python: When and How" - Charlie
- **Feb 21**: "Security Best Practices" - Diana
- **Mar 7**: "Performance Profiling Tools" - Eve
- **Mar 21**: "CI/CD Pipeline Deep Dive" - Frank

### Topic Ideas
- Design patterns in our codebase
- Debugging techniques
- Database optimization
- API design principles
- Monitoring and observability
- Code review best practices
```

**Step 2**: Create presentation template
```markdown
# File: docs/tech-talks/template.md

# Tech Talk: [Title]

**Presenter**: [Name]
**Date**: [Date]
**Duration**: 30-45 minutes

## Abstract
Brief description of what this talk covers (2-3 sentences).

## Learning Objectives
By the end of this talk, attendees will be able to:
1. Objective 1
2. Objective 2
3. Objective 3

## Outline
1. Introduction (5 min)
2. Core Concept (15 min)
3. Live Demo (15 min)
4. Best Practices (10 min)
5. Q&A (15 min)

## Resources
- Link to slides
- Link to demo code
- Further reading

## Follow-up
- Practice exercises
- Related talks
- Office hours for questions
```

**Step 3**: Promote and track attendance
```bash
# Send calendar invite
# Post in Slack #engineering channel
# Record and share on internal wiki

# Track attendance and feedback
cat > scripts/track_tech_talk.sh << 'BASH'
#!/bin/bash
echo "Tech Talk Feedback Form"
echo "======================"
echo "Talk: $1"
echo "Date: $(date)"
echo ""
echo "Attendees: $2"
echo "Rating (1-5): $3"
echo "Key Takeaways: $4"
echo "Suggestions: $5"
BASH
```

**Success Criteria**:
- [ ] Bi-weekly talks scheduled for 6 months
- [ ] 80%+ team attendance
- [ ] All talks recorded and shared
- [ ] 4.0+ average rating

### 🟠 HIGH: Build Knowledge Base
**Action**: Create centralized documentation repository
**Priority**: HIGH - Reduces repeated questions
**Effort**: 6-8 hours

**Step 1**: Set up documentation structure
```bash
# Create docs structure
mkdir -p docs/{{architecture,guides,runbooks,adr,onboarding,mentorship}}

# Create index
cat > docs/README.md << 'MD'
# Engineering Knowledge Base

## Quick Links
- [Architecture Overview](architecture/overview.md)
- [Onboarding Checklist](onboarding/checklist.md)
- [Code Review Guide](guides/code-review.md)
- [Deployment Runbook](runbooks/deployment.md)

## Architecture
- [System Overview](architecture/overview.md)
- [Data Flow](architecture/data-flow.md)
- [Design Patterns](architecture/patterns.md)
- [ADRs](adr/)

## Guides
- [Development Setup](guides/setup.md)
- [Testing Guide](guides/testing.md)
- [Security Guide](guides/security.md)
- [Performance Guide](guides/performance.md)

## Runbooks
- [Deployment](runbooks/deployment.md)
- [Incident Response](runbooks/incidents.md)
- [Database Migrations](runbooks/migrations.md)

## Mentorship
- [Mentorship Guide](mentorship/guide.md)
- [Learning Paths](mentorship/learning-paths.md)
- [Tech Talk Schedule](tech-talks/schedule.md)
MD
```

**Step 2**: Create essential guides
```markdown
# File: docs/guides/code-review.md

# Code Review Guide

## For Authors

### Before Submitting PR
- [ ] All tests pass locally
- [ ] Code is self-documented
- [ ] Added tests for new functionality
- [ ] Updated documentation
- [ ] Ran linters and formatters

### PR Description Template
\`\`\`markdown
## What
Brief description of changes

## Why
Reason for changes (link to ticket)

## How
Technical approach

## Testing
How to test these changes

## Screenshots
(if UI changes)
\`\`\`

## For Reviewers

### Review Checklist
- [ ] Code is readable and maintainable
- [ ] Tests are comprehensive
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Documentation updated
- [ ] Follows team conventions

### Feedback Guidelines
- Be kind and constructive
- Explain the "why" behind suggestions
- Distinguish between "must fix" and "nice to have"
- Approve when ready, don't nitpick
```

**Success Criteria**:
- [ ] Documentation structure created
- [ ] 10+ guides written
- [ ] Team uses docs as first resource
- [ ] Docs updated with each major change

### 🟡 MEDIUM: Implement Pair Programming Rotation
**Action**: Schedule regular pairing sessions
**Priority**: MEDIUM - Spreads knowledge
**Effort**: 2-3 hours setup

**Step 1**: Create pairing schedule
```python
# File: scripts/generate_pairing_schedule.py
import random
from datetime import datetime, timedelta

team = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]

def generate_pairs(team_members, weeks=4):
    'Generate pairing schedule.'
    pairs = []
    members = team_members.copy()

    for week in range(weeks):
        random.shuffle(members)
        week_pairs = []
        for i in range(0, len(members), 2):
            if i + 1 < len(members):
                week_pairs.append((members[i], members[i+1]))
        pairs.append(week_pairs)

    return pairs

schedule = generate_pairs(team)
for week, pairs in enumerate(schedule, 1):
    print(f"Week {{week}}:")
    for pair in pairs:
        print(f"  {{pair[0]}} ↔ {{pair[1]}}")
    print()
```

**Step 2**: Set pairing guidelines
```markdown
# File: docs/guides/pair-programming.md

# Pair Programming Guide

## When to Pair
- Complex features or refactoring
- Onboarding new team members
- Debugging difficult issues
- Learning new technologies
- Code reviews (live)

## Pairing Styles

### Driver-Navigator
- **Driver**: Types the code
- **Navigator**: Reviews, suggests, thinks ahead
- **Switch**: Every 15-30 minutes

### Ping-Pong
- Person A writes failing test
- Person B makes it pass
- Person B writes next test
- Person A makes it pass
- Repeat

## Best Practices
- Take breaks every hour
- Communicate constantly
- Be patient and respectful
- Share keyboard equally
- Ask questions
- Explain your thinking
```

**Success Criteria**:
- [ ] Pairing schedule created
- [ ] 50%+ of team pairs weekly
- [ ] Knowledge spread across team
- [ ] Positive feedback from participants

## Verification Commands

```bash
# Check onboarding docs exist
test -f docs/onboarding/checklist.md && echo "✅ Onboarding docs exist"

# Verify setup script works
bash scripts/setup_dev_environment.sh

# Check mentorship pairs
cat scripts/create_mentorship_pairs.py

# View tech talk schedule
cat docs/tech-talks/schedule.md

# Check knowledge base
ls -R docs/
```

## Priority Summary
- 🔴 **CRITICAL**: Onboarding (8-12h), Mentorship (4-6h) - **This sprint**
- 🟠 **HIGH**: Tech talks (3-4h), Knowledge base (6-8h) - **This month**
- 🟡 **MEDIUM**: Pair programming (2-3h) - **This quarter**

**Total Effort**: ~23-33 hours for critical/high priority items

## Success Stories Template

Document successful mentorship examples:
- **Mentee**: Name and level
- **Challenge**: What they struggled with
- **Approach**: How mentorship helped
- **Outcome**: Results achieved
- **Lessons**: What we learned

This creates a feedback loop for continuous improvement of the mentorship program.
"""
        return self._generate_generic_response(
            prompt_id, prompt_text, context, repository
        )

    # Helper methods for new generators

    def _format_list(self, items: List) -> str:
        """Format a list of items as markdown list."""
        if not items:
            return "- None"
        return "\n".join(f"- {item}" for item in items[:10])

    def _generate_setup_recommendations(
        self, prereqs, setup_files, build_steps, env_vars, undocumented
    ):
        """Generate setup recommendations based on findings."""
        recommendations = []
        if not prereqs:
            recommendations.append(
                "1. ❌ **CRITICAL**: Document prerequisites in README"
            )
        if not setup_files:
            recommendations.append(
                "2. ❌ **CRITICAL**: Add setup.py or requirements.txt"
            )
        if not build_steps:
            recommendations.append("3. ⚠️ **HIGH**: Document build/installation steps")
        if not env_vars:
            recommendations.append("4. ⚠️ **MEDIUM**: Document environment variables")
        if undocumented:
            recommendations.append(
                f"5. ⚠️ **MEDIUM**: Document {len(undocumented)} undocumented features"
            )

        if not recommendations:
            return "✅ All setup documentation is complete"
        return "\n".join(recommendations)

    def _calculate_setup_score(self, prereqs, setup_files, build_steps):
        """Calculate setup documentation score."""
        score = 0
        if prereqs:
            score += 40
        if setup_files:
            score += 40
        if build_steps:
            score += 20
        return score

    def _format_top_issues(self, issues: List) -> str:
        """Format top issues list."""
        if not issues:
            return "- No issues found"

        formatted = []
        for i, issue in enumerate(issues[:10], 1):
            if isinstance(issue, dict):
                severity = issue.get("severity", "UNKNOWN")
                description = issue.get("description", "No description")
                file_path = issue.get("file", "Unknown file")
                formatted.append(f"{i}. **[{severity}]** {description} ({file_path})")
            else:
                formatted.append(f"{i}. {issue}")

        return "\n".join(formatted)

    def _generate_priority_matrix(self, issues: List) -> str:
        """Generate priority matrix for top issues."""
        if not issues:
            return "| No issues | - | - | - | - |"

        rows = []
        for issue in issues[:5]:
            if isinstance(issue, dict):
                name = issue.get("description", "Unknown")[:40]
                severity = issue.get("severity", "MEDIUM")
                impact = "High" if severity in ["HIGH", "CRITICAL"] else "Medium"
                effort = (
                    "Low" if "TODO" in name or "comment" in name.lower() else "Medium"
                )
                priority = (
                    "P0"
                    if severity == "CRITICAL"
                    else "P1"
                    if severity == "HIGH"
                    else "P2"
                )
                timeline = (
                    "This sprint"
                    if priority == "P0"
                    else "Next sprint"
                    if priority == "P1"
                    else "Backlog"
                )
                rows.append(
                    f"| {name} | {impact} | {effort} | {priority} | {timeline} |"
                )

        return "\n".join(rows) if rows else "| No issues | - | - | - | - |"

    def _identify_quick_wins(self, issues: List) -> str:
        """Identify quick win improvements."""
        if not issues:
            return "- No quick wins identified"

        quick_wins = []
        for issue in issues:
            if isinstance(issue, dict):
                desc = issue.get("description", "")
                severity = issue.get("severity", "")
                # Quick wins: TODO comments, simple fixes, low-hanging fruit
                if any(
                    keyword in desc.lower()
                    for keyword in ["todo", "fixme", "comment", "print"]
                ):
                    quick_wins.append(f"- {desc} (Estimated: 1-2 hours)")

        if not quick_wins:
            return "- Review codebase for TODO/FIXME comments\n- Replace print() with logging\n- Add missing docstrings"

        return "\n".join(quick_wins[:5])

    def _identify_major_refactoring(self, issues: List) -> str:
        """Identify major refactoring projects."""
        if not issues:
            return "- No major refactoring needed"

        major_projects = []
        for issue in issues:
            if isinstance(issue, dict):
                desc = issue.get("description", "")
                severity = issue.get("severity", "")
                # Major refactoring: security issues, architecture problems
                if severity in ["HIGH", "CRITICAL"] and not any(
                    keyword in desc.lower() for keyword in ["todo", "comment"]
                ):
                    major_projects.append(f"- {desc} (Estimated: 1-2 weeks)")

        if not major_projects:
            return "- Improve test coverage to 80%+\n- Reduce cyclomatic complexity\n- Break up large modules"

        return "\n".join(major_projects[:5])
