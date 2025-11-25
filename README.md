# Codebase Reviewer - Dual-Tool Suite

This repository contains **two powerful codebase analysis tools** that work together or independently:

## 🔍 Tool 1: Static Analysis Engine (Python)

**Industry-standard static analysis** with 300+ security and quality rules.

### Features
- ✅ **200+ Security Rules**: SQL injection, XSS, hardcoded secrets, OWASP Top 10
- ✅ **100+ Quality Rules**: Code smells, complexity, maintainability
- ✅ **Compliance Reporting**: SOC2, HIPAA, PCI-DSS automation
- ✅ **Interactive HTML Reports**: Real-time filtering, search, drill-down
- ✅ **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins
- ✅ **Multi-Language Support**: Python, JavaScript, TypeScript, Go, Java, Ruby, PHP, C#
- ✅ **Dependency Analysis**: SCA (Software Composition Analysis)
- ✅ **AI-Powered Fixes**: Automated remediation suggestions
- ✅ **ROI Calculator**: Demonstrate tool value

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

### Use Cases
- **Security Audits**: Find vulnerabilities before they reach production
- **Code Reviews**: Automated quality checks in CI/CD
- **Compliance**: SOC2, HIPAA, PCI-DSS compliance automation
- **Technical Debt**: Track and prioritize code quality issues

**Status**: ✅ **Production Ready** - A+ Grade (10 sprints complete)

**Documentation**: See [`docs/STATIC_ANALYSIS.md`](docs/STATIC_ANALYSIS.md)

---

## 🤖 Tool 2: Self-Evolving Documentation System (Go + Python)

**LLM-powered documentation generation** with auto-regenerative capabilities.

### The Big Idea

Use an LLM **once** to generate **offline tools** that regenerate documentation infinitely without the LLM.

```
Phase 1 (One-Time LLM Cost)
  Codebase → Analyzer → LLM → Offline Go Tools → Initial Docs

Phase 2 (Infinite, Free, Offline)
  Code Changes → Tools → Updated Docs (No LLM!)
                   ↓
            Obsolete? → Regenerate (Gen 2, Gen 3...)
```

### Features
- ✅ **v2.0 Prompt Architecture**: Structured schemas, OWASP/CWE mapping
- ✅ **Phase II Regeneration Flow**: Self-evolving tools that improve over time
- ✅ **Obsolescence Detection**: Multi-variate heuristics (files changed, new languages, coverage, staleness)
- ✅ **Metrics Tracking**: 8 dimensions (coverage, quality, performance, staleness)
- ✅ **Learning Capture**: Tools improve with each generation
- ✅ **Human-in-the-Loop**: Approval gates, rollback support
- ✅ **Three Scan Modes**: review (quick), deep_scan (thorough), scorch (exhaustive)
- ✅ **Tested & Validated**: Complete regeneration flow tested end-to-end

### Quick Start

```bash
# Generate Phase 1 prompt (v2.0 architecture)
review-codebase analyze-v2 /path/to/your/code

# View the generated prompt
cat /tmp/codebase-reviewer/YourCode/phase1_prompt_*.md

# Send prompt to LLM (Claude, GPT-4, etc.)
# Copy/paste the prompt to your LLM

# Save LLM response and generate Phase 2 tools (coming soon)
review-codebase generate-tools-v2 /tmp/codebase-reviewer/YourCode
```

### Use Cases
- **Documentation Generation**: LLM-quality docs without LLM costs
- **Codebase Understanding**: Deep analysis with structured outputs
- **Continuous Documentation**: Auto-update docs as code changes
- **Self-Improving Tools**: Tools get better over time

**Status**: 🚧 **v2.0 Architecture Complete** - Tool generation in progress

**Documentation**: See [`docs/V2_ARCHITECTURE.md`](docs/V2_ARCHITECTURE.md)

---

## 🎯 Which Tool Should I Use?

| Use Case | Tool 1: Static Analysis | Tool 2: Self-Evolving Docs |
|----------|-------------------------|----------------------------|
| **Security vulnerabilities** | ✅ Best choice | ❌ Not designed for this |
| **Code quality metrics** | ✅ Best choice | ❌ Not designed for this |
| **Compliance reporting** | ✅ Best choice | ❌ Not designed for this |
| **Documentation generation** | ❌ Not designed for this | ✅ Best choice |
| **Codebase understanding** | ⚠️ Basic | ✅ Best choice |
| **CI/CD integration** | ✅ Best choice | ⚠️ Coming soon |
| **Offline execution** | ✅ Yes | ✅ Yes (after initial LLM) |
| **LLM required** | ❌ No | ✅ Once (then offline) |

**Pro Tip**: Use **both tools together**!
- Tool 1 for security/quality/compliance
- Tool 2 for documentation and deep understanding

---

## 📦 Installation

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

## 📚 Documentation

### Tool 1: Static Analysis Engine
- [Quick Start Guide](docs/QUICK_START.md)
- [Features Comparison](docs/FEATURES_COMPARISON.md)
- [CI/CD Integration](docs/WORKFLOW_INTEGRATION_PROPOSAL.md)
- [Compliance Guide](docs/COMPLIANCE.md)

### Tool 2: Self-Evolving Documentation
- [v2.0 Architecture](docs/V2_ARCHITECTURE.md)
- [Phase 1 Prompt Template](prompts/templates/phase1-prompt-template.yaml)
- [Phase 2 Meta-Prompt Template](prompts/templates/meta-prompt-template.md)
- [Obsolescence Detection](docs/OBSOLESCENCE_DETECTION.md)

### General
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)

---

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test suites
pytest tests/test_security_rules.py  # Security rules
pytest tests/test_quality_rules.py   # Quality rules
pytest tests/test_compliance.py      # Compliance
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with ❤️ by [Matt Bordenet](https://github.com/bordenet)

Powered by:
- **Static Analysis**: Semgrep-inspired rule engine
- **LLM Integration**: Claude (Anthropic), GPT-4 (OpenAI)
- **Language Support**: Tree-sitter parsers
