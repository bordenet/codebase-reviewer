# Simulation Report: reviewer_criteria

**Repository:** .
**Timestamp:** 2025-11-21 06:59:36
**Duration:** 1.82 seconds
**Prompts Tested:** 19

---

## 1. README Analysis & Claims Extraction

**Prompt ID:** `0.1`
**Phase:** 0

### Prompt Text

```
# README Analysis & Claims Extraction

**Objective:** Extract and catalog all claims about project architecture, features, and setup from the README

**Tasks:**
- Identify the stated project purpose and scope
- List all claimed technologies and frameworks
- Extract documented architecture pattern (if any)
- Note all setup/installation claims
- Catalog documented features and capabilities
- Identify any architectural diagrams or descriptions
- Note what version of languages/frameworks are claimed

**Deliverable:** Structured list of testable claims with source locations for validation against code

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'readme_content': '# Codebase Reviewer\n\n[![CI](https://github.com/bordenet/codebase-reviewer/actions/workflows/ci.yml/badge.svg)](https://github.com/bordenet/codebase-reviewer/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/bordenet/codebase-reviewer/branch/main/graph/badge.svg)](https://codecov.io/gh/bordenet/codebase-reviewer)\n[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n[![Linting: pylint](https://img.shields.io/badge/linting-pylint%209.5+-yellowgreen)](https://github.com/PyCQA/pylint)\n[![Type checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue)](https://github.com/python/mypy)\n[![Testing: pytest](https://img.shields.io/badge/testing-pytest-green)](https://github.com/pytest-dev/pytest)\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/bordenet/codebase-reviewer/graphs/commit-activity)\n[![GitHub issues](https://img.shields.io/github/issues/bordenet/codebase-reviewer.svg)](https://github.com/bordenet/codebase-reviewer/issues)\n[![GitHub pull requests](https://img.shields.io/github/issues-pr/bordenet/codebase-reviewer.svg)](https://github.com/bordenet/codebase-reviewer/pulls)\n\nPython tool for analyzing codebases and generating AI review prompts.\n\n## Key Features\n\n### Documentation-First Analysis\n- Analyzes project documentation (README, architecture docs, setup guides) **before** code\n- Extracts testable claims about architecture, setup, and features\n- Validates documentation against actual code implementation\n- Identifies drift, gaps, and outdated information\n\n### Multi-Phase Prompt Generation\nGenerates AI prompts in 5 progressive phases:\n\n1. **Phase 0: Documentation Review** - Extract claims from docs\n2. **Phase 1: Architecture Analysis** - Validate architecture against code\n3. **Phase 2: Implementation Deep-Dive** - Code quality, patterns, observability\n4. **Phase 3: Development Workflow** - Setup validation, testing strategy\n5. **Phase 4: Interactive Remediation** - Prioritized action planning\n\n### Comprehensive Analysis\n- Programming language and framework detection\n- Dependency analysis and health checks\n- Code quality assessment (TODOs, security issues, technical debt)\n- Architecture pattern detection and validation\n- Setup instruction validation\n\n## Quick Start\n\n### Web UI (Recommended)\n\n**One command to start everything:**\n\n```bash\n./start-web.sh\n```\n\nThis script:\n- ✅ Sets up virtual environment automatically\n- ✅ Installs all dependencies\n- ✅ Kills stale processes on the port\n- ✅ Finds an available port (defaults to 3000)\n- ✅ Opens your browser automatically\n- ✅ Just works - zero friction!\n\n### CLI Analysis\n\nUse the automated setup script:\n\n```bash\n# Show help\n./setup.sh --help\n\n# Analyze a repository via CLI\n./setup.sh /path/to/repository\n\n# Force rebuild of environment\n./setup.sh --force-setup\n```\n\nThe script:\n- Detects Python 3.9+\n- Creates virtual environment in `.venv/`\n- Installs dependencies\n- Runs the tool\n\n## Manual Installation (For Development)\n\nIf you\'re developing or want manual control:\n\n```bash\n# Create virtual environment\npython3 -m venv venv\nsource venv/bin/activate  # On Windows: venv\\Scripts\\activate\n\n# Install dependencies\npip install -r requirements.txt\n\n# Install in development mode with dev dependencies\npip install -e ".[dev]"\n\n# Set up pre-commit hooks (enforces quality checks on commits)\npre-commit install\n```\n\n### Pre-Commit Hooks\n\nPre-commit hooks enforce code quality:\n\n- Black - Code formatting (auto-fixes)\n- isort - Import sorting (auto-fixes)\n- PyLint - Linting (requires 9.5+/10)\n- MyPy - Type checking\n- Pytest - All tests must pass\n\n## Usage\n\n### Command-Line Interface\n\n#### Basic Analysis\n```bash\n# Using the automated script (recommended)\n./setup.sh /path/to/repo\n\n# Or manually (if venv is activated)\npython -m codebase_reviewer analyze /path/to/repo\n\n# Analyze with output files\npython -m codebase_reviewer analyze /path/to/repo \\\n    --output analysis.json \\\n    --prompts-output prompts.md\n\n# Quiet mode (minimal output)\npython -m codebase_reviewer analyze /path/to/repo --quiet\n```\n\n#### View Prompts\n```bash\n# Display all generated prompts\npython -m codebase_reviewer prompts /path/to/repo\n\n# Display specific phase only\npython -m codebase_reviewer prompts /path/to/repo --phase 0\n```\n\n### Web Interface\n\n#### Start Web Server\n\n**Recommended: Use the startup script**\n\n```bash\n./start-web.sh\n```\n\nThis automatically:\n- Sets up dependencies\n- Kills stale processes\n- Finds an available port\n- Opens your browser\n\n**Manual start (if needed):**\n\n```bash\n# Start web server (default port 3000)\npython -m codebase_reviewer', 'readme_path': 'README.md', 'total_docs_found': 2}
```

### Simulated Response

# Analysis Response: README Analysis & Claims Extraction

## Summary
This is a simulated response for prompt '0.1'.
The prompt asks the LLM to analyze: Extract and catalog all claims about project architecture, features, and setup from the README

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 2. Validate Documented Architecture Against Actual Code

**Prompt ID:** `1.1`
**Phase:** 1

### Prompt Text

```
# Validate Documented Architecture Against Actual Code

