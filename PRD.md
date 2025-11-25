# Product Requirements Document: Self-Evolving Codebase Documentation System

**Version**: 2.0
**Date**: 2025-11-24
**Status**: In Development
**Owner**: Matt Bordenet

---

## Executive Summary

Build a **self-evolving system** that analyzes proprietary codebases and generates **offline tools** capable of reproducing LLM-quality documentation **without requiring LLM access**. The system must detect when it becomes obsolete and automatically regenerate improved versions of itself.

**Key Innovation**: LLM generates the tools, then the tools replace the LLM.

---

## Problem Statement

### Current State (Broken)
- Manual code documentation is time-consuming and becomes stale
- LLM-based analysis requires API access and costs money per run
- Documentation drifts from code as changes occur
- No automated way to keep docs synchronized with code

### Desired State (Mission)
- **One-time LLM cost**: LLM generates offline tools once
- **Infinite offline runs**: Tools regenerate docs without LLM
- **Self-awareness**: Tools detect when they're obsolete
- **Self-evolution**: Tools regenerate themselves with improvements
- **Zero drift**: Docs stay synchronized with code automatically

---

## Success Criteria

1. **Fidelity**: Tool-generated docs ≥ 95% quality of LLM-generated docs
2. **Offline**: Tools run without internet/LLM access
3. **Speed**: Tool execution < 10% of LLM analysis time
4. **Cost**: After initial generation, $0 per documentation update
5. **Self-Evolution**: Gen 2 tools measurably better than Gen 1
6. **Automation**: Zero manual intervention after initial setup

---

## System Architecture

### The Two-Phase Evolution System

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: LLM-Powered Tool Generation (One-Time)            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Codebase → Analyzer → Prompt → LLM → Phase 2 Tools        │
│                                           ↓                 │
│                                    Compile & Validate       │
│                                           ↓                 │
│                                    Initial Docs Generated   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Offline Tool Execution (Infinite Runs)            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Codebase Changes → Phase 2 Tools → Updated Docs           │
│                           ↓                                 │
│                    Obsolescence Check                       │
│                           ↓                                 │
│                  [Still Valid] → Continue                   │
│                           ↓                                 │
│                  [Obsolete] → Regeneration Prompt           │
│                           ↓                                 │
│                    Back to Phase 1 (Gen 2)                  │
└─────────────────────────────────────────────────────────────┘
```

### Self-Evolution Loop

```
Gen 1 Tools → Run → Capture Learnings → Detect Obsolescence
                                              ↓
                                    Regeneration Prompt
                                              ↓
                                    LLM → Gen 2 Tools (Improved)
                                              ↓
                                    Gen 2 Tools → Run → ...
