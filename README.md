# Codebase Reviewer - AI-Powered Code Analysis & Review

A comprehensive, production-ready tool for analyzing codebases with AI-powered insights. Combines automated code analysis, documentation validation, and customizable review workflows.

## 🎯 What This Tool Does

**Analyzes**: Scans codebases to understand structure, languages, frameworks, and dependencies
**Validates**: Cross-checks documentation claims against actual code implementation
**Reviews**: Generates AI prompts for comprehensive code review using customizable workflows
**Simulates**: Tests and tunes prompts before using them with real LLMs
**Visualizes**: Provides web UI for interactive analysis and prompt generation

## 🚀 Quick Start

### 1. Setup (One-time)
```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Analyze a Codebase
```bash
# Using the CLI
review-codebase analyze /path/to/your/codebase

# Or with a specific workflow
review-codebase analyze /path/to/your/codebase --workflow reviewer_criteria

# Save results
review-codebase analyze /path/to/your/codebase -o analysis.json -p prompts.md
```

### 3. Use the Web Interface
```bash
# Start the web UI
./start-web.sh

# Or manually:
review-codebase web --port 3000
```

Then open http://localhost:3000 in your browser.

## 📁 Architecture

This repository contains **two complementary tools**:

### 🐍 Python-Based Comprehensive Analyzer (Primary Tool)

The main production tool with full analysis capabilities:

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

### 🔧 Go-Based Phase 1 Tool (Legacy/Alternative)

Original two-phase evolution system:

```
cmd/generate-docs/              # Go CLI tool
internal/
├── scanner/                    # Repository discovery
└── prompt/                     # Prompt generation
pkg/
├── logger/                     # Logging utilities
└── learnings/                  # Evolution system
prompts/
├── templates/                  # LLM prompt templates (YAML)
└── schemas/                    # Data schemas
```

**Use Cases:**
- Alternative prompt generation approach
- Self-evolving documentation system
- LLM-assisted tool generation

Both tools share the same `prompts/` directory for consistency.

## 🔄 How It Works

### Python Analyzer Workflow (Recommended)

The Python-based analyzer follows a **4-phase analysis pipeline**:

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