**Objective:** Verify if actual code structure matches documented architecture claims

**Tasks:**
- Compare claimed architectural pattern vs actual implementation
- Verify documented modules/layers exist in code
- Check if technology stack matches documentation
- Identify undocumented components or services
- Flag any significant documentation inaccuracies
- Assess overall architecture quality and appropriateness

**Deliverable:** Architecture validation report with discrepancies highlighted and recommendations

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'claimed_architecture': {'pattern': 'microservices', 'layers': ['service', 'repository'], 'components': ['Core', 'DocumentationAnalyzer', 'CodeAnalyzer', 'ValidationEngine', 'PromptGenerator']}, 'actual_structure': {'languages': [{'name': 'Python', 'percentage': 27.48}, {'name': 'Shell', 'percentage': 3.32}], 'frameworks': ['Flask', 'Django'], 'entry_points': []}, 'validation_results': [{'status': 'valid', 'evidence': "Detected frameworks: ['Flask', 'Django']", 'recommendation': 'Architecture pattern appears consistent'}, {'status': 'partial', 'evidence': 'Found 0/5 claimed components', 'recommendation': 'Review documented component list for accuracy'}]}
```

### Simulated Response

# Analysis Response: Validate Documented Architecture Against Actual Code

## Summary
This is a simulated response for prompt '1.1'.
The prompt asks the LLM to analyze: Verify if actual code structure matches documented architecture claims

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 3. Run static analysis/lint tools

**Prompt ID:** `static_analysis_summary`
**Phase:** 0

### Prompt Text

```
# Run static analysis/lint tools

**Objective:** Generate a summary report identifying major code quality issues, anti-patterns, and code smells

**Tasks:**

**Deliverable:** 

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

Generate a summary report identifying major code quality issues,
anti-patterns, and code smells from static analysis results.

Focus on:
- High-severity issues that impact maintainability
- Common anti-patterns in the detected language/framework
- Code smells that indicate deeper architectural problems
- Patterns that violate best practices

Deliverable: Prioritized list of quality issues with severity ratings

