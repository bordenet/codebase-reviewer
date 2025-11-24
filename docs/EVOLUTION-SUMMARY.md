# Evolution System - Implementation Summary

## ✅ What Was Added

### 1. Self-Evolution Architecture
The codebase-reviewer now implements a **self-evolving system** where Phase 2 tools:
- Detect when they become obsolete
- Emit enhanced Phase 1 prompts with learnings
- Enable continuous improvement across generations

### 2. New Files Created

#### Prompt Templates
- `prompts/templates/phase1-regeneration-prompt-template.yaml`
  - Template for regeneration prompts
  - Includes learnings from previous generation
  - Specifies improvements needed

#### Schemas
- `prompts/schemas/learnings-schema.yaml`
  - Defines structure for capturing learnings
  - Documents all fields and their purposes
  - Provides usage examples

#### Go Packages
- `pkg/learnings/learnings.go`
  - Data structures for learnings
  - Load/Save functionality
  - YAML serialization

- `pkg/learnings/regeneration.go`
  - Regeneration prompt generator
  - Combines learnings with current state
  - Outputs YAML and Markdown

#### Example Phase 2 Tool
- `/tmp/codebase-reviewer/Cari/phase2-tools/cmd/update-docs/main.go`
  - Complete example showing evolution pattern
  - Loads previous learnings
  - Detects obsolescence
  - Generates regeneration prompt
  - Saves new learnings

- `/tmp/codebase-reviewer/Cari/phase2-tools/internal/validator/validator.go`
  - Obsolescence detection logic
  - Scoring system (0.0 = fresh, 1.0 = obsolete)
  - Multiple detection criteria

#### Documentation
- `docs/EVOLUTION-SYSTEM.md`
  - Comprehensive guide to evolution system
  - Architecture diagrams
  - Workflow examples
  - Best practices

## 🔄 How It Works

### Generation 1 (Initial)
```
Phase 1 Tool → LLM → Phase 2 Tools (Gen 1)
                      ↓
                   Run tools
                      ↓
                Save learnings.yaml
```

### Generation 2+ (Evolution)
```
Phase 2 Tools (Gen N) detect obsolescence
         ↓
Generate phase1-regeneration-prompt.yaml
         ↓
User runs: generate-docs --scorch
         ↓
Provide regeneration prompt to LLM
         ↓
LLM generates Phase 2 Tools (Gen N+1)
         ↓
Gen N+1 tools are BETTER:
  ✓ Fixed issues from Gen N
  ✓ Handle edge cases
  ✓ Better performance
  ✓ New capabilities
```

## 📊 Learnings Captured

Every Phase 2 tool run captures:

1. **What Worked Well**
   - Successful operations
   - Accurate detections
   - Good performance

2. **What Failed**
   - Errors encountered
   - Failed detections
   - Performance bottlenecks

3. **Edge Cases Discovered**
   - Unexpected scenarios
   - Current vs desired behavior
   - Workarounds

4. **Patterns Identified**
   - Code patterns
   - Architecture patterns
   - Naming conventions

5. **Improvements Needed**
   - Performance optimizations
   - Accuracy improvements
   - New features

6. **Codebase Changes**
   - Structural changes
   - Language changes
   - Framework changes
   - Dependency changes

## 🎯 Obsolescence Detection

Phase 2 tools detect obsolescence based on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Fingerprint mismatch | +0.3 | Core structure changed |
| File count change >20% | +0.2 | Significant growth/shrinkage |
| New languages | +0.2 | Tool can't parse them |
| New frameworks | +0.15 | New patterns to detect |
| Architecture changes | +0.15 | Different patterns emerged |

**Threshold**: Score > 0.5 = Obsolete

## 📝 All LLM Prompts as YAML

**Critical Feature**: ALL LLM prompts are stored as YAML files:

### Why YAML?
- ✅ Human-readable
- ✅ Easy to edit
- ✅ Easy to inspect
- ✅ Version controllable
- ✅ Programmatically parseable

