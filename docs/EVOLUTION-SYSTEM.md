# Self-Evolving Tool System

## Overview

The codebase-reviewer implements a **self-evolving architecture** where tools progressively improve across generations. When Phase 2 tools detect they've become obsolete, they emit enhanced Phase 1 prompts that incorporate all learnings, creating a continuous improvement cycle.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    GENERATION 1                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1 Tool  ──►  LLM  ──►  Phase 2 Tools (Gen 1)             │
│  (scan + prompt)    (you)     (offline docs)                    │
│                                                                  │
│  Phase 2 runs, collects learnings:                              │
│  ✓ What worked well                                             │
│  ✓ What failed                                                  │
│  ✓ Edge cases discovered                                        │
│  ✓ Patterns identified                                          │
│  ✓ Improvements needed                                          │
│                                                                  │
│  Saves: /tmp/codebase-reviewer/{name}/learnings.yaml            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Codebase changes significantly
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GENERATION 2                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 2 (Gen 1) detects obsolescence:                          │
│  • Fingerprint mismatch                                         │
│  • File count changed >20%                                      │
│  • New languages/frameworks                                     │
│  • Architecture shifts                                          │
│                                                                  │
│  Emits enhanced Phase 1 prompt:                                 │
│  phase1-regeneration-prompt.yaml                                │
│                                                                  │
│  Enhanced prompt includes:                                      │
│  ✓ All learnings from Gen 1                                     │
│  ✓ What to improve                                              │
│  ✓ New patterns to detect                                       │
│  ✓ Better error handling                                        │
│  ✓ Performance optimizations                                    │
│                                                                  │
│  User runs: generate-docs --scorch {path}                       │
│  Provides regeneration prompt to LLM                            │
│                                                                  │
│  LLM generates Phase 2 Tools (Gen 2) with improvements          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Process repeats
                              ▼
                    GENERATION 3, 4, 5...
                    (progressively better)
```

## Key Components

### 1. Learnings System (`pkg/learnings/`)

**Purpose**: Capture operational insights from every Phase 2 tool run

**Structure** (`learnings.yaml`):
```yaml
metadata:
  tool_name: "update-docs"
  tool_version: "1.0.0"
  generation: 1
  run_date: "2025-11-23T19:00:00Z"
  codebase_fingerprint: "sha256:abc123..."

execution_metrics:
  duration_seconds: 12.5
  files_processed: 827
  errors_encountered: 0
  reports_generated: 15

what_worked_well:
  - category: "parsing"
    description: "TypeScript AST parsing was accurate"
    confidence: "high"
    examples: ["Successfully parsed 537 TS files"]

what_failed:
  - category: "detection"
    description: "Failed to detect Mermaid diagrams in comments"
    error_type: "regex_mismatch"
    frequency: "often"
    impact: "minor"
    suggested_fix: "Use multi-line regex with (?s) flag"

edge_cases_discovered:
  - case_id: "EC001"
    description: "Monorepo with nested package.json files"
    trigger_condition: "Multiple package.json at different depths"
    current_behavior: "Only detects root package.json"
    desired_behavior: "Detect all package.json and build dependency tree"
    priority: "high"

patterns_identified:
  - pattern_type: "architecture"
    pattern_name: "State Machine Agents"
    description: "LLM agents use state machine pattern"
    frequency: 2
    locations: ["agent-api/src/agents/receptionist", "agent-api/src/agents/service-scheduler"]
    significance: "Core architectural pattern"
    recommendation: "Create dedicated state machine diagram generator"

improvements_needed:
  - improvement_id: "IMP001"
    category: "performance"
    description: "Parallel file processing"
    current_state: "Sequential processing, 12.5s for 827 files"
    desired_state: "Parallel processing, target <5s"
    priority: "high"
    effort_estimate: "medium"
    implementation_hint: "Use worker pool with goroutines"

obsolescence_indicators:
  is_obsolete: false
  obsolescence_score: 0.15
  reasons: []
  confidence: "high"
  recommendation: "continue"
