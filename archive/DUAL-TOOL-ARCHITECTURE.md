# Dual-Tool Architecture - Codebase Reviewer

This repository now contains **TWO complementary codebase analysis tools**:

## 🐍 Tool 1: Python-Based Analyzer (Original)

**Location**: `src/codebase_reviewer/`

**Purpose**: Python-based codebase analysis and review tool

**Technology**: Python 3.x

**Usage**:
```bash
./setup.sh
./start-web.sh
```

**Documentation**: See original `README.md` (now overwritten - check git history)

---

## 🔷 Tool 2: Go-Based Phase 1 Generator (New)

**Location**: `cmd/`, `internal/`, `pkg/`, `prompts/`

**Purpose**: Self-evolving codebase documentation system with LLM integration

**Technology**: Go 1.21+

**Usage**:
```bash
make build
./bin/generate-docs -v /path/to/codebase
```

**Documentation**:
- **`START-HERE.md`** - Quick orientation
- **`QUICK-START.md`** - 5-minute setup
- **`INSTRUCTIONS-FOR-CLAUDE.md`** - For Claude/LLM
- **`MANIFEST.md`** - Complete package details
- **`docs/EVOLUTION-SYSTEM.md`** - Evolution architecture

---

## 🔄 How They Work Together

### Option 1: Use Independently
- Use Python tool for web-based analysis
- Use Go tool for LLM-assisted documentation generation

### Option 2: Complementary Workflow
1. **Go Tool**: Generate initial analysis and prompts
2. **Provide to Claude**: Get Phase 2 tools
3. **Python Tool**: Use for ongoing web-based review
4. **Go Tool**: Regenerate when codebase evolves

---

## 📁 Repository Structure

```
codebase-reviewer/
├── 🐍 PYTHON TOOL
│   ├── src/codebase_reviewer/     # Python source
│   ├── tests/                     # Python tests
│   ├── setup.py                   # Python setup
│   ├── requirements.txt           # Python deps
│   ├── setup.sh                   # Python setup script
│   └── start-web.sh               # Web server
│
├── 🔷 GO TOOL
│   ├── cmd/generate-docs/         # Go CLI
│   ├── internal/                  # Go internal packages
│   ├── pkg/                       # Go public packages
│   ├── prompts/                   # YAML prompts
│   ├── Makefile                   # Go build
│   ├── go.mod                     # Go deps
│   └── go.sum                     # Go checksums
│
├── 📚 DOCUMENTATION
│   ├── START-HERE.md              # Quick start (Go tool)
│   ├── QUICK-START.md             # Setup guide (Go tool)
│   ├── INSTRUCTIONS-FOR-CLAUDE.md # For LLM (Go tool)
│   ├── MANIFEST.md                # Package details (Go tool)
│   ├── DUAL-TOOL-ARCHITECTURE.md  # This file
│   └── docs/                      # Detailed docs
│
└── 🔧 SHARED
    ├── .git/                      # Git repository
    ├── .gitignore                 # Ignore patterns
    ├── .pre-commit-config.yaml    # Git hooks
    └── LICENSE                    # License
```

---

## 🚀 Quick Start Guide

### For Python Tool
```bash
# Setup
./setup.sh

# Run web interface
./start-web.sh

# Access at http://localhost:5000
```

### For Go Tool
```bash
# Build
make build

# Analyze codebase
./bin/generate-docs -v /path/to/codebase

# Get prompt
cat /tmp/codebase-reviewer/{name}/phase1-llm-prompt.md

# Provide to Claude (see INSTRUCTIONS-FOR-CLAUDE.md)
```

---

## 🎯 When to Use Which Tool

### Use Python Tool When:
- You want a web-based interface
- You need interactive analysis
- You prefer Python ecosystem
- You want simulation capabilities

### Use Go Tool When:
- You want LLM-assisted documentation
- You need self-evolving tools
- You want offline Phase 2 tools
- You need generation-to-generation improvement
- You want all prompts as YAML

### Use Both When:
- You want comprehensive analysis
- You need multiple perspectives
- You're building a complete documentation system

---

## 🔒 Security Notes

### Python Tool
- Check original security documentation
- Review `.gitignore` for Python-specific patterns

### Go Tool
- **All outputs to `/tmp/codebase-reviewer/`**
- Multi-layered security protection
- See `INSTRUCTIONS-FOR-CLAUDE.md` for details

---

## 📝 Documentation Priority

If you're new to this repository:

1. **Read `START-HERE.md`** - Understand the Go tool
2. **Check git history** - See original Python README
3. **Read `DUAL-TOOL-ARCHITECTURE.md`** - This file
4. **Choose your tool** - Python or Go or both

---

## 🔄 Git Workflow

### Committing Changes

**Python Tool Changes**:
```bash
git add src/ tests/ setup.py requirements.txt
git commit -m "feat(python): your changes"
```

**Go Tool Changes**:
```bash
git add cmd/ internal/ pkg/ prompts/ Makefile go.mod
git commit -m "feat(go): your changes"
```

**Documentation Changes**:
```bash
git add docs/ *.md
git commit -m "docs: your changes"
```

### Checking Status
```bash
# See what's changed
git status

# See Python vs Go changes
git diff src/          # Python
git diff cmd/ pkg/     # Go
```

---

## 🆘 Troubleshooting

### Python Tool Issues
- Check `setup.sh` output
- Verify Python version
- Check `requirements.txt` dependencies

### Go Tool Issues
- Check Go version (need 1.21+)
- Run `make clean && make build`
- Check `QUICK-START.md` troubleshooting

### Conflicts Between Tools
- Tools are independent - no conflicts expected
- Different output directories
- Different dependencies

---

## 📈 Future Enhancements

### Potential Integration
- Go tool generates initial analysis
- Python tool provides web interface for results
- Shared data format (JSON/YAML)
- Unified reporting

### Separate Evolution
- Each tool can evolve independently
- Different use cases
- Different maintainers possible

---

## ✅ Status

- ✅ Python tool: Existing, functional
- ✅ Go tool: Newly added, complete
- ✅ Documentation: Complete for Go tool
- ⚠️  Integration: Not yet implemented (optional)

---

**Created**: 2025-11-23
**Purpose**: Document dual-tool architecture
**Maintainer**: See git history for contributors

---

## 🎉 Summary

You now have **two powerful codebase analysis tools** in one repository:

1. **Python Tool** - Web-based, interactive analysis
2. **Go Tool** - LLM-assisted, self-evolving documentation

Use them independently or together for comprehensive codebase understanding!

**Next Steps**:
- Try the Go tool: `make build && ./bin/generate-docs -v /path/to/codebase`
- Review Python tool: `./setup.sh && ./start-web.sh`
- Read documentation: `START-HERE.md`, `QUICK-START.md`
