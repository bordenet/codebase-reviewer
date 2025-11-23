# Codebase Reviewer

[![CI](https://github.com/bordenet/codebase-reviewer/actions/workflows/ci.yml/badge.svg)](https://github.com/bordenet/codebase-reviewer/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/bordenet/codebase-reviewer/branch/main/graph/badge.svg)](https://codecov.io/gh/bordenet/codebase-reviewer)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Linting: pylint](https://img.shields.io/badge/linting-pylint%209.5+-yellowgreen)](https://github.com/PyCQA/pylint)
[![Type checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue)](https://github.com/python/mypy)
[![Testing: pytest](https://img.shields.io/badge/testing-pytest-green)](https://github.com/pytest-dev/pytest)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/bordenet/codebase-reviewer/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/bordenet/codebase-reviewer.svg)](https://github.com/bordenet/codebase-reviewer/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/bordenet/codebase-reviewer.svg)](https://github.com/bordenet/codebase-reviewer/pulls)

Python tool for analyzing codebases and generating AI review prompts.

## Key Features

### Documentation-First Analysis
- Analyzes project documentation (README, architecture docs, setup guides) **before** code
- Extracts testable claims about architecture, setup, and features
- Validates documentation against actual code implementation
- Identifies drift, gaps, and outdated information

### Multi-Phase Prompt Generation
Generates AI prompts in 5 progressive phases:

1. **Phase 0: Documentation Review** - Extract claims from docs
2. **Phase 1: Architecture Analysis** - Validate architecture against code
3. **Phase 2: Implementation Deep-Dive** - Code quality, patterns, observability
4. **Phase 3: Development Workflow** - Setup validation, testing strategy
5. **Phase 4: Interactive Remediation** - Prioritized action planning

### Comprehensive Analysis
- Programming language and framework detection
- Dependency analysis and health checks
- Code quality assessment (TODOs, security issues, technical debt)
- Architecture pattern detection and validation
- Setup instruction validation

## Quick Start

### Web UI (Recommended)

**One command to start everything:**

```bash
./start-web.sh
```

This script:
- ✅ Sets up virtual environment automatically
- ✅ Installs all dependencies
- ✅ Kills stale processes on the port
- ✅ Finds an available port (defaults to 3000)
- ✅ Opens your browser automatically
- ✅ Just works - zero friction!

### CLI Analysis

Use the automated setup script:

```bash
# Show help
./setup.sh --help

# Analyze a repository via CLI
./setup.sh /path/to/repository

# Force rebuild of environment
./setup.sh --force-setup
```

The script:
- Detects Python 3.9+
- Creates virtual environment in `.venv/`
- Installs dependencies
- Runs the tool

## Manual Installation (For Development)

If you're developing or want manual control:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks (enforces quality checks on commits)
pre-commit install
```

### Pre-Commit Hooks

Pre-commit hooks enforce code quality:

- Black - Code formatting (auto-fixes)
- isort - Import sorting (auto-fixes)
- PyLint - Linting (requires 9.5+/10)
- MyPy - Type checking
- Pytest - All tests must pass

## Usage

### Command-Line Interface

#### Basic Analysis
```bash
# Using the automated script (recommended)
./setup.sh /path/to/repo

# Or manually (if venv is activated)
python -m codebase_reviewer analyze /path/to/repo

# Analyze with output files
python -m codebase_reviewer analyze /path/to/repo \
    --output analysis.json \
    --prompts-output prompts.md

# Quiet mode (minimal output)
python -m codebase_reviewer analyze /path/to/repo --quiet
```

#### View Prompts
```bash
# Display all generated prompts
python -m codebase_reviewer prompts /path/to/repo

# Display specific phase only
python -m codebase_reviewer prompts /path/to/repo --phase 0
```

### Web Interface

#### Start Web Server

**Recommended: Use the startup script**

```bash
./start-web.sh
```

This automatically:
- Sets up dependencies
- Kills stale processes
- Finds an available port
- Opens your browser

**Manual start (if needed):**

```bash
# Start web server (default port 3000)
python -m codebase_reviewer web

# Specify custom host and port
python -m codebase_reviewer web --host 0.0.0.0 --port 8080

# Run in debug mode
python -m codebase_reviewer web --debug
```

Then open your browser to `http://127.0.0.1:3000` (or your specified port)

Features:
- Real-time analysis progress
- Visual metrics dashboard
- Download prompts (Markdown/JSON)
- Export analysis results

### Example Output

```
Codebase Reviewer - Analyzing: /home/user/my-project

  Phase 0: Analyzing documentation...
  Found 8 documentation files
  Extracted 12 testable claims
  Phase 1-2: Analyzing code structure...
  Detected 2 languages
  Detected 3 frameworks
  Found 45 quality issues
  Validation: Comparing documentation vs code...
  Found 3 documentation drift issues
  Drift severity: medium
  Generating AI prompts...
  Generated 11 AI prompts across 5 phases
  Analysis complete in 2.34 seconds

============================================================
ANALYSIS SUMMARY
============================================================

Documentation:
  Files found: 8
  Completeness: 75.0%
  Claims extracted: 12
  Architecture: microservices

Code Structure:
  Python: 85.3%
  Shell: 14.7%
  Frameworks: Flask, Docker
  Quality issues: 45

Validation:
  Drift severity: MEDIUM
  Drift issues: 3
  Undocumented features: 2

Generated Prompts:
  Total prompts: 11
  Phase 0 (Documentation Review): 3
  Phase 1 (Architecture Analysis): 2
  Phase 2 (Implementation Deep-Dive): 2
  Phase 3 (Development Workflow): 2
  Phase 4 (Interactive Remediation): 2

Completed in 2.34 seconds
```

## Architecture

### Core Components

```
┌─────────────────────────────────────────┐
│       Analysis Orchestrator              │
│  (Coordinates analysis pipeline)         │
└─────────────────────────────────────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
┌─────▼─────┐ ┌───▼────┐ ┌────▼──────┐
│   Docs    │ │  Code  │ │Validation │
│ Analyzer  │ │Analyzer│ │  Engine   │
└───────────┘ └────────┘ └───────────┘
      │            │            │
      └────────────┼────────────┘
                   │
           ┌───────▼────────┐
           │     Prompt     │
           │   Generator    │
           └────────────────┘
```

### Analysis Flow

1. **Documentation Analyzer**: Discovers and analyzes all markdown/documentation files
2. **Code Analyzer**: Analyzes repository structure, languages, frameworks, dependencies
3. **Validation Engine**: Cross-checks documentation claims against code reality
4. **Prompt Generator**: Creates structured AI prompts incorporating findings

## Generated Prompts

Prompts are designed to guide AI assistants (Claude, GPT-4, Gemini) through systematic code review:

### Phase 0: Documentation Review
- README analysis and claims extraction
- Architecture documentation review
- Setup and build documentation assessment

### Phase 1: Architecture Analysis
- Architecture validation against code
- Dependency analysis and health checks

### Phase 2: Implementation Deep-Dive
- Code quality and technical debt assessment
- Observability and operational maturity review

### Phase 3: Development Workflow
- Setup instruction validation
- Testing strategy assessment

### Phase 4: Interactive Remediation
- Issue prioritization and action planning

## Output Formats

### JSON Analysis Results
```json
{
  "repository_path": "/path/to/repo",
  "timestamp": "2025-11-14T10:30:00",
  "documentation": {
    "total_docs": 8,
    "completeness_score": 75.0,
    "claims_count": 12
  },
  "code": {
    "languages": [{"name": "Python", "percentage": 85.3}],
    "frameworks": ["Flask", "Docker"],
    "quality_issues_count": 45
  },
  "validation": {
    "drift_severity": "medium",
    "architecture_drift_count": 2,
    "setup_drift_count": 1
  }
}
```

### Markdown Prompts
```markdown
# AI Code Review Prompts

## Phase 0: Documentation Review

### Prompt 0.1: README Analysis & Claims Extraction

**Objective:** Extract and catalog all claims about project architecture...

**Tasks:**
- Identify the stated project purpose and scope
- List all claimed technologies and frameworks
- Extract documented architecture pattern
...
```

## Use Cases

### 1. New Team Member Onboarding
```bash
# Generate comprehensive onboarding prompts
python -m codebase_reviewer analyze /path/to/repo --prompts-output onboarding.md

# New team member uses prompts with AI assistant (Claude, GPT-4, etc.)
# AI walks through architecture, patterns, setup process
```

### 2. Technical Debt Assessment
```bash
# Analyze codebase for quality issues and drift
python -m codebase_reviewer analyze /path/to/repo --output assessment.json

# Review drift severity and quality issues
# Use Phase 4 prompts to prioritize remediation
```

### 3. Documentation Audit
```bash
# Check documentation completeness and accuracy
python -m codebase_reviewer analyze /path/to/repo

# Review documentation completeness score
# Identify undocumented features and drift
```

## Configuration

Default behavior can be customized by modifying analyzer classes:

- **DocumentationAnalyzer**: Add custom documentation patterns
- **CodeAnalyzer**: Extend language/framework detection
- **ValidationEngine**: Customize validation rules
- **PromptGenerator**: Modify prompt templates

## Development

### Running Tests
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=codebase_reviewer tests/
```

### Linting
```bash
# Run pylint
pylint src/codebase_reviewer

# Run mypy
mypy src/codebase_reviewer

# Format with black
black src/codebase_reviewer
```

## Project Structure

```
codebase-reviewer/
├── src/
│   └── codebase_reviewer/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py                 # Command-line interface
│       ├── web.py                 # Flask web interface
│       ├── models.py              # Data models
│       ├── orchestrator.py        # Analysis orchestrator
│       ├── prompt_generator.py    # Prompt generation
│       ├── analyzers/             # Analysis modules
│       │   ├── __init__.py
│       │   ├── code.py            # Code analyzer
│       │   ├── constants.py       # Constants
│       │   ├── documentation.py   # Documentation analyzer
│       │   ├── parsing_utils.py   # Parsing utilities
│       │   └── validation.py      # Validation engine
│       └── prompts/               # Prompt templates
│           ├── __init__.py
│           ├── export.py          # Export utilities
│           ├── phase0.py          # Phase 0 prompts
│           ├── phase1.py          # Phase 1 prompts
│           ├── phase2.py          # Phase 2 prompts
│           ├── phase3.py          # Phase 3 prompts
│           └── phase4.py          # Phase 4 prompts
├── tests/                         # Test suite
│   └── test_basic.py
├── docs/                          # Documentation
│   ├── PRD.md                     # Product requirements
│   ├── DESIGN.md                  # Technical design
│   └── CLAUDE.md                  # AI assistant guidelines
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
├── requirements.txt               # Dependencies
├── setup.py                       # Package setup
├── .pre-commit-config.yaml        # Pre-commit hooks
├── .coveragerc                    # Coverage configuration
└── README.md                      # This file
```

## Limitations

- Static analysis only (no code execution)
- Supports Python, JavaScript/TypeScript, Java, C#, Go, Ruby, Shell
- Large repositories (>1GB) may be slow

## Contributing

To extend this tool:

1. Add language support: Extend `LANGUAGE_EXTENSIONS` in `code.py`
2. Add framework detection: Update `FRAMEWORK_PATTERNS` in `code.py`
3. Add documentation patterns: Modify `DOCUMENTATION_PATTERNS` in `documentation.py`
4. Custom validation rules: Extend `ValidationEngine` class
5. Custom prompts: Modify `PromptGenerator` methods

## License

MIT License - see LICENSE file