### Prompt Locations
```
prompts/
├── templates/
│   ├── phase1-prompt-template.yaml              # Initial prompt
│   └── phase1-regeneration-prompt-template.yaml # Regeneration template
└── schemas/
    └── learnings-schema.yaml                    # Learnings structure

/tmp/codebase-reviewer/{name}/
├── phase1-llm-prompt.yaml                       # Generated initial prompt
└── phase1-regeneration-prompt.yaml              # Generated regeneration prompt
```

### Inspecting Prompts
```bash
# View initial prompt
cat /tmp/codebase-reviewer/Cari/phase1-llm-prompt.yaml

# View regeneration prompt (after obsolescence detected)
cat /tmp/codebase-reviewer/Cari/phase1-regeneration-prompt.yaml

# Edit before providing to LLM
code /tmp/codebase-reviewer/Cari/phase1-regeneration-prompt.yaml
```

## 🚀 Usage Example

### First Run (Gen 1)
```bash
# Generate initial prompt
./bin/generate-docs -v ./Cari

# Provide to LLM → Get Phase 2 tools

# Run Phase 2 tools
cd /tmp/codebase-reviewer/Cari/phase2-tools
make build
./bin/update-docs --path /Users/matt/GitHub/CallBox/Cari

# Output: Documentation + learnings.yaml
```

### After Codebase Changes (Gen 2)
```bash
# Run Phase 2 tools again
./bin/update-docs --path /Users/matt/GitHub/CallBox/Cari

# Tool detects obsolescence:
# ⚠️  Tool has become obsolete!
# ✅ Regeneration prompt saved

# Review regeneration prompt
cat /tmp/codebase-reviewer/Cari/phase1-regeneration-prompt.yaml

# Regenerate
cd /Users/matt/GitHub/CallBox
./bin/generate-docs --scorch ./Cari

# Provide regeneration prompt to LLM → Get improved Phase 2 tools
```

## 💡 Key Benefits

### 1. Continuous Improvement
Each generation is measurably better:
- Fixes discovered bugs
- Handles edge cases
- Improves performance
- Adds new capabilities

### 2. Transparent Evolution
All prompts are YAML files:
- Easy to inspect what the tool is learning
- Easy to edit prompts before regeneration
- Easy to track evolution over time
- Easy to share learnings

### 3. Codebase-Specific
Tools adapt to YOUR codebase:
- Learn your patterns
- Optimize for your languages
- Generate reports you need
- Handle your edge cases

### 4. No Manual Intervention
When codebase changes too much:
- Tool detects it automatically
- Generates regeneration prompt automatically
- Includes all learnings automatically
- You just run --scorch and provide to LLM

## 📁 File Summary

### Git-Tracked (Safe for Public GitHub)
```
✅ prompts/templates/phase1-regeneration-prompt-template.yaml
✅ prompts/schemas/learnings-schema.yaml
✅ pkg/learnings/learnings.go
✅ pkg/learnings/regeneration.go
✅ docs/EVOLUTION-SYSTEM.md
✅ EVOLUTION-SUMMARY.md (this file)
```

### Non-Tracked (Proprietary)
```
🔒 /tmp/codebase-reviewer/Cari/phase1-regeneration-prompt.yaml
🔒 /tmp/codebase-reviewer/Cari/learnings.yaml
🔒 /tmp/codebase-reviewer/Cari/phase2-tools/
```

## ✅ Requirements Met

Your requirements:
1. ✅ Phase 2 tools detect when they can't perform direct offline updates
2. ✅ Tools emit FULL, DETAILED LLM prompt to regenerate Phase 1
3. ✅ Prompts include learnings and discoveries from previous runs
4. ✅ Tools build in mutation/evolution
5. ✅ Tools get progressively better from generation to generation
6. ✅ ALL LLM prompts saved as YAML text files
7. ✅ Easy access and inspection of prompts

## 🎉 Status

**Evolution System**: ✅ COMPLETE

The codebase-reviewer now has a complete self-evolution system that:
- Learns from every run
- Detects obsolescence automatically
- Generates enhanced prompts with learnings
- Stores all prompts as YAML
- Enables continuous improvement

**Next**: Run the tool and watch it evolve!

---

**Created**: 2025-11-23  
**Status**: Ready for use
