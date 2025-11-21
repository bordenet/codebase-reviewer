# Workflow Integration Proposal: Configuration-Driven Review Steps

**Version**: 1.0  
**Date**: 2025-11-21  
**Status**: PROPOSAL  

## Executive Summary

This proposal integrates the **accordion-style procedural workflow** (from Perplexity research) with our existing **documentation-first phase-based approach** by:

1. **Decoupling workflow steps from code** → YAML/JSON configuration files
2. **Maintaining our core strength** → Documentation-first validation
3. **Adding flexibility** → Customizable review workflows for different contexts
4. **Enabling extensibility** → Plugin-based step execution

---

## Current Approach Analysis

### Strengths ✅
- **Documentation-first validation**: Unique differentiator - validates docs against code
- **Structured phases**: Clear progression (Phase 0-4)
- **Type-safe models**: Pydantic models ensure data integrity
- **Automated prompt generation**: AI-ready outputs
- **Validation engine**: Cross-checks claims vs reality

### Limitations ⚠️
- **Hardcoded workflow**: Steps are embedded in Python code
- **Fixed phase structure**: Can't easily customize for different review types
- **Limited reusability**: Can't share workflows across teams
- **No runtime customization**: Must modify code to change workflow

---

## Alternative Approach Analysis (Accordion Model)

### Strengths ✅
- **Procedural clarity**: 6 clear stages from reconnaissance to strategy
- **Comprehensive coverage**: Includes security, architecture, and mentoring
- **Industry best practices**: Based on research from multiple sources
- **Flexible execution**: Can expand/collapse sections as needed
- **Principal engineer focus**: Strategic interventions, not just analysis

### Gaps ⚠️
- **No documentation-first approach**: Treats docs as one of many inputs
- **No validation engine**: Doesn't cross-check docs vs code
- **Manual execution**: Requires human interpretation at each step
- **No AI integration**: Doesn't generate prompts or automate analysis

---

## Proposed Integration: Hybrid Configuration-Driven Model

### Core Concept

**Combine the best of both approaches**:
- Keep our documentation-first validation engine (unique value)
- Add configuration-driven workflow steps (flexibility)
- Enable custom review types (principal engineer, onboarding, audit, security)
- Maintain type safety and automation (existing strength)

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Workflow Configuration Layer                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  YAML/JSON Workflow Definitions                        │ │
│  │  • default_review.yml (current 5-phase approach)       │ │
│  │  • principal_engineer_review.yml (accordion approach)  │ │
│  │  • security_audit.yml (security-focused)               │ │
│  │  • onboarding_review.yml (new developer focus)         │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  Workflow Engine (NEW)                       │
│  • Parses workflow configuration                            │
│  • Validates step dependencies                              │
│  • Orchestrates step execution                              │
│  • Manages step state (collapsed/expanded)                  │
│  • Generates progress reports                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Step Executor Registry (NEW)                    │
│  • Maps step types to executor implementations              │
│  • Built-in executors (existing analyzers)                  │
│  • Plugin executors (custom steps)                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│           Existing Analysis Engine (UNCHANGED)               │
│  • DocumentationAnalyzer                                     │
│  • CodeAnalyzer                                              │
│  • ValidationEngine                                          │
│  • PromptGenerator                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration Schema

### Workflow Definition Format

