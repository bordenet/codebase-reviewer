# Claude Code Guidelines for This Repository

This document contains project-specific guidelines and lessons learned for Claude Code when working in this repository.

## Project Overview

**Codebase Reviewer** is a Python-based tool for analyzing codebases and generating AI review prompts.

- **Language**: Python 3.9+
- **Framework**: Flask (web interface)
- **Package Manager**: pip + virtualenv
- **Code Quality**: pylint, mypy, black, pytest
- **Installation**: Development mode (`pip install -e .`)

## User Environment

- **All hardware is Apple Silicon** (ARM64 architecture)
- Homebrew paths: `/opt/homebrew/` (not `/usr/local/`)
- When suggesting paths, always use Apple Silicon defaults first
- **macOS uses BSD tools, not GNU** - always test awk/sed/grep syntax in bash scripts
  - BSD awk does NOT support `match()` with array capture
  - Use `grep | sed` pipelines instead of complex awk
  - Test all regex/text processing commands before committing

## Quality Standards for Code Delivery

### ALWAYS Do Before Claiming "Done":

1. **Lint the code**
   - Run `pylint src/codebase_reviewer` (target: 9.5+/10)
   - Run `mypy src/codebase_reviewer` for type checking
   - Run `black src/codebase_reviewer tests/` for formatting
   - Fix ALL warnings that aren't explicitly false positives
   - Don't wait to be asked

2. **Test the code**
   - **ALWAYS run `pytest tests/ -v` before committing**
   - Ensure all existing tests pass
   - Add tests for new functionality
   - Don't commit broken code
   - Test edge cases and error conditions
   - If you can't test on the target platform, explicitly document this

3. **Handle edge cases**
   - Filenames with spaces/special characters
   - Empty inputs / None values
   - Missing files or directories
   - Invalid repository paths
   - Malformed documentation files

4. **Error handling**
   - Use proper exception handling (try/except)
   - Provide actionable error messages
   - Log errors comprehensively
   - Don't silently swallow exceptions
   - Return appropriate status codes

5. **Input validation**
   - Validate file paths exist before processing
   - Check for required fields in data structures
   - Sanitize user input (especially for web interface)
   - Use type hints for function parameters

### Python-Specific Standards:

1. **Type hints**: Use them consistently
   ```python
   # Good
   def analyze(repo_path: str) -> RepositoryAnalysis:
       ...
   ```

2. **Docstrings**: Use for all public functions/classes
   ```python
   """Analyze a codebase and generate review prompts.

   Args:
       repo_path: Absolute path to repository

   Returns:
       RepositoryAnalysis object with findings
   """
   ```

3. **Imports**: Organize properly
   - Standard library first
   - Third-party packages second
   - Local imports last
   - Remove unused imports

4. **Code formatting**: Follow black style
   - Max line length: 120 (per project convention)
   - Use double quotes for strings
   - 4 spaces for indentation

### Before Creating a PR:

1. **All tests pass**: `pytest tests/ -v`
2. **Code is formatted**: `black src/codebase_reviewer tests/`
3. **Linting passes**: `pylint src/codebase_reviewer` (9.5+/10)
4. **Type checking passes**: `mypy src/codebase_reviewer`
5. **Pre-commit hooks pass** (automatically enforced)
6. Edge cases considered and documented
7. Error handling tested where possible
8. Code follows project conventions
9. Commit messages are descriptive

**Don't make the user ask for basic quality practices.**

### Creating Pull Requests:

**ALWAYS provide a PR URL when changes are ready for review.**

When in Web mode (where `gh` CLI is unavailable):
1. Provide the direct GitHub compare URL for PR creation
2. Format: `https://github.com/OWNER/REPO/compare/BASE...BRANCH?expand=1`
3. Include pre-written title and description for user to paste
4. Don't leave the user hunting for how to create the PR

Example:
```
https://github.com/matt/codebase-reviewer/compare/main...feature-branch?expand=1
```

## Shell Script Standards

**CRITICAL**: This repository MUST be friction-free for adopters. If setup is painful, the repo is worthless.

### Philosophy:

We ALWAYS rely on high-quality shell scripts to:
1. **Install dependencies** (`scripts/setup-*.sh`)
2. **Run the application** (`start-web.sh`, `setup.sh`)

### Shell Script Requirements:

Every shell script MUST:

1. **Be self-contained and robust**
   - Kill abandoned sessions tying up ports
   - Set up virtual environments automatically
   - Install dependencies without user intervention
   - Handle errors gracefully with clear messages
   - Provide colored, informative output

2. **Follow our style guide**
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail  # Fail fast, catch errors

   # Colors for output
   RED='\033[0;31m'
   GREEN='\033[0;32m'
   YELLOW='\033[1;33m'
   BLUE='\033[0;34m'
   NC='\033[0m' # No Color

   log_info() { echo -e "${BLUE}ℹ${NC} $*"; }
   log_success() { echo -e "${GREEN}✓${NC} $*"; }
   log_warning() { echo -e "${YELLOW}⚠${NC} $*"; }
   log_error() { echo -e "${RED}✗${NC} $*" >&2; }
   ```

3. **Handle port conflicts intelligently**
   - Check if port is in use
   - Kill stale processes (with user awareness)
   - Find alternative ports automatically
   - Use sensible defaults (avoid system ports like 5000 on macOS)

4. **Provide excellent UX**
   - Clear progress indicators
   - Helpful error messages
   - Show URLs where services are running
   - Explain what's happening at each step

5. **Be macOS-aware**
   - Use BSD-compatible commands (not GNU)
   - Handle Apple Silicon paths (`/opt/homebrew/`)
   - Avoid ports used by macOS services (5000 = AirPlay)
   - Test with `lsof` for port checking

### Example: Running the Web App

The `start-web.sh` script MUST:
1. ✅ Set up the virtual environment
2. ✅ Kill old abandoned sessions on the target port
3. ✅ Build/install the app
4. ✅ Start the server on an available port
5. ✅ Open the web browser automatically
6. ✅ Provide clear instructions for stopping

**One command to rule them all:**
```bash
./start-web.sh
```

No manual venv activation. No port conflicts. No confusion. Just works.

## Pre-Commit Hooks

This repository uses pre-commit hooks to enforce quality standards. All commits must pass:

1. **Black formatting** - Auto-formats code
2. **PyLint** - Linting checks (9.5+/10 required)
3. **Pytest** - All tests must pass
4. **MyPy** - Type checking

The hooks run automatically on `git commit`. If they fail, the commit is blocked.
