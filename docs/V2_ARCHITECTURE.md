# Codebase Reviewer v2.0 Architecture

## Overview

Version 2.0 represents a major architectural upgrade with enhanced prompt engineering, structured output schemas, comprehensive metrics tracking, and robust obsolescence detection. This document describes the v2.0 architecture and how to use it.

## Key Improvements in v2.0

### 1. Structured Output Schemas

All Phase 1 tasks now have explicit JSON schemas defining expected outputs:

- **T1**: Comprehensive security and quality analysis with OWASP/CWE mapping
- **T2**: Materials plan for documentation generation
- **T3**: Go tool specifications with CLI design
- **T4**: Skeleton generation acknowledging token limits
- **T5**: Validation plan with concrete test commands
- **T6**: Security validation report with Pass/Fail/Warning status

### 2. Enhanced Security Analysis

- **OWASP Top 10 Mapping**: All security findings mapped to OWASP categories
- **CWE Integration**: Common Weakness Enumeration IDs for each finding
- **Confidence Levels**: High/Medium/Low confidence scoring
- **Severity Levels**: Critical/High/Medium/Low/Info classification
- **"Not Enough Information" Handling**: Prevents hallucination when data unavailable

### 3. Scan Modes

Three scan modes with different depth/focus:

- **review**: Quick scan for high-level insights (default)
- **deep_scan**: Thorough analysis with detailed findings
- **scorch**: Exhaustive analysis with maximum detail

### 4. Obsolescence Detection

Multi-variate heuristics to detect when Phase 2 tools become obsolete:

- Files changed percentage threshold (default: 20%)
- New languages detected
- Coverage drop detection (default: 10%)
- Staleness detection (default: 30 days)
- Error rate spike detection (default: 50% increase)
- False positive spike detection (default: 30% increase)
- Checksum diff on critical directories
- Cooldown period enforcement (default: 7 days)
- Fallback strategies for suppression

### 5. Comprehensive Metrics Tracking

Eight dimensions of metrics:

1. **Coverage**: files_total, files_analyzed, files_documented, coverage_percent
2. **Changes**: files_changed, files_changed_percent, files_added, files_deleted, new_languages
3. **Quality**: error_count, error_rate_percent, warning_count, false_positive_estimate
4. **Performance**: avg_runtime_seconds, memory_usage_mb
5. **Staleness**: last_run_date, days_since_last_run
6. **Patterns**: detected, newly_detected
7. **Tests**: regression_pass_count, regression_fail_count
8. **User Feedback**: human_override_flags, notes

### 6. Learning Capture Framework

Structured learning entries for continuous improvement:

```json
{
  "id": "string",
  "description": "string",
  "impact": "positive|neutral|negative",
  "actions_taken": ["string"],
  "validation": "string",
  "pending_issues": "string"
}
```

### 7. Human-in-the-Loop Workflow

- Approval gates before regeneration
- Rollback support to previous tool versions
- Incremental regeneration for efficiency
- Versioning and backward compatibility

## Usage

### Running Phase 1 Analysis (v2.0)

```bash
# Basic usage
codebase-reviewer analyze-v2 /path/to/codebase

# With scan mode
codebase-reviewer analyze-v2 /path/to/codebase --scan-mode deep_scan

# With custom output directory (must be in /tmp/)
codebase-reviewer analyze-v2 /path/to/codebase --output-dir /tmp/my-analysis

# With exclusions
codebase-reviewer analyze-v2 /path/to/codebase --exclude "*.test.js" --exclude "node_modules/*"

# With specific languages
codebase-reviewer analyze-v2 /path/to/codebase --languages python --languages go
```

### Output Structure

All outputs are saved to `/tmp/codebase-reviewer/{repo_name}/`:

```
/tmp/codebase-reviewer/MyRepo/
├── phase1_prompt_YYYYMMDD_HHMMSS.md  # Generated prompt for LLM
├── metrics.json                       # Initial metrics
└── (after LLM analysis)
    ├── phase1_response.json           # LLM response
    ├── phase2_tools/                  # Generated Go tools
    └── learning.json                  # Learning entries
```

### Security Features

1. **Forced /tmp/ Output**: All outputs must go to `/tmp/` to prevent git tracking
2. **CallBox Protection**: .gitignore and pre-commit hooks block any CallBox references
3. **IP Protection**: Pre-commit hooks scan for proprietary paths and code
4. **Validation Script**: `scripts/validate_security.sh` for comprehensive security checks

### Workflow

1. **Generate Phase 1 Prompt**:
   ```bash
   codebase-reviewer analyze-v2 /path/to/codebase
   ```

2. **Review Generated Prompt**:
   ```bash
   cat /tmp/codebase-reviewer/MyRepo/phase1_prompt_*.md
   ```

3. **Send to LLM**: Copy prompt and send to your LLM (Claude, GPT-4, etc.)

4. **Save LLM Response**:
   ```bash
   # Save LLM response to:
   /tmp/codebase-reviewer/MyRepo/phase1_response.json
   ```

5. **Validate Response** (future):
   ```bash
   codebase-reviewer validate-v2 /tmp/codebase-reviewer/MyRepo
   ```

6. **Generate Phase 2 Tools** (future):
   ```bash
   codebase-reviewer generate-tools-v2 /tmp/codebase-reviewer/MyRepo
   ```

## Architecture Components

### Core Modules

- **`prompts/v2_loader.py`**: Loads and parses v2.0 YAML templates
- **`prompts/generator_v2.py`**: Generates Phase 1 prompts from templates
- **`models_v2.py`**: Data models for v2.0 outputs
- **`validation/schema_validator.py`**: JSON schema validation
- **`obsolescence/detector.py`**: Obsolescence detection logic
- **`metrics/tracker.py`**: Metrics collection and persistence

### Templates

- **`prompts/templates/phase1-prompt-template.yaml`**: Phase 1 prompt template
- **`prompts/templates/meta-prompt-template.md`**: Phase 2 meta-prompt template

### Schemas

- **`schemas/phase1_task1_output.json`**: T1 comprehensive analysis schema
- **`schemas/phase1_task2_output.json`**: T2 materials plan schema
- **`schemas/phase1_task3_output.json`**: T3 tool specifications schema
- **`schemas/phase1_task5_output.json`**: T5 validation plan schema
- **`schemas/phase1_task6_output.json`**: T6 security validation schema
- **`schemas/metrics.json`**: Metrics structure schema
- **`schemas/learning.json`**: Learning entry schema

## Migration from v1.0

The v2.0 architecture is a complete redesign. Key differences:

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Prompt Structure | Multi-phase | Single Phase 1 |
| Output Format | Unstructured | JSON schemas |
| Security Mapping | Basic | OWASP/CWE |
| Confidence Levels | No | Yes |
| Obsolescence Detection | No | Yes |
| Metrics Tracking | Basic | Comprehensive |
| Learning Capture | No | Yes |
| Scan Modes | No | 3 modes |

## Next Steps

1. Implement `validate-v2` command for response validation
2. Implement `generate-tools-v2` command for Phase 2 tool generation
3. Add LLM integration for automated analysis
4. Implement incremental regeneration
5. Add visualization for metrics trends

## References

- [Phase 1 Prompt Template](../prompts/templates/phase1-prompt-template.yaml)
- [Phase 2 Meta-Prompt Template](../prompts/templates/meta-prompt-template.md)
- [Security Validation Script](../scripts/validate_security.sh)