```

### Simulated Response

# Analysis Response: Run static analysis/lint tools

## Summary
This is a simulated response for prompt 'static_analysis_summary'.
The prompt asks the LLM to analyze: Generate a summary report identifying major code quality issues, anti-patterns, and code smells

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 4. Validate Setup and Build Instructions

**Prompt ID:** `3.1`
**Phase:** 3

### Prompt Text

```
# Validate Setup and Build Instructions

**Objective:** Verify documented setup instructions are accurate and complete

**Tasks:**
- Trace documented setup steps to actual configuration files
- Identify missing prerequisites not documented
- Flag outdated version requirements
- Note environment variables used but not documented
- Identify undocumented build steps or scripts
- Assess overall setup documentation quality

**Deliverable:** Setup documentation accuracy report with specific corrections needed

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'documented_setup': {'prerequisites': [], 'build_steps': [], 'env_vars': []}, 'validation_results': [], 'undocumented_features': ['Framework: Django']}
```

### Simulated Response

# Analysis Response: Validate Setup and Build Instructions

## Summary
This is a simulated response for prompt '3.1'.
The prompt asks the LLM to analyze: Verify documented setup instructions are accurate and complete

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 5. Testing Strategy and Coverage Review

**Prompt ID:** `3.2`
**Phase:** 3

### Prompt Text

```
# Testing Strategy and Coverage Review

**Objective:** Assess testing practices, coverage, and quality

**Tasks:**
- Identify test types present (unit, integration, e2e)
- Evaluate test organization and naming conventions
- Assess test coverage (estimate based on test file count)
- Identify testing framework and tools used
- Evaluate test quality and maintainability
- Identify gaps in test coverage

**Deliverable:** Testing assessment with recommendations for improvement

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'repository_path': '.'}
```

### Simulated Response

# Analysis Response: Testing Strategy and Coverage Review

## Summary
This is a simulated response for prompt '3.2'.
The prompt asks the LLM to analyze: Assess testing practices, coverage, and quality

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 6. Dependency Analysis and Health Check

**Prompt ID:** `1.2`
**Phase:** 1

### Prompt Text

```
# Dependency Analysis and Health Check

**Objective:** Analyze project dependencies for health, security, and documentation accuracy

**Tasks:**
- Review all external dependencies and their purposes
- Identify any outdated or deprecated dependencies
- Check for potential security concerns
- Verify dependencies match documented prerequisites
- Identify missing dependency documentation
- Assess dependency management practices

