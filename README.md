# Codebase Reviewer - Self-Evolving Documentation System

**The Mission**: Generate offline tools that reproduce LLM-quality documentation **without requiring LLM access**.

## 🎯 The Big Idea

**Problem**: LLMs are expensive and require internet access for every documentation update.

**Solution**: Use the LLM **once** to generate **offline tools** that can regenerate documentation infinitely without the LLM.

**Innovation**: The tools detect when they become obsolete and automatically regenerate improved versions of themselves.

```
┌─────────────────────────────────────────────────────────┐
│ PHASE 1: LLM Generates Tools (One-Time Cost)           │
├─────────────────────────────────────────────────────────┤
│  Codebase → Analyzer → LLM → Offline Tools (Go)        │
│                                    ↓                    │
│                            Initial Docs Generated       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ PHASE 2: Tools Run Offline (Infinite, Free)            │
├─────────────────────────────────────────────────────────┤
│  Code Changes → Tools → Updated Docs (No LLM!)          │
│                    ↓                                    │
│              Obsolete? → Regenerate (Gen 2)             │
└─────────────────────────────────────────────────────────┘
```

## 🚀 What This System Does

**Phase 1 (One-Time)**:
- Analyzes your codebase deeply
- Generates an LLM prompt
- LLM creates **offline Go tools** tailored to your codebase
- Tools compile and validate

**Phase 2 (Infinite)**:
- Tools regenerate docs **without LLM** (offline, free, fast)
- Tools detect when codebase changed too much
- Tools capture learnings and trigger regeneration
- Gen 2 tools are better than Gen 1 (self-evolution)

**Key Benefits**:

- ✅ **One-time LLM cost** instead of per-run
- ✅ **Offline execution** (no internet needed)
- ✅ **10x faster** than LLM analysis
- ✅ **Self-evolving** (gets better over time)
- ✅ **≥95% fidelity** to LLM output

---

## 📊 Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| **Phase 1: Prompt Generation** | ✅ Complete | Go tool works |
| **LLM Integration** | ❌ Missing | Manual copy/paste only |
| **Phase 2: Tool Generation** | ❌ Missing | 80% of mission |
| **Offline Execution** | ❌ Missing | Core value prop |
| **Self-Evolution** | ❌ Missing | Differentiation |
| **Validation Framework** | ❌ Missing | Quality assurance |

**Mission Completion**: ~20% ⚠️

See [PRD.md](PRD.md) for complete roadmap and [CRITICAL_GAP_ANALYSIS.md](CRITICAL_GAP_ANALYSIS.md) for detailed gap analysis.

---

## 🚀 Quick Start

### The Complete Workflow (What You Want)

```bash
# ONE COMMAND to generate offline tools (coming soon):
review-codebase evolve /path/to/your/codebase \
  --llm-provider anthropic \
  --api-key $ANTHROPIC_API_KEY \
  --output-dir /tmp/my-codebase-reviewer

# This will:
# 1. Analyze your codebase
# 2. Send prompt to LLM
# 3. Generate Phase 2 tools
# 4. Compile and validate tools
# 5. Generate initial documentation

# Then run tools offline (no LLM needed):
/tmp/my-codebase-reviewer/phase2-tools/bin/generate-docs /path/to/your/codebase

# Watch for changes and auto-update:
review-codebase watch /path/to/your/codebase \
  --tools-dir /tmp/my-codebase-reviewer/phase2-tools \
  --auto-regenerate
```

**Status**: 🚧 **In Development** - See [PRD.md](PRD.md) for full roadmap

### Current Capabilities (What Works Today)

#### Option A: Manual Workflow (Go Tool)

```bash
# Step 1: Build Phase 1 tool
make build

# Step 2: Generate LLM prompt
./bin/generate-docs /path/to/your/codebase

# Step 3: Send prompt to LLM (manual)
cat /tmp/codebase-reviewer/{name}/phase1-llm-prompt.md
# Copy/paste to Claude

# Step 4: Save LLM's Phase 2 tools (manual)
# LLM will generate Go code - save to /tmp/codebase-reviewer/{name}/phase2-tools/

# Step 5: Compile and run Phase 2 tools
cd /tmp/codebase-reviewer/{name}/phase2-tools/
go build ./cmd/generate-docs/
./generate-docs /path/to/your/codebase
```

#### Option B: Python Analysis Tool

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Analyze codebase (generates actionable prompts for humans)
review-codebase analyze /path/to/your/codebase \
  --workflow reviewer_criteria \
  --output analysis.json \
  --prompts-output prompts.md

