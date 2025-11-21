# Implementation Recommendation: Principal Engineer Review Integration

**Date**: 2025-11-21  
**Recommendation**: **Option B - Workflow System** (with pragmatic phasing)  
**Rationale**: Best long-term architecture, aligns with existing YAML-driven design

---

## Why Option B (Workflow System)?

### Alignment with Current Architecture
Our recent refactoring **already moved in this direction**:
- ✅ Prompts decoupled to YAML (`phase0.yml` - `phase4.yml`)
- ✅ Unified `PhaseGenerator` with registry pattern
- ✅ Template-driven approach (not hardcoded)
- ✅ Configuration-first philosophy (per `CLAUDE.md`)

**The workflow system is the natural next step.**

### Extensibility Benefits
- Support multiple review types (Principal Engineer, Security Audit, Onboarding)
- Enable user-customizable workflows
- Allow workflow sharing/marketplace
- Support workflow composition and inheritance

### Code Quality
- Maintains A+ standards (no file over 400 lines)
- Clean separation of concerns
- Follows existing patterns (YAML config + Python logic)
- Testable and maintainable

---

## Phased Implementation (Pragmatic Approach)

### Phase 1: Foundation (Week 1) - MINIMAL VIABLE WORKFLOW
**Goal**: Get Principal Engineer workflow working with existing prompts

**Deliverables**:
1. Simple workflow schema (YAML)
2. Basic `WorkflowLoader` class
3. `principal_engineer.yml` workflow (using existing prompts)
4. CLI flag: `--workflow principal_engineer`

**Code Changes**:
- New file: `src/codebase_reviewer/prompts/workflow_loader.py` (~150 lines)
- New file: `src/codebase_reviewer/prompts/workflows/principal_engineer.yml` (~200 lines)
- Modify: `src/codebase_reviewer/cli.py` (add `--workflow` option)
- Modify: `src/codebase_reviewer/prompt_generator.py` (add workflow support)

**Complexity**: LOW  
**Risk**: LOW (backward compatible)

---

### Phase 2: Gap Filling (Week 2) - NEW PROMPTS
**Goal**: Add missing prompts identified in PERPLEXITY_MAPPING.md

**Deliverables**:
1. New prompt templates for 7 missing steps
2. Enhanced prompts for 9 partial matches
3. Updated `principal_engineer.yml` to use new prompts

**New Files**:
- `src/codebase_reviewer/prompts/templates/security.yml` (security-focused prompts)
- `src/codebase_reviewer/prompts/templates/architecture_insights.yml` (call graphs, hotspots)
- `src/codebase_reviewer/prompts/templates/strategy.yml` (instrumentation, mentoring)

**Complexity**: MEDIUM  
**Risk**: LOW (additive only)

---

### Phase 3: Advanced Features (Week 3-4) - WORKFLOW ENGINE
**Goal**: Full workflow orchestration with dependencies and state

**Deliverables**:
1. `WorkflowExecutor` class with dependency resolution
2. Progress tracking and state management
3. Web UI workflow visualization
4. Workflow export (Markdown/JSON)

**Code Changes**:
- New file: `src/codebase_reviewer/workflow_executor.py` (~300 lines)
- New file: `src/codebase_reviewer/workflow_state.py` (~150 lines)
- Modify: `src/codebase_reviewer/web.py` (add workflow UI)

**Complexity**: HIGH  
**Risk**: MEDIUM (new abstraction)

---

## Detailed Design: Phase 1 (Minimal Viable Workflow)

### 1. Workflow Schema (Simple Version)

**File**: `src/codebase_reviewer/prompts/workflows/principal_engineer.yml`

```yaml
workflow:
  name: "Principal Engineer Strategic Review"
  version: "1.0"
  description: "Perplexity.ai methodology for principal engineers"
  
  # Simple linear execution (no dependencies yet)
  sections:
    - id: "reconnaissance"
      title: "High-Level Reconnaissance"
      prompts:
        - template: "phase0.yml#0.1"  # Scan docs & README
        - template: "phase1.yml#1.1"  # Map dependencies
        - template: "phase2.yml#2.1"  # Static analysis
    
    - id: "hygiene"
      title: "Baseline Hygiene Checks"
      prompts:
        - template: "phase3.yml#3.1"  # Test coverage
        - template: "phase3.yml#3.2"  # CI/CD review
        - template: "phase1.yml#1.2"  # Entry points
        - custom:
            id: "comment_check"
            title: "Check code comments"
            prompt: |
              Detect comments that are outdated, missing, or inconsistent 
              with the code logic, and recommend areas needing documentation 
              improvements.
    
    # ... more sections
```