```

### 2. Obsolescence Detection (`internal/validator/`)

**Purpose**: Detect when Phase 2 tools can no longer accurately process the codebase

**Detection Logic**:
- **Fingerprint mismatch** (+0.3): Core structure changed
- **File count change >20%** (+0.2): Significant growth/shrinkage
- **New languages** (+0.2): Tool doesn't know how to parse them
- **New frameworks** (+0.15): New patterns to detect
- **Architecture changes** (+0.15): Different patterns emerged

**Threshold**: Score > 0.5 = Obsolete

**Example**:
```go
obsolescence := validator.CheckObsolescence(currentScan, previousLearnings, log)
if obsolescence.IsObsolete {
    // Generate regeneration prompt
    regenPrompt := learnings.GenerateRegenerationPrompt(...)
    learnings.SaveRegenerationPrompt(regenPrompt, outputDir)

    log.Info("Tool is obsolete. Regeneration prompt saved.")
    log.Info("Run: generate-docs --scorch /path/to/codebase")
    os.Exit(2) // Exit code 2 = obsolete
}
```

### 3. Regeneration Prompt (`pkg/learnings/regeneration.go`)

**Purpose**: Generate enhanced Phase 1 prompt with all learnings

**Output**: `phase1-regeneration-prompt.yaml`

**Contents**:
- All learnings from previous generation
- What worked / what failed
- Edge cases discovered
- Patterns identified
- Specific improvements needed
- Enhanced requirements for Phase 2 tools

**Usage**:
1. Phase 2 tool detects obsolescence
2. Generates regeneration prompt
3. User runs `generate-docs --scorch {path}`
4. User provides regeneration prompt to LLM
5. LLM generates improved Phase 2 tools



## Workflow

### Initial Generation (Gen 1)

```bash
# Step 1: Run Phase 1 tool
cd /Users/matt/GitHub/CallBox
./bin/generate-docs -v ./Cari

# Output:
# - /tmp/codebase-reviewer/Cari/phase1-llm-prompt.yaml
# - /tmp/codebase-reviewer/Cari/phase1-llm-prompt.md

# Step 2: Provide prompt to LLM (Augment Agent)
# LLM generates Phase 2 tools in:
# - /tmp/codebase-reviewer/Cari/phase2-tools/

# Step 3: Build and run Phase 2 tools
cd /tmp/codebase-reviewer/Cari/phase2-tools
make build
./bin/update-docs --path /Users/matt/GitHub/CallBox/Cari

# Output:
# - /tmp/codebase-reviewer/Cari/reference-materials/ (docs)
# - /tmp/codebase-reviewer/Cari/learnings.yaml (learnings)
```

### Subsequent Generations (Gen 2+)

```bash
# Codebase changes over time...
# New services added, languages changed, etc.

# Step 1: Run Phase 2 tool (Gen 1)
cd /tmp/codebase-reviewer/Cari/phase2-tools
./bin/update-docs --path /Users/matt/GitHub/CallBox/Cari

# Tool detects obsolescence:
# ⚠️  Tool has become obsolete!
# ⚠️  Obsolescence score: 0.65
# ⚠️  Reason: Codebase fingerprint changed (and other changes)
#
# ✅ Regeneration prompt saved to:
#    - /tmp/codebase-reviewer/Cari/phase1-regeneration-prompt.yaml
#    - /tmp/codebase-reviewer/Cari/phase1-regeneration-prompt.md
#
# Next steps:
# 1. Review the regeneration prompt
# 2. Run Phase 1 tool with --scorch flag
# 3. Provide the regeneration prompt to the LLM

# Step 2: Review regeneration prompt
cat /tmp/codebase-reviewer/Cari/phase1-regeneration-prompt.md

# Step 3: Re-run Phase 1 with --scorch
cd /Users/matt/GitHub/CallBox
./bin/generate-docs --scorch ./Cari

# Step 4: Provide regeneration prompt to LLM
# LLM reads learnings and generates IMPROVED Phase 2 tools (Gen 2)

# Step 5: Build and run Gen 2 tools
cd /tmp/codebase-reviewer/Cari/phase2-tools
make build
./bin/update-docs --path /Users/matt/GitHub/CallBox/Cari