```

---

## Core Components

### 1. Phase 1: Analyzer & Prompt Generator
**Purpose**: Analyze codebase and generate LLM prompt

**Inputs**:
- Codebase path (e.g., `/Users/Matt/GitHub/CallBox`)
- Analysis depth (quick/deep)
- Target LLM provider (Claude/OpenAI)

**Outputs**:
- Structured codebase analysis (JSON)
- LLM prompt (Markdown + YAML)
- Repository metadata

**Technology**: Go (existing: `cmd/generate-docs/main.go`)

**Status**: ✅ **COMPLETE**

### 2. LLM Integration Layer
**Purpose**: Automate LLM interaction

**Capabilities**:
- Send prompts to Claude/OpenAI APIs
- Parse LLM responses
- Extract code blocks from markdown
- Validate response completeness
- Handle errors and retries

**Inputs**:
- Phase 1 prompt
- API credentials
- LLM provider config

**Outputs**:
- Phase 2 tool source code (Go files)
- LLM analysis artifacts
- Validation report

**Technology**: Python (`src/codebase_reviewer/llm/`)

**Status**: ❌ **NOT IMPLEMENTED**

### 3. Phase 2 Tool Generator
**Purpose**: Compile and validate LLM-generated tools

**Capabilities**:
- Extract Go code from LLM response
- Create proper Go project structure
- Compile tools (`go build`)
- Run validation tests
- Install tools to output directory

**Inputs**:
- LLM-generated code
- Target codebase path
- Output directory

**Outputs**:
- Compiled Phase 2 tools (binaries)
- Validation report
- Initial documentation

**Technology**: Python + Go

**Status**: ❌ **NOT IMPLEMENTED**

### 4. Phase 2 Tools (LLM-Generated)
**Purpose**: Offline documentation generation

**Capabilities**:
- Parse source code (AST analysis)
- Extract architecture patterns
- Generate Mermaid diagrams
- Create API documentation
- Detect integration points
- Track dependencies
- Measure code quality

**Inputs**:
- Codebase path
- Configuration (YAML)

**Outputs**:
- PRD (Product Requirements Document)
- Design specifications
- Architecture diagrams
- API documentation
- Integration maps
- Execution log (for learnings)

**Technology**: Go (generated by LLM)

**Status**: ❌ **NOT IMPLEMENTED** (must be generated)

### 5. Validation Framework
**Purpose**: Prove tools reproduce LLM quality

**Capabilities**:
- Compare LLM output vs Tool output
- Calculate fidelity score (0-1)
- Identify missing information
- Measure format compliance
- Generate comparison reports

**Inputs**:
- LLM-generated documentation
- Tool-generated documentation

**Outputs**:
- Fidelity score (target: ≥0.95)
- Comparison report (Markdown)
- Gap analysis

**Technology**: Python

**Status**: ❌ **NOT IMPLEMENTED**

### 6. Obsolescence Detector
**Purpose**: Determine when tools need regeneration

**Detection Criteria**:
- Codebase structure changed significantly (>30% files added/removed)
- New languages/frameworks introduced
- Major dependency changes
- Tool execution errors increased
- Documentation coverage dropped

**Inputs**:
- Current codebase state
- Baseline codebase fingerprint
- Tool execution logs

**Outputs**:
- Obsolescence score (0-1)
- Obsolescence reason
- Trigger regeneration (yes/no)

**Technology**: Go (part of Phase 2 tools)

**Status**: ❌ **NOT IMPLEMENTED**

### 7. Learnings Capture System
**Purpose**: Extract insights for next generation

**Captures**:
- What worked well
- What failed
- Edge cases discovered
- Patterns identified
- Performance bottlenecks
- Codebase changes detected

**Inputs**:
- Tool execution logs
- Error reports
- Performance metrics

**Outputs**:
- `learnings.yaml` file
- Improvement recommendations

**Technology**: Go (part of Phase 2 tools)

**Status**: 🟡 **PARTIAL** (design exists in `pkg/learnings/`)

### 8. Regeneration System
**Purpose**: Create improved next-generation tools

**Capabilities**:
- Load learnings from previous generation
- Generate enhanced Phase 1 prompt
- Include all learnings in prompt
- Trigger LLM to create Gen 2 tools
- Validate improvements

**Inputs**:
- Learnings from Gen N
- Obsolescence report
- Current codebase state

**Outputs**:
- Enhanced Phase 1 prompt
- Gen N+1 tools (via LLM)

**Technology**: Python + Go

**Status**: ❌ **NOT IMPLEMENTED**

---

## User Workflows

### Workflow 1: Initial Setup (One-Time)

```bash
# Step 1: Analyze codebase and generate Phase 2 tools
review-codebase evolve /Users/Matt/GitHub/CallBox \
  --llm-provider anthropic \
  --api-key $ANTHROPIC_API_KEY \
  --output-dir /tmp/callbox-reviewer

# System does:
# 1. Analyzes CallBox codebase
# 2. Generates Phase 1 prompt
# 3. Sends to Claude API
# 4. Extracts Phase 2 tool code
# 5. Compiles tools
# 6. Runs tools to generate initial docs
# 7. Validates fidelity ≥ 95%

# Output:
# ✅ /tmp/callbox-reviewer/phase2-tools/bin/generate-docs
# ✅ /tmp/callbox-reviewer/docs/ (initial documentation)
# ✅ Fidelity: 97% ✅
```

### Workflow 2: Offline Updates (Daily/Weekly)

```bash
# Run Phase 2 tools (no LLM needed)
/tmp/callbox-reviewer/phase2-tools/bin/generate-docs \
  /Users/Matt/GitHub/CallBox

# System does:
# 1. Scans codebase for changes
# 2. Updates documentation
# 3. Checks for obsolescence
# 4. Captures learnings