### 2. WorkflowLoader Class

**File**: `src/codebase_reviewer/prompts/workflow_loader.py`

```python
"""Workflow configuration loader and validator."""

from pathlib import Path
from typing import Dict, List, Optional
import yaml
from pydantic import BaseModel, Field


class WorkflowPrompt(BaseModel):
    """A single prompt in a workflow."""
    template: Optional[str] = None  # e.g., "phase0.yml#0.1"
    custom: Optional[Dict] = None   # Custom prompt definition


class WorkflowSection(BaseModel):
    """A section (accordion) in a workflow."""
    id: str
    title: str
    prompts: List[WorkflowPrompt]


class WorkflowDefinition(BaseModel):
    """Complete workflow definition."""
    name: str
    version: str
    description: str
    sections: List[WorkflowSection]


class WorkflowLoader:
    """Loads and validates workflow YAML files."""
    
    def __init__(self, workflows_dir: Optional[Path] = None):
        """Initialize with workflows directory."""
        if workflows_dir is None:
            workflows_dir = Path(__file__).parent / "workflows"
        self.workflows_dir = workflows_dir
        self._cache: Dict[str, WorkflowDefinition] = {}
    
    def load(self, workflow_name: str) -> WorkflowDefinition:
        """Load a workflow by name."""
        if workflow_name in self._cache:
            return self._cache[workflow_name]
        
        workflow_path = self.workflows_dir / f"{workflow_name}.yml"
        if not workflow_path.exists():
            raise FileNotFoundError(f"Workflow not found: {workflow_name}")
        
        with open(workflow_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        workflow = WorkflowDefinition(**data['workflow'])
        self._cache[workflow_name] = workflow
        return workflow
    
    def list_workflows(self) -> List[str]:
        """List all available workflows."""
        return [
            p.stem for p in self.workflows_dir.glob("*.yml")
        ]
```

### 3. CLI Integration

**File**: `src/codebase_reviewer/cli.py` (modifications)

```python
@click.option(
    "--workflow",
    "-w",
    default="default",
    type=str,
    help="Workflow to use (default, principal_engineer, security_audit)",
)
def analyze(repository_path, output, workflow):
    """Analyze a repository."""
    # ... existing code ...
    
    # NEW: Load workflow if specified
    if workflow != "default":
        from codebase_reviewer.prompts.workflow_loader import WorkflowLoader
        loader = WorkflowLoader()
        workflow_def = loader.load(workflow)
        # Use workflow-based generation
        prompts = generate_from_workflow(workflow_def, repo_analysis)
    else:
        # Existing 5-phase generation
        prompts = prompt_generator.generate_all_phases(repo_analysis)
```

---

## File Size Compliance

All new files will comply with 400-line limit:

| File | Estimated Lines | Status |
|------|----------------|--------|
| `workflow_loader.py` | ~150 | ✅ Under limit |
| `principal_engineer.yml` | ~250 | ✅ Under limit |
| `workflow_executor.py` | ~300 | ✅ Under limit |
| `workflow_state.py` | ~150 | ✅ Under limit |
| `security.yml` | ~100 | ✅ Under limit |
| `architecture_insights.yml` | ~120 | ✅ Under limit |
| `strategy.yml` | ~150 | ✅ Under limit |

**Total new code**: ~1,220 lines across 7 files  
**Average file size**: 174 lines ✅

---

## Testing Strategy

### Unit Tests
- `test_workflow_loader.py` - YAML parsing and validation
- `test_workflow_executor.py` - Step execution and dependencies
- `test_workflow_integration.py` - End-to-end workflow execution

### Integration Tests
- Test Principal Engineer workflow on sample repos
- Verify backward compatibility with default workflow
- Test workflow switching via CLI

### Quality Gates
- All pre-commit hooks must pass
- Test coverage > 80%
- Pylint score > 9.0
- MyPy type checking passes

---

## Next Steps

1. **Get approval** on this approach
2. **Create Phase 1 branch**: `feature/workflow-system-phase1`
3. **Implement WorkflowLoader** and basic schema
4. **Create principal_engineer.yml** using existing prompts
5. **Add CLI integration** with `--workflow` flag
6. **Test and iterate** on sample repositories
7. **Merge to main** when Phase 1 complete
8. **Proceed to Phase 2** (gap filling)

---

## Questions for Discussion

1. Should we support workflow inheritance? (e.g., `extends: default.yml`)
2. Do we need workflow versioning/migration?
3. Should workflows be user-editable or read-only?
4. Do we want a workflow marketplace/sharing mechanism?
5. Should we support parallel step execution in Phase 3?

