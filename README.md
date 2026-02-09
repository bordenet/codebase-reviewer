# Codebase Reviewer

Two codebase analysis tools: static analysis (Python) and self-evolving documentation (Go + Python).

[![CI](https://github.com/bordenet/codebase-reviewer/actions/workflows/ci.yml/badge.svg)](https://github.com/bordenet/codebase-reviewer/actions/workflows/ci.yml)

## Tool 1: Static Analysis Engine (Python)

300+ security and quality rules. No LLM required.

### What It Does

- **200+ security rules** — SQL injection, XSS, hardcoded secrets, OWASP Top 10
- **100+ quality rules** — Code smells, complexity, maintainability
- **Compliance** — SOC2, HIPAA, PCI-DSS automation
- **HTML reports** — Interactive filtering, search, drill-down
- **CI/CD** — GitHub Actions, GitLab CI, Jenkins
- **Languages** — Python, JavaScript, TypeScript, Go, Java, Ruby, PHP, C#
- **SCA** — Dependency vulnerability scanning
- **Fix suggestions** — Automated remediation via AI

### Quick Start

```bash
# Install
pip install -e .

# Analyze a codebase
review-codebase analyze /path/to/your/code

# Generate interactive HTML report
review-codebase analyze /path/to/your/code --format html

# Check compliance
review-codebase compliance /path/to/your/code --framework soc2

# Calculate ROI
review-codebase roi /path/to/your/code
```

**Status**: 191 tests passing. See [`docs/STATIC_ANALYSIS.md`](docs/STATIC_ANALYSIS.md)

---

## Tool 2: Self-Evolving Documentation System (Go + Python)

Use an LLM **once** to generate **offline tools** that regenerate documentation without the LLM.

```
Phase 1 (One-Time LLM Cost)
  Codebase → Analyzer → LLM → Offline Go Tools → Initial Docs

Phase 2 (Offline, Free)
  Code Changes → Tools → Updated Docs (No LLM!)
```

### What It Does

- **Prompt architecture** — Structured schemas, OWASP/CWE mapping
- **Obsolescence detection** — Heuristics for files changed, coverage gaps, staleness
- **Metrics** — 8 dimensions (coverage, quality, performance, staleness)
- **Scan modes** — review (quick), deep_scan (thorough), scorch (exhaustive)
- **Tool generation** — `evolve` command compiles Go tools from LLM output
- **Version control** — Rollback, approval gates, version history

### Quick Start

```bash
# Option 1: Interactive mode (default) - You paste the LLM response
review-codebase evolve /path/to/your/code

# Option 2: API mode - Automatic LLM integration
review-codebase evolve /path/to/your/code --api --provider anthropic --model claude-sonnet-4

# Option 3: Manual workflow (Phase 1 only)
review-codebase analyze-v2 /path/to/your/code
cat /tmp/codebase-reviewer/YourCode/phase1_prompt_*.md
# Then use evolve command to process LLM response and generate tools
```

### Version Management & Rollback

Human-in-the-Loop features for safe tool evolution:

```bash
# List all tool versions
review-codebase versions /path/to/your/code

# View version history
review-codebase history /path/to/your/code

# Rollback to previous version
review-codebase rollback /path/to/your/code

# Rollback to specific version
review-codebase rollback /path/to/your/code --to-version 2

# Activate a specific version
review-codebase activate /path/to/your/code 1

# Request approval for regeneration
review-codebase approve /path/to/your/code --reason "Obsolescence detected"
```

See [`docs/V2_ARCHITECTURE.md`](docs/V2_ARCHITECTURE.md)

---

## Which Tool Should I Use?

| Use Case | Tool 1 | Tool 2 |
|----------|--------|--------|
| Security vulnerabilities | ✅ | ❌ |
| Code quality metrics | ✅ | ❌ |
| Compliance reporting | ✅ | ❌ |
| Documentation generation | ❌ | ✅ |
| Codebase understanding | ⚠️ | ✅ |
| CI/CD integration | ✅ | ⚠️ |
| Offline execution | ✅ | ✅ (after LLM) |
| LLM required | ❌ | ✅ Once |

Use Tool 1 for security/quality, Tool 2 for documentation.

---

## Installation

```bash
# Clone repository
git clone https://github.com/bordenet/codebase-reviewer.git
cd codebase-reviewer

# Install Python tool (Tool 1)
pip install -e .

# Build Go tool (Tool 2)
make build

# Verify installation
review-codebase --help
./bin/generate-docs -h
```

---

## Documentation

### Tool 1: Static Analysis Engine
- [Quick Start Guide](docs/QUICK_START.md)
- [Features Comparison](docs/FEATURES_COMPARISON.md)
- [CI/CD Integration](docs/WORKFLOW_INTEGRATION_PROPOSAL.md)

### Tool 2: Self-Evolving Documentation
- [v2.0 Architecture](docs/V2_ARCHITECTURE.md)
- [Phase 1 Prompt Template](prompts/templates/phase1-prompt-template.yaml)

### General
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)

---

## Testing

```bash
# Run all tests
make test

# Run specific test suites
pytest tests/test_security_rules.py  # Security rules
pytest tests/test_quality_rules.py   # Quality rules
pytest tests/test_compliance.py      # Compliance
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - See [LICENSE](LICENSE).

## Author

Matt Bordenet ([@bordenet](https://github.com/bordenet))