**Deliverable:** Dependency health report with recommendations for updates or documentation

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'dependencies': [{'name': 'black', 'version': '23.12.1', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'chardet', 'version': '5.2.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'click', 'version': '8.1.7', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'dataclasses-json', 'version': '0.6.3', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'Flask', 'version': '3.0.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'GitPython', 'version': '3.1.40', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'Jinja2', 'version': '3.1.2', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'mypy', 'version': '1.7.1', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pathspec', 'version': '0.11.2', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pydantic', 'version': '2.12.4', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pygments', 'version': '2.17.2', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pylint', 'version': '3.0.3', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pytest', 'version': '7.4.3', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pytest-cov', 'version': '4.1.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'python-dotenv', 'version': '1.0.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'PyYAML', 'version': '6.0.1', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'requests', 'version': '2.31.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'toml', 'version': '0.10.2', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'types-PyYAML', 'version': '6.0.12.20250915', 'type': 'runtime', 'source': 'requirements.txt'}], 'total_count': 19, 'documented_prerequisites': []}
```

### Simulated Response

# Analysis Response: Dependency Analysis and Health Check

## Summary
This is a simulated response for prompt '1.2'.
The prompt asks the LLM to analyze: Analyze project dependencies for health, security, and documentation accuracy

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 7. Check code comments

**Prompt ID:** `comment_quality`
**Phase:** 0

### Prompt Text

```
# Check code comments

**Objective:** Detect comments that are outdated, missing, or inconsistent with code logic

**Tasks:**

**Deliverable:** 

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

Detect comments that are outdated, missing, or inconsistent with the code logic,
and recommend areas needing documentation improvements.

Analyze:
- Comments that contradict the actual code behavior
- TODO/FIXME comments that are outdated or vague
- Missing comments in complex or critical code sections
- Over-commented trivial code (noise)
- Inconsistent comment styles

Deliverable: List of comment issues with recommendations for improvement

```

### Simulated Response

# Analysis Response: Check code comments

## Summary
This is a simulated response for prompt 'comment_quality'.
The prompt asks the LLM to analyze: Detect comments that are outdated, missing, or inconsistent with code logic

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 8. Logging and Observability Review

**Prompt ID:** `2.2`
**Phase:** 2

### Prompt Text

```
# Logging and Observability Review

**Objective:** Evaluate logging practices and observability readiness

**Tasks:**
- Assess logging coverage and consistency
- Identify areas lacking proper error logging
- Evaluate log levels and message quality
- Check for structured logging practices
- Assess monitoring and metrics instrumentation
- Identify observability gaps

**Deliverable:** Observability assessment with gaps and recommendations

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'repository_path': '.'}
```

### Simulated Response

# Analysis Response: Logging and Observability Review

## Summary
This is a simulated response for prompt '2.2'.
The prompt asks the LLM to analyze: Evaluate logging practices and observability readiness

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 9. Error Handling & Resilience Verification

**Prompt ID:** `security.2`
**Phase:** 0

### Prompt Text

```
# Error Handling & Resilience Verification

**Objective:** Verify error handling patterns and system resilience

**Tasks:**
- Review error handling patterns across the codebase
- Check for proper exception handling and logging
- Identify areas where errors are silently swallowed
- Verify graceful degradation strategies
- Check for proper resource cleanup (file handles, connections, etc.)
- Review retry logic and circuit breaker patterns
- Assess error messages for information leakage
- Verify proper handling of edge cases and boundary conditions

**Deliverable:** **Error Handling Analysis**

## Error Handling Patterns
[Document common error handling patterns used]

## Issues Found
- **Missing Error Handling**: [List areas lacking proper error handling]
- **Silent Failures**: [List places where errors are ignored]
- **Resource Leaks**: [List potential resource leak scenarios]

## Resilience Assessment
[Evaluate system resilience and fault tolerance]

## Recommendations
[Specific improvements for error handling and resilience]


---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'todo_count': 0, 'sample_todos': [], 'security_issues_count': 2, 'sample_security_issues': [{'title': 'Potential security issue in quality_checker.py', 'description': 'Use of eval() detected'}, {'title': 'Potential security issue in quality_checker.py', 'description': 'Use of exec() detected'}]}
```

### Simulated Response

# Analysis Response: Error Handling & Resilience Verification

## Summary
This is a simulated response for prompt 'security.2'.
The prompt asks the LLM to analyze: Verify error handling patterns and system resilience

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 10. Security Vulnerability Assessment

**Prompt ID:** `security.1`
**Phase:** 0

### Prompt Text

```
# Security Vulnerability Assessment

**Objective:** Identify potential security vulnerabilities and unsafe practices in the codebase

**Tasks:**
- Scan for common security vulnerabilities (SQL injection, XSS, CSRF, etc.)
- Check for hardcoded credentials, API keys, or sensitive data
- Review authentication and authorization mechanisms
- Identify insecure cryptographic practices
- Check for unsafe deserialization or eval() usage
- Review file upload/download security
- Assess input validation and sanitization
- Check for security headers and CORS configuration

**Deliverable:** **Security Assessment Report**

## Critical Security Issues
[List any critical vulnerabilities found]

## Medium Priority Issues
[List medium-priority security concerns]

## Low Priority Issues
[List minor security improvements]

## Security Best Practices
[Recommendations for improving security posture]

## Compliance Considerations
[Any relevant compliance requirements (GDPR, HIPAA, etc.)]


---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'todo_count': 0, 'sample_todos': [], 'security_issues_count': 2, 'sample_security_issues': [{'title': 'Potential security issue in quality_checker.py', 'description': 'Use of eval() detected'}, {'title': 'Potential security issue in quality_checker.py', 'description': 'Use of exec() detected'}]}
```

### Simulated Response

# Analysis Response: Security Vulnerability Assessment

## Summary
This is a simulated response for prompt 'security.1'.
The prompt asks the LLM to analyze: Identify potential security vulnerabilities and unsafe practices in the codebase

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 11. Validate Documented Architecture Against Actual Code

**Prompt ID:** `1.1`
**Phase:** 1

### Prompt Text

```
# Validate Documented Architecture Against Actual Code