# Output:
# ✅ Updated docs in /tmp/callbox-reviewer/docs/
# ✅ Obsolescence: 0.15 (still valid)
# ✅ Learnings saved to learnings.yaml
```

### Workflow 3: Automatic Regeneration (When Obsolete)

```bash
# Watch mode (continuous monitoring)
review-codebase watch /Users/Matt/GitHub/CallBox \
  --tools-dir /tmp/callbox-reviewer/phase2-tools \
  --check-interval 3600 \
  --auto-regenerate

# System does:
# 1. Runs Phase 2 tools every hour
# 2. Detects obsolescence score > 0.65
# 3. Loads learnings from Gen 1
# 4. Generates enhanced Phase 1 prompt
# 5. Sends to LLM for Gen 2 tools
# 6. Compiles and validates Gen 2
# 7. Switches to Gen 2 tools

# Output:
# ⚠️  Obsolescence detected: 0.72
# 🔄 Regenerating with learnings...
# ✅ Gen 2 tools created (15% faster, 3 new features)
```

---

## Technical Requirements

### Performance
- Phase 1 analysis: < 60 seconds for 100K LOC
- LLM response: < 120 seconds (depends on provider)
- Phase 2 tool compilation: < 30 seconds
- Phase 2 tool execution: < 10 seconds for 100K LOC
- Fidelity validation: < 5 seconds

### Scalability
- Support codebases up to 1M LOC
- Handle 100+ repositories in monorepo
- Parallel processing for file analysis
- Incremental updates (only changed files)

### Security
- All outputs to `/tmp/` or user-specified directory
- Never commit proprietary code to git
- API keys stored securely (env vars)
- Sanitize file paths in logs
- Multi-layer .gitignore protection

### Reliability
- Graceful degradation if LLM unavailable
- Retry logic for API failures
- Validation before overwriting docs
- Backup previous generation tools
- Rollback capability

---

## Success Metrics

### Quantitative
- **Fidelity Score**: ≥ 95% (Tool output vs LLM output)
- **Cost Reduction**: > 99% (after initial generation)
- **Speed Improvement**: > 90% (Tool vs LLM execution time)
- **Obsolescence Detection Accuracy**: > 90%
- **Gen 2 Improvement**: ≥ 10% better than Gen 1

### Qualitative
- Tools compile without errors
- Documentation is accurate and complete
- Self-evolution produces measurable improvements
- Zero manual intervention required
- Developers trust the generated docs

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM generates broken code | High | Validation framework, compilation tests |
| Tools can't parse new language | Medium | Extensible parser architecture |
| Obsolescence detection too sensitive | Medium | Tunable thresholds, manual override |
| Fidelity < 95% | High | Iterative prompt improvement, validation |
| API costs too high | Low | Batch processing, caching |
| Proprietary code leaked | Critical | Multi-layer .gitignore, /tmp/ outputs |

---

## Timeline & Milestones

### Phase A: Foundation (Week 1)
- ✅ PRD complete
- ✅ README updated
- ✅ Manual test successful
- ✅ LLM integration implemented

### Phase B: Automation (Week 2)
- ✅ Phase 2 tool generator working
- ✅ Compilation and validation automated
- ✅ Initial docs generated

### Phase C: Validation (Week 3)
- ✅ Comparison framework implemented
- ✅ Fidelity ≥ 95% achieved
- ✅ Gap analysis automated

### Phase D: Evolution (Week 4)
- ✅ Obsolescence detection working
- ✅ Learnings capture implemented
- ✅ Regeneration loop automated
- ✅ Gen 2 tools validated

---

## Out of Scope (V1)

- Multi-language Phase 2 tools (Go only for V1)
- Real-time code change detection (polling only)
- Distributed execution
- Web UI for tool management
- Integration with CI/CD pipelines

---

## Appendix

### Related Documents
- `CRITICAL_GAP_ANALYSIS.md` - Current state assessment
- `MISSION_RECOVERY_PLAN.md` - Implementation plan
- `PRODUCTION_READINESS_ASSESSMENT.md` - What works today

### References
- Phase 1 template: `prompts/templates/phase1-prompt-template.yaml`
- Learnings design: `pkg/learnings/learnings.go`
- Existing analyzer: `cmd/generate-docs/main.go`