```yaml
# workflows/principal_engineer_review.yml
workflow:
  name: "Principal Engineer Strategic Review"
  version: "1.0"
  description: "Comprehensive codebase assessment for principal engineers"
  
  # Global settings
  settings:
    parallel_execution: true
    fail_fast: false
    cache_results: true
    
  # Accordion sections (collapsible groups)
  sections:
    - id: "reconnaissance"
      title: "1. High-Level Reconnaissance"
      collapsed: false  # Start expanded
      steps:
        - id: "scan_docs"
          type: "documentation_analyzer"
          title: "Scan architecture docs & README"
          executor: "builtin.documentation"
          config:
            doc_types: ["primary", "architecture", "api"]
            extract_claims: true
          outputs:
            - "documentation_analysis"
            
        - id: "map_dependencies"
          type: "dependency_mapper"
          title: "Map critical modules & dependencies"
          executor: "builtin.code_structure"
          depends_on: ["scan_docs"]
          config:
            include_graphs: true
            depth: 3
          outputs:
            - "dependency_graph"
            
        - id: "static_analysis"
          type: "quality_check"
          title: "Run static analysis/lint tools"
          executor: "builtin.quality"
          parallel_with: ["map_dependencies"]
          config:
            tools: ["pylint", "mypy", "bandit"]
          outputs:
            - "quality_report"

    - id: "baseline_hygiene"
      title: "2. Baseline Hygiene Checks"
      collapsed: true  # Start collapsed
      steps:
        - id: "test_coverage"
          type: "coverage_analyzer"
          title: "Survey test coverage and testability"
          executor: "builtin.test_coverage"
          depends_on: ["map_dependencies"]
          config:
            threshold: 60
            report_untested: true
          outputs:
            - "coverage_report"

        - id: "build_validation"
          type: "build_checker"
          title: "Review build, dependency, and CI configs"
          executor: "builtin.build_validator"
          config:
            check_ci: true
            check_reproducibility: true
          outputs:
            - "build_health"

    - id: "core_safety"
      title: "3. Core Safety and Security"
      collapsed: true
      steps:
        - id: "security_scan"
          type: "security_analyzer"
          title: "Assess security of public interfaces"
          executor: "plugin.security_scanner"
          config:
            scan_endpoints: true
            check_auth: true
            check_data_access: true
          outputs:
            - "security_report"

    - id: "architecture_insights"
      title: "4. Architecture and Dependency Insights"
      collapsed: true
      steps:
        - id: "validate_architecture"
          type: "architecture_validator"
          title: "Cross-reference code with design docs"
          executor: "builtin.validation"
          depends_on: ["scan_docs", "map_dependencies"]
          config:
            check_drift: true
            severity_threshold: "medium"
          outputs:
            - "validation_results"

        - id: "visualize_dependencies"
          type: "graph_generator"
          title: "Visualize module and dependency graphs"
          executor: "plugin.graph_viz"
          depends_on: ["map_dependencies"]
          config:
            format: "mermaid"
            include_external: false
          outputs:
            - "dependency_graph.mmd"

    - id: "principal_strategy"
      title: "6. Principal Engineer Strategy"
      collapsed: true
      steps:
        - id: "generate_prompts"
          type: "prompt_generator"
          title: "Generate AI-assisted review prompts"
          executor: "builtin.prompts"
          depends_on: ["validate_architecture", "security_scan", "test_coverage"]
          config:
            phases: [0, 1, 2, 3, 4]
            include_validation: true
          outputs:
            - "prompt_collection"

        - id: "prioritize_debt"
          type: "debt_prioritizer"
          title: "Prioritize and document technical debt"
          executor: "plugin.debt_analyzer"
          depends_on: ["quality_report", "validation_results"]
          config:
            business_impact: true
            effort_estimation: true
          outputs:
            - "debt_backlog"
```

---

## Step Executor Interface

### Base Executor Contract

```python
# src/codebase_reviewer/workflow/executor.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class StepConfig(BaseModel):
    """Configuration for a workflow step."""
    step_id: str
    step_type: str
    title: str
    executor: str
    config: Dict[str, Any]
    depends_on: List[str] = []
    parallel_with: List[str] = []
    outputs: List[str] = []

class StepResult(BaseModel):
    """Result of executing a workflow step."""
    step_id: str
    status: str  # "success", "failed", "skipped"
    outputs: Dict[str, Any]
    duration_seconds: float
    error: Optional[str] = None

class StepExecutor(ABC):
    """Base class for all step executors."""

    @abstractmethod
    def execute(
        self,
        config: StepConfig,
        context: Dict[str, Any]
    ) -> StepResult:
        """
        Execute a workflow step.

        Args:
            config: Step configuration
            context: Shared context from previous steps

        Returns:
            StepResult with outputs and status
        """
        pass

    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate step configuration before execution."""
        pass
```

---

## Built-in Executors (Adapters for Existing Code)

### Documentation Analyzer Executor

```python
# src/codebase_reviewer/workflow/executors/documentation.py

from codebase_reviewer.analyzers import DocumentationAnalyzer
from codebase_reviewer.workflow.executor import StepExecutor, StepConfig, StepResult

class DocumentationExecutor(StepExecutor):
    """Executor for documentation analysis steps."""

    def __init__(self):
        self.analyzer = DocumentationAnalyzer()

    def execute(self, config: StepConfig, context: Dict[str, Any]) -> StepResult:
        """Run documentation analysis."""
        repo_path = context.get("repo_path")

        # Run existing analyzer
        result = self.analyzer.analyze(repo_path)

        return StepResult(
            step_id=config.step_id,
            status="success",
            outputs={"documentation_analysis": result},
            duration_seconds=0.0  # Track actual time
        )

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate documentation analyzer config."""
        # Check for required fields
        return True
```