**Objective:** Verify if actual code structure matches documented architecture claims

**Tasks:**
- Compare claimed architectural pattern vs actual implementation
- Verify documented modules/layers exist in code
- Check if technology stack matches documentation
- Identify undocumented components or services
- Flag any significant documentation inaccuracies
- Assess overall architecture quality and appropriateness

**Deliverable:** Architecture validation report with discrepancies highlighted and recommendations

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'claimed_architecture': {'pattern': 'microservices', 'layers': ['service', 'repository'], 'components': ['Core', 'DocumentationAnalyzer', 'CodeAnalyzer', 'ValidationEngine', 'PromptGenerator']}, 'actual_structure': {'languages': [{'name': 'Python', 'percentage': 27.48}, {'name': 'Shell', 'percentage': 3.32}], 'frameworks': ['Flask', 'Django'], 'entry_points': []}, 'validation_results': [{'status': 'valid', 'evidence': "Detected frameworks: ['Flask', 'Django']", 'recommendation': 'Architecture pattern appears consistent'}, {'status': 'partial', 'evidence': 'Found 0/5 claimed components', 'recommendation': 'Review documented component list for accuracy'}]}
```

### Simulated Response

# Analysis Response: Validate Documented Architecture Against Actual Code

## Summary
This is a simulated response for prompt '1.1'.
The prompt asks the LLM to analyze: Verify if actual code structure matches documented architecture claims

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 12. Call Graph & Dependency Tracing

**Prompt ID:** `arch.1`
**Phase:** 0

### Prompt Text

```
# Call Graph & Dependency Tracing

**Objective:** Map critical execution paths and dependency relationships

**Tasks:**
- Identify main entry points and critical execution paths
- Trace call graphs for key functionality
- Map dependencies between modules and components
- Identify circular dependencies
- Analyze depth and complexity of call chains
- Find tightly coupled components
- Identify unused or dead code paths
- Map external API and service dependencies

**Deliverable:** **Call Graph Analysis**

## Critical Execution Paths
[Document main execution flows]

## Dependency Map
[Visual or textual representation of key dependencies]

## Circular Dependencies
[List any circular dependencies found]

## Coupling Analysis
- **Tightly Coupled**: [Components with high coupling]
- **Loosely Coupled**: [Well-isolated components]

## Dead Code
[Unused functions, classes, or modules]

## Recommendations
[Suggestions for improving dependency structure]