# Web UI
review-codebase web --port 3000
```

**Note**: The Python tool generates prompts for **human review**, not offline tools. See [CRITICAL_GAP_ANALYSIS.md](CRITICAL_GAP_ANALYSIS.md) for details.

## 📁 System Architecture

### The True Mission: Two-Phase Evolution

This system implements a **self-evolving documentation pipeline**:

**Phase 1 (Go)**: Analyzes codebase → Generates LLM prompt → LLM creates Phase 2 tools
**Phase 2 (Go, LLM-generated)**: Offline tools regenerate docs without LLM

See [PRD.md](PRD.md) for complete architecture.

### Current Implementation Status

This repository contains **two tools** (one complete, one in development):

#### 🐍 Python Analysis Tool (Complete, Different Purpose)

Generates **actionable prompts for human review** (not the main mission):

```
src/codebase_reviewer/
├── analyzers/                  # Core analysis engines
│   ├── documentation.py        # Doc analysis & claim extraction
│   ├── code.py                 # Code structure analysis
│   ├── validation.py           # Cross-validation engine
│   ├── language_detector.py    # Language/framework detection
│   ├── dependency_parser.py    # Dependency analysis
│   └── quality_checker.py      # Code quality assessment
├── prompts/                    # Prompt generation system
│   ├── workflows/              # Workflow definitions (YAML)
│   │   ├── default.yml         # 5-phase documentation review
│   │   └── reviewer_criteria.yml # Principal engineer review
│   ├── templates/              # Prompt templates
│   └── workflow_loader.py      # Workflow execution engine
├── cli.py                      # Command-line interface
├── web.py                      # Web UI (Flask)
├── orchestrator.py             # Analysis coordinator
├── simulation.py               # Prompt testing/tuning
└── models.py                   # Data models
```

**Key Features:**
- ✅ Multi-phase analysis (Documentation → Code → Validation → Prompts)
- ✅ Customizable workflows (default, reviewer_criteria, custom)
- ✅ Web UI for interactive analysis
- ✅ Simulation mode for prompt tuning
- ✅ Export to JSON/Markdown
- ✅ Production-ready Python package

#### 🔧 Go Phase 1 Tool (Core Mission, Partially Complete)

The **main mission tool** for generating Phase 2 offline tools:

```text
cmd/generate-docs/              # Phase 1 CLI tool
internal/
├── scanner/                    # Repository discovery
└── prompt/                     # Prompt generation
pkg/
├── logger/                     # Logging utilities
└── learnings/                  # Evolution system (design only)
prompts/
├── templates/                  # LLM prompt templates (YAML)
└── schemas/                    # Data schemas
```

**Status**: ✅ **Phase 1 Complete** | ❌ **Phase 2 Not Implemented**

**What Works**:

- ✅ Analyzes codebase structure
- ✅ Generates Phase 1 LLM prompt
- ✅ Prompt saved to `/tmp/codebase-reviewer/{name}/phase1-llm-prompt.md`

**What's Missing** (The Critical 80%):

- ❌ LLM integration (manual copy/paste required)
- ❌ Phase 2 tool generation (LLM response → compiled tools)
- ❌ Offline tool execution framework
- ❌ Self-evolution loop implementation
- ❌ Validation framework (LLM vs Tool comparison)

See [CRITICAL_GAP_ANALYSIS.md](CRITICAL_GAP_ANALYSIS.md) for complete details.

## 🔄 How It Works

### The Mission Workflow (In Development)

See [PRD.md](PRD.md) for the complete two-phase evolution system.

**Target Workflow**:

1. **Phase 1**: Analyze codebase → Generate LLM prompt → LLM creates Phase 2 tools
2. **Phase 2**: Offline tools regenerate docs without LLM (infinite, free)
3. **Evolution**: Tools detect obsolescence → Regenerate improved Gen 2 tools

**Current Status**: Phase 1 works manually, automation in progress.

### Python Analyzer (Current, Different Purpose)

The Python tool generates **actionable prompts for humans** (not offline tools):

#### Phase 0: Documentation Analysis
1. Discover all documentation files (README, docs/, etc.)
2. Extract testable claims from documentation
3. Identify claimed architecture, setup instructions, APIs
4. Calculate documentation completeness score

#### Phase 1-2: Code Analysis
1. Detect languages and frameworks
2. Analyze directory structure and dependencies
3. Run quality checks (code smells, anti-patterns)
4. Map critical modules and entry points

#### Phase 3: Validation (Cross-Check)
1. Compare documentation claims vs actual code
2. Detect documentation drift (outdated/incorrect docs)
3. Find undocumented features
4. Assess drift severity

#### Phase 4: Prompt Generation
1. Load workflow definition (default or custom)
2. Generate AI prompts based on analysis results
3. Include context from all previous phases
4. Export to JSON/Markdown for LLM consumption

### Workflow System

Choose from pre-built workflows or create custom ones:

**Default Workflow**: 5-phase documentation-first review
- Phase 0: Documentation Review
- Phase 1: Architecture Analysis
- Phase 2: Implementation Deep-Dive
- Phase 3: Development Workflow
- Phase 4: Interactive Remediation

**Reviewer Criteria Workflow**: Principal engineer-level review
- Reconnaissance (architecture, dependencies, static analysis)
- Hygiene Checks (tests, CI, comments)
- Safety & Security (anti-patterns, error handling)
- Architecture Insights (call graphs, hotspots, duplication)
- Coverage & Modeling (integrations, boundaries, complexity)
- Strategy (design docs, instrumentation, tech debt, mentoring)

## 💡 Key Features

### 1. Comprehensive Analysis
- **Documentation Analysis**: Extracts and validates claims from all docs
- **Code Structure**: Detects languages, frameworks, dependencies
- **Quality Assessment**: Identifies code smells, anti-patterns, issues
- **Cross-Validation**: Compares docs vs code to find drift

### 2. Customizable Workflows
- **YAML-Based**: Define custom review workflows
- **Pre-Built**: Default and reviewer_criteria workflows included
- **Extensible**: Add custom prompts and analysis steps
- **Template System**: Reusable prompt templates

### 3. Multiple Interfaces
- **CLI**: Full-featured command-line interface
- **Web UI**: Interactive browser-based interface
- **Programmatic**: Use as Python library

### 4. Simulation & Testing
- **Prompt Tuning**: Systematic workflow for improving prompts
- **Test Data Generation**: Create realistic test cases
- **Quality Evaluation**: Score outputs against rubrics
- **Improvement Recommendations**: Get specific prompt enhancements
- **Mock Responses**: Simulate LLM responses for testing
- **Iterative Improvement**: Refine prompts based on results

### 5. Export & Integration
- **JSON Export**: Machine-readable analysis results
- **Markdown Export**: Human-readable prompts
- **Flexible Output**: Save to files or stdout

## 🛠️ Commands

### Python CLI Commands

```bash
# Analyze a codebase
review-codebase analyze /path/to/repo