---

## Workflow Engine Implementation

```python
# src/codebase_reviewer/workflow/engine.py

import yaml
from typing import Dict, List, Optional
from pathlib import Path

from codebase_reviewer.workflow.executor import StepExecutor, StepConfig, StepResult
from codebase_reviewer.workflow.registry import ExecutorRegistry

class WorkflowEngine:
    """Executes configuration-driven workflows."""

    def __init__(self, registry: ExecutorRegistry):
        self.registry = registry
        self.context: Dict[str, Any] = {}

    def load_workflow(self, workflow_path: str) -> Dict:
        """Load workflow from YAML file."""
        with open(workflow_path, 'r') as f:
            return yaml.safe_load(f)

    def execute_workflow(
        self,
        workflow_config: Dict,
        repo_path: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, StepResult]:
        """
        Execute complete workflow.

        Args:
            workflow_config: Parsed workflow configuration
            repo_path: Path to repository
            progress_callback: Optional progress updates

        Returns:
            Dictionary of step_id -> StepResult
        """
        self.context["repo_path"] = repo_path
        results: Dict[str, StepResult] = {}

        # Extract all steps from all sections
        all_steps = self._flatten_steps(workflow_config)

        # Build dependency graph
        dep_graph = self._build_dependency_graph(all_steps)

        # Execute in topological order
        execution_order = self._topological_sort(dep_graph)

        for step_id in execution_order:
            step_config = all_steps[step_id]

            # Check if dependencies succeeded
            if not self._dependencies_met(step_config, results):
                results[step_id] = StepResult(
                    step_id=step_id,
                    status="skipped",
                    outputs={},
                    duration_seconds=0.0,
                    error="Dependencies not met"
                )
                continue

            # Get executor
            executor = self.registry.get_executor(step_config.executor)

            # Execute step
            if progress_callback:
                progress_callback(f"Executing: {step_config.title}")

            result = executor.execute(step_config, self.context)
            results[step_id] = result

            # Update context with outputs
            self.context.update(result.outputs)

        return results
```

---

## Mapping: Accordion Model → Configuration

### How the 6 Accordion Sections Map to Workflow Config

| Accordion Section | Workflow Section ID | Key Steps | Executors |
|-------------------|---------------------|-----------|-----------|
| **1. High-Level Reconnaissance** | `reconnaissance` | • Scan docs<br>• Map dependencies<br>• Static analysis | `builtin.documentation`<br>`builtin.code_structure`<br>`builtin.quality` |
| **2. Baseline Hygiene Checks** | `baseline_hygiene` | • Test coverage<br>• Build validation<br>• Entry points<br>• Comment check | `builtin.test_coverage`<br>`builtin.build_validator`<br>`plugin.comment_analyzer` |
| **3. Core Safety and Security** | `core_safety` | • Anti-patterns<br>• Error handling<br>• Security scan | `builtin.quality`<br>`plugin.security_scanner` |
| **4. Architecture Insights** | `architecture_insights` | • Visualize graphs<br>• Trace call flows<br>• VCS hotspots<br>• Duplication | `plugin.graph_viz`<br>`plugin.call_tracer`<br>`plugin.git_analyzer`<br>`builtin.quality` |
| **5. In-Depth Coverage** | `deep_coverage` | • Audit integrations<br>• Cohesion/coupling<br>• GenAI summarization<br>• Test criticality | `plugin.integration_auditor`<br>`builtin.validation`<br>`plugin.ai_summarizer`<br>`builtin.test_coverage` |
| **6. Principal Strategy** | `principal_strategy` | • Cross-ref design docs<br>• Dependency maps<br>• Profile hot paths<br>• Prioritize debt<br>• Generate prompts | `builtin.validation`<br>`plugin.graph_viz`<br>`plugin.profiler`<br>`plugin.debt_analyzer`<br>`builtin.prompts` |

---

## Example Workflow Configurations

### 1. Default Review (Current 5-Phase Approach)