# Gen 2 tools are better:
# ✓ Fixed issues from Gen 1
# ✓ Handle edge cases discovered
# ✓ Better performance
# ✓ New report types
# ✓ Enhanced detection logic
```

## Benefits

### 1. Continuous Improvement
Each generation is measurably better than the last:
- Fixes bugs discovered in previous runs
- Handles edge cases that were missed
- Implements performance optimizations
- Adds new capabilities based on patterns discovered

### 2. Codebase-Specific Optimization
Tools evolve to match the specific codebase:
- Learn unique patterns (e.g., "State Machine Agents")
- Adapt to architecture changes
- Optimize for specific languages/frameworks
- Generate reports tailored to the project

### 3. Knowledge Preservation
All learnings are preserved across generations:
- What worked well (keep doing it)
- What failed (fix it)
- Edge cases (handle them)
- Patterns (leverage them)

### 4. Transparent Evolution
All LLM prompts stored as YAML:
- Easy to inspect: `cat prompts/phase2-regeneration/*.yaml`
- Easy to edit: Modify YAML before providing to LLM
- Easy to version: Track prompt evolution in git
- Easy to understand: Human-readable format

### 5. Offline Operation
Phase 2 tools run completely offline:
- No LLM API calls during documentation generation
- Fast execution (seconds, not minutes)
- No API costs
- Works in air-gapped environments

## File Locations

### Git-Tracked (Generic Tool Code)
```
codebase-reviewer/
├── prompts/
│   ├── templates/
│   │   ├── phase1-prompt-template.yaml              # Initial prompt
│   │   └── phase1-regeneration-prompt-template.yaml # Regeneration template
│   └── schemas/
│       └── learnings-schema.yaml                    # Learnings structure
├── pkg/
│   └── learnings/
│       ├── learnings.go                             # Learnings data structures
│       └── regeneration.go                          # Regeneration prompt generator
└── docs/
    └── EVOLUTION-SYSTEM.md                          # This document
```

### Non-Tracked (Codebase-Specific)
```
/tmp/codebase-reviewer/{codebase-name}/
├── phase1-llm-prompt.yaml                           # Gen 1 prompt
├── phase1-llm-prompt.md
├── phase1-regeneration-prompt.yaml                  # Gen 2+ prompt
├── phase1-regeneration-prompt.md
├── learnings.yaml                                   # Accumulated learnings
├── phase2-tools/                                    # Generated tools
│   ├── cmd/update-docs/main.go
│   ├── internal/
│   │   ├── scanner/
│   │   ├── analyzer/
│   │   ├── generator/
│   │   └── validator/
│   └── Makefile
└── reference-materials/                             # Generated docs
    ├── architecture/
    ├── services/
    ├── ai/
    └── ...
```

## Example: Evolution in Action

### Generation 1
**Prompt**: Standard Phase 1 prompt
**Tools**: Basic TypeScript parser, simple reports
**Learnings**:
- ✓ TypeScript parsing works well
- ✗ Failed to detect state machine pattern
- ✗ Slow performance (12.5s for 827 files)
- Edge case: Nested package.json files

### Generation 2
**Prompt**: Regeneration prompt with Gen 1 learnings
**Tools**: Improved with:
- State machine pattern detector
- Parallel file processing (5.2s for 827 files)
- Nested package.json handler
- New report: State machine diagrams

**Learnings**:
- ✓ State machine detection works perfectly
- ✓ Performance improved 2.4x
- ✗ Failed to detect LLM prompts in code
- Edge case: Multi-line YAML in TypeScript strings

### Generation 3
**Prompt**: Regeneration prompt with Gen 1 + Gen 2 learnings
**Tools**: Further improved with:
- LLM prompt extractor
- Multi-line YAML parser
- Even better performance (3.8s)
- New report: LLM prompt catalog

**Result**: Each generation builds on previous learnings

## Best Practices

### 1. Review Learnings Regularly
```bash
# Check what the tool learned
cat /tmp/codebase-reviewer/{name}/learnings.yaml

# Look for patterns
grep -A 5 "patterns_identified:" learnings.yaml
```

### 2. Edit Regeneration Prompts
```bash
# Before providing to LLM, review and edit
code /tmp/codebase-reviewer/{name}/phase1-regeneration-prompt.yaml

# Add custom requirements
# Adjust priorities
# Clarify ambiguities
```

### 3. Track Generations
```bash
# Keep a log of generations
echo "Gen 2: $(date) - Added state machine detection" >> GENERATIONS.log
```

### 4. Preserve Successful Generations
```bash
# Backup working tools before regenerating
cp -r /tmp/codebase-reviewer/{name}/phase2-tools \
      /tmp/codebase-reviewer/{name}/phase2-tools-gen1-backup
```

## Future Enhancements

- **Automatic regeneration**: Tool regenerates itself when obsolete
- **A/B testing**: Compare Gen N vs Gen N+1 performance
- **Learnings visualization**: Dashboard showing evolution over time
- **Cross-codebase learnings**: Share patterns across projects
- **Confidence scoring**: Track prediction accuracy over time

---

**Status**: ✅ Evolution system implemented
**Next**: Run Phase 1 tool and let the evolution begin!