---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'dependencies': [{'name': 'black', 'version': '23.12.1', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'chardet', 'version': '5.2.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'click', 'version': '8.1.7', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'dataclasses-json', 'version': '0.6.3', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'Flask', 'version': '3.0.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'GitPython', 'version': '3.1.40', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'Jinja2', 'version': '3.1.2', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'mypy', 'version': '1.7.1', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pathspec', 'version': '0.11.2', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pydantic', 'version': '2.12.4', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pygments', 'version': '2.17.2', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pylint', 'version': '3.0.3', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pytest', 'version': '7.4.3', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'pytest-cov', 'version': '4.1.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'python-dotenv', 'version': '1.0.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'PyYAML', 'version': '6.0.1', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'requests', 'version': '2.31.0', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'toml', 'version': '0.10.2', 'type': 'runtime', 'source': 'requirements.txt'}, {'name': 'types-PyYAML', 'version': '6.0.12.20250915', 'type': 'runtime', 'source': 'requirements.txt'}], 'total_count': 19, 'documented_prerequisites': []}
```

### Simulated Response

# Analysis Response: Call Graph & Dependency Tracing

## Summary
This is a simulated response for prompt 'arch.1'.
The prompt asks the LLM to analyze: Map critical execution paths and dependency relationships

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 13. Git Hotspots & Change Analysis

**Prompt ID:** `arch.2`
**Phase:** 0

### Prompt Text

```
# Git Hotspots & Change Analysis

**Objective:** Identify frequently changed files and potential problem areas

**Tasks:**
- Analyze git history to find frequently modified files
- Identify files with high churn rate
- Correlate file changes with bug fixes
- Find files touched by many different developers
- Identify files that change together (temporal coupling)
- Analyze commit message patterns for problem indicators
- Find areas with frequent merge conflicts
- Identify technical debt accumulation patterns

**Deliverable:** **Git Hotspot Analysis**

## High-Churn Files
[Files changed most frequently]

## Bug-Prone Areas
[Files with high correlation to bug fixes]

## Temporal Coupling
[Files that frequently change together]

## Merge Conflict Zones
[Areas with frequent conflicts]

## Developer Ownership
[Files with unclear or distributed ownership]

## Recommendations
- **Refactoring Priorities**: [Files that need attention]
- **Ownership**: [Suggestions for code ownership]
- **Process Improvements**: [Ways to reduce churn]


---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'todo_count': 0, 'sample_todos': [], 'security_issues_count': 2, 'sample_security_issues': [{'title': 'Potential security issue in quality_checker.py', 'description': 'Use of eval() detected'}, {'title': 'Potential security issue in quality_checker.py', 'description': 'Use of exec() detected'}]}
```

### Simulated Response

# Analysis Response: Git Hotspots & Change Analysis

## Summary
This is a simulated response for prompt 'arch.2'.
The prompt asks the LLM to analyze: Identify frequently changed files and potential problem areas

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 14. Cohesion & Coupling Boundary Analysis

**Prompt ID:** `arch.4`
**Phase:** 0

### Prompt Text

```
# Cohesion & Coupling Boundary Analysis

**Objective:** Assess module cohesion and coupling at architectural boundaries

**Tasks:**
- Analyze cohesion within modules and classes
- Measure coupling between architectural layers
- Identify violations of architectural boundaries
- Check adherence to separation of concerns
- Assess API boundary design
- Review data flow across boundaries
- Identify leaky abstractions
- Evaluate interface segregation

**Deliverable:** **Cohesion & Coupling Analysis**

## Cohesion Assessment
- **High Cohesion**: [Well-focused modules]
- **Low Cohesion**: [Modules doing too many things]

## Coupling Assessment
- **Tight Coupling**: [Problematic dependencies]
- **Appropriate Coupling**: [Acceptable dependencies]

## Boundary Violations
[Cases where architectural boundaries are crossed inappropriately]

## Leaky Abstractions
[Abstractions that expose implementation details]

## Recommendations
- **Refactoring**: [Specific areas to improve cohesion/coupling]
- **Architectural Changes**: [Larger structural improvements]
- **Interface Design**: [API improvements]


---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'claimed_architecture': {'pattern': 'microservices', 'layers': ['service', 'repository'], 'components': ['Core', 'DocumentationAnalyzer', 'CodeAnalyzer', 'ValidationEngine', 'PromptGenerator']}, 'actual_structure': {'languages': [{'name': 'Python', 'percentage': 27.48}, {'name': 'Shell', 'percentage': 3.32}], 'frameworks': ['Flask', 'Django'], 'entry_points': []}, 'validation_results': [{'status': 'valid', 'evidence': "Detected frameworks: ['Flask', 'Django']", 'recommendation': 'Architecture pattern appears consistent'}, {'status': 'partial', 'evidence': 'Found 0/5 claimed components', 'recommendation': 'Review documented component list for accuracy'}]}
```

### Simulated Response

# Analysis Response: Cohesion & Coupling Boundary Analysis

## Summary
This is a simulated response for prompt 'arch.4'.
The prompt asks the LLM to analyze: Assess module cohesion and coupling at architectural boundaries

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 15. Code Quality and Technical Debt Assessment

**Prompt ID:** `2.1`
**Phase:** 2

### Prompt Text

```
# Code Quality and Technical Debt Assessment

**Objective:** Assess code quality, identify technical debt, and security concerns

**Tasks:**
- Review TODO/FIXME comments for patterns and urgency
- Assess potential security issues (hardcoded secrets, etc.)
- Identify areas with high technical debt
- Evaluate error handling patterns
- Assess code organization and modularity
- Identify anti-patterns or code smells

**Deliverable:** Code quality report with prioritized remediation recommendations