```yaml
# workflows/default_review.yml
workflow:
  name: "Documentation-First Code Review"
  version: "2.0"
  description: "Our proven 5-phase documentation-first approach"

  sections:
    - id: "phase0"
      title: "Phase 0: Documentation Review"
      steps:
        - id: "analyze_docs"
          type: "documentation_analyzer"
          executor: "builtin.documentation"
          outputs: ["documentation_analysis"]

    - id: "phase1"
      title: "Phase 1: Architecture Analysis"
      steps:
        - id: "analyze_code"
          type: "code_analyzer"
          executor: "builtin.code"
          depends_on: ["analyze_docs"]
          outputs: ["code_analysis"]

        - id: "validate_architecture"
          type: "validation"
          executor: "builtin.validation"
          depends_on: ["analyze_docs", "analyze_code"]
          outputs: ["validation_results"]

    - id: "phase2_to_4"
      title: "Phases 2-4: Deep Analysis & Prompts"
      steps:
        - id: "generate_prompts"
          type: "prompt_generator"
          executor: "builtin.prompts"
          depends_on: ["validate_architecture"]
          config:
            phases: [0, 1, 2, 3, 4]
          outputs: ["prompt_collection"]
```

### 2. Security Audit Workflow

```yaml
# workflows/security_audit.yml
workflow:
  name: "Security-Focused Audit"
  version: "1.0"

  sections:
    - id: "security_scan"
      title: "Security Assessment"
      steps:
        - id: "dependency_vulnerabilities"
          type: "security_scanner"
          executor: "plugin.snyk"
          config:
            check_cves: true
            severity_threshold: "medium"

        - id: "code_security"
          type: "security_scanner"
          executor: "plugin.bandit"
          parallel_with: ["dependency_vulnerabilities"]

        - id: "secrets_scan"
          type: "security_scanner"
          executor: "plugin.trufflehog"
          parallel_with: ["dependency_vulnerabilities"]
```

### 3. Onboarding Review (New Developer Focus)

```yaml
# workflows/onboarding_review.yml
workflow:
  name: "New Developer Onboarding"
  version: "1.0"

  sections:
    - id: "getting_started"
      title: "Getting Started Guide"
      steps:
        - id: "setup_validation"
          type: "setup_validator"
          executor: "builtin.setup_checker"
          config:
            test_build: true
            test_run: true

        - id: "generate_onboarding_prompts"
          type: "prompt_generator"
          executor: "builtin.prompts"
          depends_on: ["setup_validation"]
          config:
            phases: [0, 3]  # Focus on docs and workflow
            audience: "junior_developer"
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Goal**: Create workflow engine infrastructure

- [ ] Define workflow YAML schema
- [ ] Implement `WorkflowEngine` class
- [ ] Create `ExecutorRegistry` for step executors
- [ ] Build base `StepExecutor` interface
- [ ] Add workflow validation logic

**Deliverables**:
- `src/codebase_reviewer/workflow/engine.py`
- `src/codebase_reviewer/workflow/executor.py`
- `src/codebase_reviewer/workflow/registry.py`
- `workflows/schema.json` (JSON Schema for validation)

### Phase 2: Adapter Layer (Week 3)
**Goal**: Wrap existing analyzers as executors

- [ ] Create `DocumentationExecutor` (wraps `DocumentationAnalyzer`)
- [ ] Create `CodeExecutor` (wraps `CodeAnalyzer`)
- [ ] Create `ValidationExecutor` (wraps `ValidationEngine`)
- [ ] Create `PromptExecutor` (wraps `PromptGenerator`)
- [ ] Register all built-in executors

**Deliverables**:
- `src/codebase_reviewer/workflow/executors/documentation.py`
- `src/codebase_reviewer/workflow/executors/code.py`
- `src/codebase_reviewer/workflow/executors/validation.py`
- `src/codebase_reviewer/workflow/executors/prompts.py`

### Phase 3: Default Workflows (Week 4)
**Goal**: Create workflow configs for existing use cases

- [ ] `workflows/default_review.yml` (current 5-phase approach)
- [ ] `workflows/principal_engineer_review.yml` (accordion approach)
- [ ] `workflows/quick_scan.yml` (fast overview)
- [ ] Update `AnalysisOrchestrator` to use workflow engine
- [ ] Maintain backward compatibility

**Deliverables**:
- 3+ workflow YAML files
- Updated orchestrator with workflow support
- Migration guide for existing users

### Phase 4: Plugin System (Week 5-6)
**Goal**: Enable custom executors

- [ ] Define plugin interface
- [ ] Create plugin discovery mechanism
- [ ] Build example plugins:
  - `SecurityScannerExecutor` (Bandit integration)
  - `GraphVisualizerExecutor` (Mermaid diagrams)
  - `GitAnalyzerExecutor` (VCS hotspots)
- [ ] Document plugin development guide

**Deliverables**:
- `src/codebase_reviewer/workflow/plugin.py`
- `plugins/` directory with examples
- `docs/PLUGIN_DEVELOPMENT.md`

### Phase 5: UI Integration (Week 7-8)
**Goal**: Accordion UI in web interface

- [ ] Add workflow selector to web UI
- [ ] Implement collapsible accordion sections
- [ ] Show step progress and status
- [ ] Enable step re-execution
- [ ] Add workflow editor (optional)

**Deliverables**:
- Updated Flask templates with accordion UI
- Workflow management endpoints
- Real-time progress updates (WebSocket/SSE)

---

## Benefits of This Approach

### 1. **Flexibility** 🎯
- **Multiple review types**: Principal engineer, security audit, onboarding, quick scan
- **Customizable per team**: Each team can define their own workflow
- **Context-specific**: Different workflows for different project types

### 2. **Maintainability** 🔧
- **Separation of concerns**: Workflow logic separate from analysis logic
- **Easier testing**: Test executors independently
- **Version control**: Workflows are YAML files, easy to track changes

### 3. **Extensibility** 🔌
- **Plugin architecture**: Add new steps without modifying core code
- **Community contributions**: Share workflows and plugins
- **Tool integration**: Wrap any CLI tool as an executor

### 4. **Backward Compatibility** ✅
- **Existing code unchanged**: Analyzers work as-is
- **Default workflow**: Matches current 5-phase behavior
- **Gradual migration**: Can adopt incrementally

### 5. **Best of Both Worlds** 🌟
- **Keep documentation-first**: Our unique validation approach
- **Add accordion flexibility**: Industry best practices
- **Enable AI integration**: Prompt generation at any step
- **Support strategic reviews**: Principal engineer workflows

---

## Comparison: Before vs After

| Aspect | Current Approach | Proposed Approach |
|--------|------------------|-------------------|
| **Workflow Definition** | Hardcoded in Python | YAML configuration files |
| **Customization** | Modify code | Edit YAML file |
| **Review Types** | One (5-phase) | Multiple (default, principal, security, onboarding) |
| **Step Execution** | Fixed order | Configurable dependencies |
| **Extensibility** | Fork and modify | Plugin system |
| **UI** | Linear progress | Accordion sections |
| **Sharing** | Share code | Share YAML files |
| **Testing** | Integration tests | Unit test executors + workflow validation |
| **Documentation-First** | ✅ Core feature | ✅ Preserved in default workflow |
| **Validation Engine** | ✅ Built-in | ✅ Available as executor |

---

## Migration Path

### For Existing Users

**No breaking changes**:
```python
# Old way (still works)
orchestrator = AnalysisOrchestrator()
result = orchestrator.run_full_analysis(repo_path)

