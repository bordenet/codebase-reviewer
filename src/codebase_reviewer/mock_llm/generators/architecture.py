"""Architecture analysis response generators."""

from typing import Any, List

from .base import BaseGenerator


class ArchitectureGenerator(BaseGenerator):
    """Generates architecture analysis responses."""

    def validate(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate architecture validation response."""
        if not isinstance(context, dict):
            return self._generate_fallback(repository)

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

    def _validate_components(self, claimed: List, actual: List) -> str:
        """Validate claimed components against actual structure."""
        if not claimed and not actual:
            return "- No components to validate"

        result = []
        if claimed:
            result.append("**Claimed Components**:")
            for comp in claimed[:5]:
                result.append(f"- {comp}")

        if actual:
            result.append("\n**Actual Packages**:")
            for pkg in actual[:5]:
                result.append(f"- {pkg}")

        return "\n".join(result)

    def _format_languages(self, languages: List) -> str:
        """Format detected languages.

        Args:
            languages: List of language strings or dicts with 'name' key

        Returns:
            Comma-separated list of language names
        """
        if not languages:
            return "None detected"
        # Handle both string and dict formats
        names = []
        for lang in languages:
            if isinstance(lang, dict):
                names.append(lang.get("name", str(lang)))
            elif hasattr(lang, "name"):
                names.append(lang.name)
            else:
                names.append(str(lang))
        return ", ".join(names)

    def _format_packages(self, packages: List) -> str:
        """Format package list."""
        if not packages:
            return "- No packages found"
        return "\n".join(f"- `{pkg}`" for pkg in packages[:10])

    def _format_validation_results(self, results: Any) -> str:
        """Format validation results.

        Args:
            results: List of results or dict with validation data

        Returns:
            Formatted validation results string
        """
        if not results:
            return "- No validation issues found"
        # Handle dict format with drift info
        if isinstance(results, dict):
            formatted = []
            if results.get("drift_severity"):
                formatted.append(f"- Drift severity: {results['drift_severity']}")
            if results.get("architecture_drift"):
                for drift in results["architecture_drift"][:5]:
                    formatted.append(f"- {drift}")
            if results.get("missing_components"):
                for comp in results["missing_components"][:5]:
                    formatted.append(f"- Missing: {comp}")
            return "\n".join(formatted) if formatted else "- No validation issues found"
        # Handle list format
        if isinstance(results, list):
            return "\n".join(f"- {result}" for result in results[:10])
        return f"- {results}"

    def _generate_fallback(self, repository: str) -> str:
        """Generate fallback response when context is invalid."""
        return f"""# Architecture Validation

## Summary
Analyzed repository at `{repository}`.

## Findings
Unable to extract detailed architecture information due to missing context data.

## Recommendations
1. Provide complete context data for analysis
2. Re-run analysis with proper context
"""

    def analyze_dependencies(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate dependency analysis response."""
        return f"""# Dependency Analysis

## Summary
Analyzed dependencies for `{repository}`.

## Findings
- Direct dependencies identified
- Transitive dependencies mapped
- Version conflicts checked

## Recommendations
1. Update outdated dependencies
2. Remove unused dependencies
3. Pin critical dependency versions
"""

    def call_graph(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate call graph analysis response."""
        return f"""# Call Graph Analysis

## Summary
Generated call graph for `{repository}`.

## Findings
- Function call relationships mapped
- Critical paths identified
- Circular dependencies detected

## Recommendations
1. Break circular dependencies
2. Simplify complex call chains
3. Document critical paths
"""

    def git_hotspots(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate git hotspots analysis response."""
        return f"""# Git Hotspots Analysis

## Summary
Analyzed change frequency for `{repository}`.

## Findings
- High-churn files identified
- Change patterns analyzed
- Risk areas highlighted

## Recommendations
1. Refactor high-churn files
2. Add tests to risky areas
3. Review change patterns
"""

    def cohesion_coupling(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate cohesion and coupling analysis response."""
        return f"""# Cohesion & Coupling Analysis

## Summary
Analyzed module cohesion and coupling for `{repository}`.

## Findings
- Low cohesion modules identified
- High coupling detected
- Modularity score calculated

## Recommendations
1. Increase module cohesion
2. Reduce inter-module coupling
3. Refactor tightly coupled components
"""