---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'todo_count': 0, 'sample_todos': [], 'security_issues_count': 2, 'sample_security_issues': [{'title': 'Potential security issue in quality_checker.py', 'description': 'Use of eval() detected'}, {'title': 'Potential security issue in quality_checker.py', 'description': 'Use of exec() detected'}]}
```

### Simulated Response

# Analysis Response: Code Quality and Technical Debt Assessment

## Summary
This is a simulated response for prompt '2.1'.
The prompt asks the LLM to analyze: Assess code quality, identify technical debt, and security concerns

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 16. Test Coverage & Quality Strategy

**Prompt ID:** `strategy.3`
**Phase:** 0

### Prompt Text

```
# Test Coverage & Quality Strategy

**Objective:** Develop comprehensive testing strategy and improve test quality

**Tasks:**
- Assess current test coverage (unit, integration, e2e)
- Identify critical paths lacking tests
- Evaluate test quality and maintainability
- Review test execution time and flakiness
- Assess test data management
- Evaluate testing infrastructure and CI/CD
- Identify opportunities for test automation
- Recommend testing best practices

**Deliverable:** **Testing Strategy**

## Current Test Coverage
- **Unit Tests**: [Coverage and quality]
- **Integration Tests**: [Coverage and quality]
- **E2E Tests**: [Coverage and quality]
- **Overall Coverage**: [Percentage and critical gaps]

## Test Quality Issues
- **Flaky Tests**: [Tests that fail intermittently]
- **Slow Tests**: [Tests that slow down CI/CD]
- **Brittle Tests**: [Tests that break easily]

## Critical Gaps
[Functionality that lacks adequate testing]

## Recommended Approach
- **Test Pyramid**: [Balance of unit/integration/e2e tests]
- **Test Data**: [Strategy for test data management]
- **Mocking**: [When and how to use mocks]
- **Coverage Goals**: [Realistic coverage targets]

## Implementation Plan
1. **Immediate**: [Critical test gaps to fill]
2. **Short-term**: [Test infrastructure improvements]
3. **Long-term**: [Testing culture and practices]


---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'repository_path': '.'}
```

### Simulated Response

# Analysis Response: Test Coverage & Quality Strategy

## Summary
This is a simulated response for prompt 'strategy.3'.
The prompt asks the LLM to analyze: Develop comprehensive testing strategy and improve test quality

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 17. Observability & Instrumentation Strategy

**Prompt ID:** `strategy.2`
**Phase:** 0

### Prompt Text

```
# Observability & Instrumentation Strategy

**Objective:** Plan comprehensive observability and monitoring approach

**Tasks:**
- Assess current logging practices and coverage
- Review metrics collection and monitoring
- Evaluate distributed tracing capabilities
- Check error tracking and alerting
- Assess performance monitoring
- Review log aggregation and analysis tools
- Identify blind spots in observability
- Recommend instrumentation improvements

**Deliverable:** **Observability Strategy**

## Current Observability
- **Logging**: [Current logging approach and coverage]
- **Metrics**: [What metrics are collected]
- **Tracing**: [Distributed tracing capabilities]
- **Alerting**: [Current alerting setup]

## Gaps & Blind Spots
[Areas lacking visibility]

## Recommended Instrumentation
- **Structured Logging**: [Implement structured logging]
- **Key Metrics**: [Critical metrics to track]
- **Distributed Tracing**: [Tracing strategy for microservices]
- **Error Tracking**: [Centralized error tracking]
- **Performance Monitoring**: [APM and profiling]

## Tooling Recommendations
[Specific tools and platforms to consider]

## Implementation Roadmap
1. **Phase 1**: [Foundation - basic instrumentation]
2. **Phase 2**: [Enhancement - advanced observability]
3. **Phase 3**: [Optimization - proactive monitoring]


---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'repository_path': '.'}
```

### Simulated Response

# Analysis Response: Observability & Instrumentation Strategy

## Summary
This is a simulated response for prompt 'strategy.2'.
The prompt asks the LLM to analyze: Plan comprehensive observability and monitoring approach

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 18. Technical Debt & Refactoring Roadmap

**Prompt ID:** `strategy.4`
**Phase:** 0

### Prompt Text

```
# Technical Debt & Refactoring Roadmap

**Objective:** Create prioritized plan for addressing technical debt

**Tasks:**
- Catalog known technical debt items
- Assess impact and urgency of each debt item
- Estimate effort required for remediation
- Identify quick wins vs. long-term projects
- Prioritize based on business value and risk
- Create incremental refactoring plan
- Recommend debt prevention strategies
- Define metrics for tracking debt reduction

