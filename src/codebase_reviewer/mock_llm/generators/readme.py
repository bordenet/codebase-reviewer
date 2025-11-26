"""README analysis response generator."""

from typing import Any

from .base import BaseGenerator


class ReadmeGenerator(BaseGenerator):
    """Generates README analysis responses."""

    def analyze(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate README analysis response."""
        if not isinstance(context, dict):
            return self._generate_fallback(repository)

        readme_content = context.get("readme_content", "")
        total_docs = context.get("total_docs_found", 0)

        # Extract key claims
        claims = self._extract_readme_claims(readme_content)

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

    def _extract_readme_claims(self, content: str) -> list:
        """Extract testable claims from README content."""
        claims = []
        if "Python" in content:
            claims.append("Python-based tool")
        if "workflow" in content.lower():
            claims.append("Customizable workflow system")
        if "Web" in content or "web" in content:
            claims.append("Web UI available")
        if "CLI" in content or "command" in content.lower():
            claims.append("Command-line interface")
        return claims

    def _generate_fallback(self, repository: str) -> str:
        """Generate fallback response when context is invalid."""
        return f"""# README Analysis

## Summary
Analyzed repository at `{repository}`.

## Findings
Unable to extract detailed claims due to missing context data.

## Recommendations
1. Ensure README.md exists in repository root
2. Provide complete context data for analysis
3. Re-run analysis with proper context
"""