# Use specific workflow
review-codebase analyze /path/to/repo --workflow reviewer_criteria

# Save outputs
review-codebase analyze /path/to/repo -o analysis.json -p prompts.md

# Show only specific phase prompts
review-codebase prompts /path/to/repo --phase 0

# Run simulation (test prompts)
review-codebase simulate /path/to/repo --workflow reviewer_criteria

# Start web UI
review-codebase web --port 3000

# Prompt tuning workflow
review-codebase tune init --project my_project --num-tests 5
review-codebase tune evaluate ./prompt_tuning_results/tuning_my_project_*

# Get help
review-codebase --help
review-codebase analyze --help
review-codebase tune --help
```

### Go CLI Commands (Legacy Tool)

```bash
# Build the Go tool
make build

# Run with verbose output
./bin/generate-docs -v /path/to/codebase

# Regenerate (scorch mode)
./bin/generate-docs --scorch /path/to/codebase

# Review existing analysis
./bin/generate-docs --review /path/to/codebase

# Clean
make clean
```

## 🎓 Example Workflows

### Example 1: Quick Analysis

```bash
# Analyze a repository
review-codebase analyze /Users/matt/GitHub/CallBox/Cari

# Output shows:
# - Documentation files found
# - Languages and frameworks detected
# - Quality issues identified
# - Drift between docs and code
# - Generated prompts count

# Results saved to:
# - prompts.md (AI prompts for review)
# - prompts.json (machine-readable format)
```

### Example 2: Principal Engineer Review

```bash
# Use the comprehensive review workflow
review-codebase analyze /Users/matt/GitHub/CallBox/Cari \
  --workflow reviewer_criteria \
  -o cari_analysis.json \
  -p cari_prompts.md

