# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/bordenet/codebase-reviewer.git
cd codebase-reviewer

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Basic Usage

### 1. Security & Quality Analysis

Analyze your codebase for security vulnerabilities and code quality issues:

```bash
# JSON output
python3 -m codebase_reviewer.cli analyze /path/to/your/project \
    --format json \
    --output analysis.json

# HTML report
python3 -m codebase_reviewer.cli analyze /path/to/your/project \
    --format html \
    --output report.html

# Interactive HTML dashboard
python3 -m codebase_reviewer.cli analyze /path/to/your/project \
    --format interactive-html \
    --output dashboard.html
```

**Features:**
- 🔒 **200 security rules** (SQL injection, XSS, hardcoded secrets, etc.)
- 📊 **101 quality rules** (complexity, maintainability, testing, documentation)
- 🎯 **Smart prioritization** by severity (critical, high, medium, low)
- 📈 **Detailed remediation** guidance for each issue

### 2. Compliance Reporting

Generate compliance reports for SOC2, HIPAA, or PCI-DSS:

```bash
# SOC2 compliance
python3 -m codebase_reviewer.cli compliance /path/to/your/project \
    --framework soc2 \
    --output soc2-report.json

# HIPAA compliance
python3 -m codebase_reviewer.cli compliance /path/to/your/project \
    --framework hipaa

# PCI-DSS compliance
python3 -m codebase_reviewer.cli compliance /path/to/your/project \
    --framework pci_dss
```

**Features:**
- ✅ Automated compliance checking
- 📋 Control-by-control violation reporting
- 📊 Compliance score calculation
- 🔧 Remediation guidance

### 3. Developer Productivity Metrics

Track developer productivity over time:

```bash
# Last 30 days
python3 -m codebase_reviewer.cli productivity /path/to/your/project \
    --days 30

# Last 90 days for specific author
python3 -m codebase_reviewer.cli productivity /path/to/your/project \
    --days 90 \
    --author "john@example.com"
```

**Metrics tracked:**
- 📝 Commits, files changed, lines of code
- 🐛 Bugs fixed vs introduced
- 📊 Code churn percentage
- 🎯 Productivity score (0-100)
- 💡 Automated insights and recommendations

### 4. ROI Calculator

Demonstrate the value of code analysis:

```bash
python3 -m codebase_reviewer.cli roi \
    --team-size 5 \
    --salary 120000 \
    --critical 20 \
    --high 50 \
    --medium 100 \
    --low 150 \
    --months 12
```

**Calculates:**
- ⏱️ Time savings (hours saved by early fixes)
- 🐛 Bug prevention value (production bugs avoided)
- 💰 Tool costs (setup, maintenance, licensing)
- 📈 ROI percentage and payback period

## Advanced Features

### Multi-Repository Analysis

Analyze multiple repositories in parallel:

```bash
python3 -m codebase_reviewer.cli multi-repo \
    /path/to/repo1 \
    /path/to/repo2 \
    /path/to/repo3 \
    --output dashboard.html
```

### Natural Language Queries

Ask questions about your analysis results:

```bash
python3 -m codebase_reviewer.cli ask \
    --analysis-file analysis.json \
    --question "What are the most critical security issues?"
```

### CI/CD Integration

See `.github/workflows/codebase-review.yml` for GitHub Actions integration example.

## Example Workflow

Run the comprehensive analysis script:

```bash
./examples/analyze_project.sh /path/to/your/project ./results
```

This will generate:
- Security and quality analysis (JSON, HTML, Interactive HTML)
- Compliance reports (SOC2, HIPAA, PCI-DSS)
- Productivity metrics (30-day and 90-day)
- ROI analysis

## Next Steps

- Read the [PRD](PRD.md) for complete feature documentation
- Check [DESIGN.md](DESIGN.md) for architecture details
- See [examples/](../examples/) for more usage examples
- Review [.github/workflows/](.github/workflows/) for CI/CD integration