**Deliverable:** **Technical Debt Roadmap**

## Debt Inventory
[Categorized list of technical debt items]

## Prioritization Matrix
| Item | Impact | Effort | Priority | Timeline |
|------|--------|--------|----------|----------|
| ...  | ...    | ...    | ...      | ...      |

## Quick Wins
[High-value, low-effort improvements]

## Major Refactoring Projects
[Larger efforts requiring dedicated time]

## Incremental Approach
[How to chip away at debt alongside feature work]

## Prevention Strategy
- **Code Review**: [Standards to prevent new debt]
- **Architecture Review**: [Process for major changes]
- **Metrics**: [Track debt accumulation]

## Success Metrics
[How to measure progress on debt reduction]


---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'total_issues': 4, 'issues_by_severity': {'high': 2, 'medium': 0, 'low': 0}, 'top_issues': [{'type': 'architecture_drift', 'severity': 'valid', 'description': "Detected frameworks: ['Flask', 'Django']", 'recommendation': 'Architecture pattern appears consistent'}, {'type': 'architecture_drift', 'severity': 'partial', 'description': 'Found 0/5 claimed components', 'recommendation': 'Review documented component list for accuracy'}, {'type': 'code_quality', 'severity': 'high', 'description': 'Use of eval() detected', 'source': 'src/codebase_reviewer/analyzers/quality_checker.py'}, {'type': 'code_quality', 'severity': 'high', 'description': 'Use of exec() detected', 'source': 'src/codebase_reviewer/analyzers/quality_checker.py'}]}
```

### Simulated Response

# Analysis Response: Technical Debt & Refactoring Roadmap

## Summary
This is a simulated response for prompt 'strategy.4'.
The prompt asks the LLM to analyze: Create prioritized plan for addressing technical debt

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---

## 19. Team Mentorship & Best Practices Guide

**Prompt ID:** `strategy.5`
**Phase:** 0

### Prompt Text

```
# Team Mentorship & Best Practices Guide

**Objective:** Provide guidance for coaching team on code quality and best practices

**Tasks:**
- Identify common code quality issues in the codebase
- Document best practices for the team's tech stack
- Create examples of good vs. bad patterns
- Recommend code review guidelines
- Suggest pair programming or mob programming opportunities
- Identify areas where team training would help
- Recommend knowledge sharing practices
- Create onboarding guide for new developers

**Deliverable:** **Mentorship & Best Practices Guide**

## Common Issues & Solutions
[Patterns to avoid and better alternatives]

## Best Practices
- **Code Style**: [Consistent coding standards]
- **Architecture**: [Architectural patterns to follow]
- **Testing**: [Testing best practices]
- **Security**: [Security guidelines]
- **Performance**: [Performance considerations]

## Code Review Guidelines
[What to look for in code reviews]

## Learning Opportunities
- **Training Needs**: [Skills gaps to address]
- **Pair Programming**: [Good opportunities for pairing]
- **Knowledge Sharing**: [Topics for tech talks or docs]

## Onboarding Guide
[How to get new developers up to speed]

## Continuous Improvement
[Process for evolving practices over time]


---

**Repository Context:**
- Path: .
- Languages: Python, Shell

**Context Data:**

{'todo_count': 0, 'sample_todos': [], 'security_issues_count': 2, 'sample_security_issues': [{'title': 'Potential security issue in quality_checker.py', 'description': 'Use of eval() detected'}, {'title': 'Potential security issue in quality_checker.py', 'description': 'Use of exec() detected'}]}
```

### Simulated Response

# Analysis Response: Team Mentorship & Best Practices Guide

## Summary
This is a simulated response for prompt 'strategy.5'.
The prompt asks the LLM to analyze: Provide guidance for coaching team on code quality and best practices

## Key Findings
- [Simulated finding 1]
- [Simulated finding 2]
- [Simulated finding 3]

## Recommendations
- [Simulated recommendation 1]
- [Simulated recommendation 2]

## Context Analyzed
- Repository: .
- Languages: Python, Shell

---
*This is a simulated response. In interactive mode, Claude would provide actual analysis.*

---