# New way (opt-in)
from codebase_reviewer.workflow import WorkflowEngine

engine = WorkflowEngine.from_file("workflows/default_review.yml")
result = engine.execute(repo_path)
```

### For New Features

**Use workflow configs**:
```python
# Principal engineer review
engine = WorkflowEngine.from_file("workflows/principal_engineer_review.yml")
result = engine.execute(repo_path)

# Security audit
engine = WorkflowEngine.from_file("workflows/security_audit.yml")
result = engine.execute(repo_path)
```

---

## Next Steps

### Immediate Actions

1. **Review this proposal** with stakeholders
2. **Validate workflow schema** with sample configs
3. **Prototype workflow engine** (basic implementation)
4. **Test with default workflow** (ensure backward compatibility)

### Decision Points

- [ ] Approve overall architecture
- [ ] Confirm YAML as configuration format (vs JSON/TOML)
- [ ] Prioritize which workflows to implement first
- [ ] Decide on plugin system scope

### Success Criteria

- ✅ Existing 5-phase workflow works via YAML config
- ✅ Principal engineer accordion workflow implemented
- ✅ At least 2 custom plugins working
- ✅ Web UI shows accordion sections
- ✅ Documentation complete
- ✅ All tests passing
- ✅ Zero breaking changes for existing users

---

## Conclusion

This proposal **integrates the best of both approaches**:

- **Preserves our unique value**: Documentation-first validation
- **Adds industry best practices**: Accordion-style procedural workflow
- **Enables flexibility**: Configuration-driven, not code-driven
- **Maintains quality**: Type-safe, testable, extensible

**The result**: A powerful, flexible codebase review tool that serves multiple audiences (principal engineers, security teams, new developers) while maintaining our core differentiator (documentation validation).

**Recommendation**: Proceed with **Phase 1 (Foundation)** to validate the architecture with a working prototype.
