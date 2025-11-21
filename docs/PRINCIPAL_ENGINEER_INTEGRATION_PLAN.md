# Principal Engineer Review Integration Plan

**Date**: 2025-11-21  
**Status**: PROPOSED  
**Goal**: Integrate Perplexity.ai's Principal Engineer review methodology into our existing architecture

---

## Executive Summary

This plan integrates the **6-phase Principal Engineer review workflow** from Perplexity.ai into our existing **documentation-first 5-phase architecture** by:

1. **Mapping Perplexity phases to our existing structure** (where overlap exists)
2. **Creating new workflow templates** for Principal Engineer reviews
3. **Extending our YAML configuration system** to support multiple review types
4. **Maintaining backward compatibility** with existing 5-phase workflow
5. **Leveraging existing analyzers** (no code duplication)

---

## Phase Mapping Analysis

### Current Architecture (5 Phases)
- **Phase 0**: Documentation Review (README, architecture docs, setup guides)
- **Phase 1**: Architecture Analysis (structure, patterns, dependencies)
- **Phase 2**: Implementation Deep-Dive (code quality, patterns, anti-patterns)
- **Phase 3**: Development Workflow (testing, CI/CD, build process)
- **Phase 4**: Interactive Remediation (prioritized action planning)

### Perplexity Principal Engineer Workflow (6 Phases)
1. **High-Level Reconnaissance** (3 steps)
2. **Baseline Hygiene Checks** (4 steps)
3. **Core Safety and Security** (3 steps)
4. **Architecture Insights** (4 steps)
5. **Coverage & Modeling** (4 steps)
6. **Principal Engineer Strategy** (6 steps)

### Mapping Strategy

| Perplexity Phase | Maps to Current Phase | Notes |
|------------------|----------------------|-------|
| High-Level Reconnaissance | Phase 0 + Phase 1 | Docs + architecture mapping |
| Baseline Hygiene Checks | Phase 3 + Phase 2 | Testing + build + code quality |
| Core Safety and Security | Phase 2 (extended) | NEW: Security-focused analysis |
| Architecture Insights | Phase 1 (extended) | NEW: Call graphs, hotspots, duplication |
| Coverage & Modeling | Phase 2 + Phase 3 | Integration audit + boundary analysis |
| Principal Engineer Strategy | Phase 4 (extended) | NEW: Design drift, instrumentation, mentoring |

---

## Proposed Architecture Changes

### 1. Workflow Configuration System

**New Directory Structure:**
```
src/codebase_reviewer/
├── prompts/
│   ├── templates/
│   │   ├── phase0.yml          # Existing
│   │   ├── phase1.yml          # Existing
│   │   ├── phase2.yml          # Existing
│   │   ├── phase3.yml          # Existing
│   │   └── phase4.yml          # Existing
│   └── workflows/               # NEW
│       ├── default.yml          # Maps to existing 5-phase
│       ├── principal_engineer.yml  # NEW: Perplexity workflow
│       ├── security_audit.yml   # NEW: Security-focused
│       └── onboarding.yml       # NEW: New developer focus
```

### 2. Workflow Schema

**File: `src/codebase_reviewer/prompts/workflows/principal_engineer.yml`**

```yaml
workflow:
  name: "Principal Engineer Strategic Review"
  version: "1.0"
  description: "Comprehensive codebase assessment using Perplexity.ai methodology"
  
  # Map to existing phases where possible
  phases:
    - id: "reconnaissance"
      title: "High-Level Reconnaissance"
      steps:
        - prompt_template: "phase0.yml#0.1"  # Reuse existing README analysis
          title: "Scan architecture docs & README"
          
        - prompt_template: "phase1.yml#1.1"  # Reuse existing dependency mapping
          title: "Map critical modules & dependencies"
          
        - prompt_template: "NEW"  # Requires new template
          title: "Run static analysis/lint tools"
          custom_prompt: |
            Generate a summary report identifying major code quality issues,
            anti-patterns, and code smells from static analysis results.
```

### 3. New Components Required

#### A. WorkflowLoader (NEW)
- **Location**: `src/codebase_reviewer/prompts/workflow_loader.py`
- **Purpose**: Load and validate workflow YAML files
- **Responsibilities**:
  - Parse workflow definitions
  - Resolve prompt template references
  - Validate step dependencies
  - Merge custom prompts with templates

#### B. WorkflowExecutor (NEW)
- **Location**: `src/codebase_reviewer/workflow_executor.py`
- **Purpose**: Execute workflows step-by-step
- **Responsibilities**:
  - Orchestrate step execution
  - Track progress
  - Handle step dependencies
  - Generate workflow-specific reports

#### C. Extended PhaseGenerator (MODIFY)
- **Location**: `src/codebase_reviewer/prompts/generator.py`
- **Changes**: Add support for custom prompts (not just templates)
- **New Method**: `generate_custom(prompt_text, context)`

---

## Implementation Plan

### Phase 1: Foundation (Week 1)
- [ ] Create workflow schema definition
- [ ] Implement `WorkflowLoader` class
- [ ] Add workflow validation logic
- [ ] Write tests for workflow loading

### Phase 2: Principal Engineer Workflow (Week 2)
- [ ] Create `principal_engineer.yml` workflow
- [ ] Map existing prompts to Perplexity steps
- [ ] Identify gaps requiring new prompts
- [ ] Create new prompt templates for gaps

### Phase 3: Execution Engine (Week 3)
- [ ] Implement `WorkflowExecutor` class
- [ ] Add step dependency resolution
- [ ] Implement progress tracking
- [ ] Add workflow state management

### Phase 4: Integration (Week 4)
- [ ] Update CLI to support workflow selection
- [ ] Update web UI to display workflow progress
- [ ] Add workflow export functionality
- [ ] Update documentation

---

## Backward Compatibility Strategy

**Critical**: Existing 5-phase workflow MUST continue to work unchanged.

**Solution**: Create `default.yml` workflow that maps 1:1 to existing phases:

```yaml
workflow:
  name: "Default Documentation-First Review"
  version: "1.0"
  phases:
    - id: "phase0"
      prompts: ["phase0.yml"]  # Use entire template
    - id: "phase1"
      prompts: ["phase1.yml"]
    # ... etc
```

**CLI Compatibility**:
```bash
# Existing behavior (unchanged)
codebase-reviewer analyze /path/to/repo

# New workflow selection
codebase-reviewer analyze /path/to/repo --workflow principal_engineer
codebase-reviewer analyze /path/to/repo --workflow security_audit
```

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Prioritize gaps** in current prompts vs Perplexity methodology
3. **Create detailed prompt templates** for missing steps
4. **Implement WorkflowLoader** as first deliverable
5. **Iterate on principal_engineer.yml** workflow definition

---

## Questions to Resolve

1. Should workflows be user-customizable (edit YAML) or fixed?
2. Do we need a workflow marketplace/sharing mechanism?
3. Should we support workflow composition (inherit from base workflows)?
4. How do we handle workflow versioning and migration?