# This generates prompts for:
# 1. High-Level Reconnaissance
# 2. Baseline Hygiene Checks
# 3. Core Safety and Security
# 4. Architecture Insights
# 5. Coverage & Modeling
# 6. Principal Engineer Strategy
```

### Example 3: Simulation & Tuning

```bash
# Test prompts before using with real LLM
review-codebase simulate /Users/matt/GitHub/CallBox/Cari \
  --workflow reviewer_criteria \
  --output-dir ./simulation_results

# Review simulation results
cat ./simulation_results/simulation_*.md

# Iterate on prompts in src/codebase_reviewer/prompts/templates/
# Re-run simulation to verify improvements
```

### Example 4: Web UI

```bash
# Start the web interface
./start-web.sh

# Or manually:
review-codebase web --port 3000

# Then:
# 1. Open http://localhost:3000
# 2. Enter repository path: /Users/matt/GitHub/CallBox/Cari
# 3. Click "Analyze"
# 4. View results and download prompts
```

## 🔧 Requirements

### Python Tool (Primary)
- Python 3.9+
- pip or pip3
- Git (for repository analysis)

### Go Tool (Optional/Legacy)
- Go 1.21+
- Git

## 📦 Installation

### Python Tool Setup

```bash
# Option 1: Automated setup (recommended)
./setup.sh

# Option 2: Manual setup
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

# Verify installation
review-codebase --help
```

### Go Tool Setup (Optional)

```bash
# Build the Go tool
make build

# Verify
./bin/generate-docs -h
```

## 🎯 Target Repository

This tool is configured to analyze:

**Primary Target**: `/Users/matt/GitHub/CallBox/Cari/`

```bash
# Quick analysis
review-codebase analyze /Users/matt/GitHub/CallBox/Cari

# Comprehensive review
review-codebase analyze /Users/matt/GitHub/CallBox/Cari \
  --workflow reviewer_criteria \
  -o cari_analysis.json \
  -p cari_review_prompts.md

# Simulation mode
review-codebase simulate /Users/matt/GitHub/CallBox/Cari \
  --workflow reviewer_criteria
```

## 📚 Documentation

### Getting Started
- **`README.md`** (this file) - Overview and quick start
- **`QUICK-START.md`** - 5-minute setup guide
- **`START-HERE.md`** - Guided introduction

### Python Tool Documentation
- **`setup.py`** - Package configuration
- **`src/codebase_reviewer/`** - Source code with inline docs
- **`tests/`** - Test suite with examples

### Workflow Documentation
- **`src/codebase_reviewer/prompts/workflows/`** - Workflow definitions
- **`src/codebase_reviewer/prompts/templates/`** - Prompt templates
- **`docs/WORKFLOW_INTEGRATION_PROPOSAL.md`** - Workflow system design

### Prompt Tuning Documentation
- **`docs/PROMPT_TUNING_GUIDE.md`** - Complete tuning workflow guide
- **`archive/PROMPT_TUNING_*.md`** - Original methodology and design specs
- **`src/codebase_reviewer/tuning/`** - Tuning system source code

### Go Tool Documentation (Legacy)
- **`docs/EVOLUTION-SYSTEM.md`** - Evolution system guide
- **`docs/EVOLUTION-SUMMARY.md`** - Quick reference
- **`docs/NEXT-STEPS.md`** - Usage instructions
- **`prompts/schemas/learnings-schema.yaml`** - Learnings schema

## 🤝 Contributing

This tool is designed to be:

- **Generic** - Works with any codebase
- **Extensible** - Easy to add new analyzers and workflows
- **Customizable** - YAML-based configuration
- **Well-Tested** - Comprehensive test suite

To add a custom workflow:

1. Create a new YAML file in `src/codebase_reviewer/prompts/workflows/`
2. Define sections and prompts
3. Reference existing templates or create custom prompts
4. Test with simulation mode

## 📄 License

See LICENSE file for details.

## 🆘 Support

### For Python Tool Issues
1. Check test suite: `pytest tests/`
2. Review analyzer output with `--quiet` flag removed
3. Check simulation results for prompt quality
4. Review workflow YAML for configuration issues

### For Go Tool Issues
1. Check `docs/EVOLUTION-SYSTEM.md` for detailed guide
2. Review `docs/NEXT-STEPS.md` for usage instructions
3. Inspect YAML prompts for debugging

### Common Issues
- **Import errors**: Run `./setup.sh` or `pip install -e .`
- **Port conflicts**: Use `--port` flag to specify different port
- **Analysis errors**: Ensure repository path is correct and accessible

---

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Last Updated**: 2025-11-24
**Primary Tool**: Python-based comprehensive analyzer
**Target Repository**: /Users/matt/GitHub/CallBox/Cari/
