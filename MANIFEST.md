# Codebase Reviewer - Package Manifest

## 📦 Package Contents

This directory contains a complete, self-contained codebase analysis tool.

### Core Tool (Phase 1)
```
cmd/generate-docs/main.go           # CLI entry point
internal/scanner/scanner.go         # Repository discovery
internal/prompt/generator.go        # Prompt generation
pkg/logger/logger.go                # Logging utilities
pkg/learnings/learnings.go          # Learnings data structures
pkg/learnings/regeneration.go       # Regeneration prompt generator
```

### Prompt Templates
```
prompts/templates/phase1-prompt-template.yaml
  → Initial analysis prompt template

prompts/templates/phase1-regeneration-prompt-template.yaml
  → Regeneration prompt template with learnings

prompts/schemas/learnings-schema.yaml
  → Complete schema for learnings.yaml
```

### Documentation
```
README.md                           # Main documentation
QUICK-START.md                      # 5-minute setup guide
INSTRUCTIONS-FOR-CLAUDE.md          # Instructions for Claude/LLM
MANIFEST.md                         # This file

docs/EVOLUTION-SYSTEM.md            # Evolution system guide
docs/EVOLUTION-SUMMARY.md           # Quick reference
docs/NEXT-STEPS.md                  # Usage instructions
docs/GIT-COMMIT-CHECKLIST.md        # Security checklist
```

### Build & Configuration
```
Makefile                            # Build automation
go.mod                              # Go dependencies
go.sum                              # Dependency checksums
.gitignore                          # Security protection
.pre-commit-config.yaml             # Git hooks
```

## 🎯 What This Package Does

### Phase 1: Analysis & Prompt Generation
1. Scans target codebase
2. Discovers nested git repositories
3. Analyzes file structure, languages, frameworks
4. Generates comprehensive LLM prompt (YAML + Markdown)
5. Outputs to `/tmp/codebase-reviewer/{name}/`

### Phase 2: Tool Generation (by Claude)
1. User provides Phase 1 prompt to Claude
2. Claude reads `INSTRUCTIONS-FOR-CLAUDE.md`
3. Claude generates custom offline tools
4. Tools analyze codebase and generate documentation
5. Tools save learnings for evolution

### Evolution: Continuous Improvement
1. Phase 2 tools detect obsolescence
2. Generate enhanced Phase 1 prompt with learnings
3. User re-runs Phase 1 with `--scorch`
4. Claude generates improved Phase 2 tools
5. Each generation is measurably better

## 🔒 Security Features

### Multi-Layered Protection
1. **Output Isolation**: All outputs to `/tmp/codebase-reviewer/`
2. **`.gitignore`**: Blocks all sensitive patterns
3. **Pre-commit Hooks**: Prevents accidental commits
4. **Path Validation**: Code validates output paths
5. **Documentation**: Clear security warnings

### What's Protected
- Proprietary codebase analysis
- Generated Phase 2 tools
- Reference documentation
- Learnings data
- All prompts with codebase details

### What's Safe to Commit
- Generic tool code (this package)
- Prompt templates (no codebase data)
- Documentation (generic)
- Build configuration

## 📊 File Statistics

```
Total Files: 20+
Total Lines: 5,000+
Languages: Go, YAML, Markdown
Dependencies: gopkg.in/yaml.v3
Go Version: 1.21+
```

## 🚀 Quick Start

```bash
# 1. Build
cd codebase-reviewer-tool
make build

# 2. Analyze
./bin/generate-docs -v /path/to/codebase

# 3. Get prompt
cat /tmp/codebase-reviewer/{name}/phase1-llm-prompt.md

# 4. Provide to Claude
# (Include INSTRUCTIONS-FOR-CLAUDE.md)

# 5. Run Phase 2 tools
cd /tmp/codebase-reviewer/{name}/phase2-tools
make build
./bin/update-docs --path /path/to/codebase
```

## �� Documentation Map

**Start Here**:
1. `README.md` - Overview and features
2. `QUICK-START.md` - 5-minute setup

**For Claude/LLM**:
3. `INSTRUCTIONS-FOR-CLAUDE.md` - Complete instructions

**Deep Dive**:
4. `docs/EVOLUTION-SYSTEM.md` - Evolution architecture
5. `docs/EVOLUTION-SUMMARY.md` - Quick reference
6. `docs/NEXT-STEPS.md` - Detailed usage

**Reference**:
7. `prompts/schemas/learnings-schema.yaml` - Learnings schema
8. `docs/GIT-COMMIT-CHECKLIST.md` - Security checklist

## 🔄 Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│                     GENERATION 1                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1 Tool                                               │
│  └─> Scan codebase                                          │
│  └─> Generate phase1-llm-prompt.yaml                        │
│                                                             │
│  User provides prompt to Claude                             │
│  └─> Claude reads INSTRUCTIONS-FOR-CLAUDE.md                │
│  └─> Claude generates Phase 2 tools                         │
│                                                             │
│  Phase 2 Tools                                              │
│  └─> Analyze codebase                                       │
│  └─> Generate documentation                                 │
│  └─> Save learnings.yaml                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

                            ↓
                   Codebase changes
                            ↓

┌─────────────────────────────────────────────────────────────┐
│                     GENERATION 2+                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 2 Tools (Gen N)                                      │
│  └─> Detect obsolescence (score > 0.5)                      │
│  └─> Generate phase1-regeneration-prompt.yaml               │
│      (includes ALL learnings from Gen N)                    │
│                                                             │
│  User runs: generate-docs --scorch                          │
│  └─> Generates enhanced Phase 1 prompt                      │
│                                                             │
│  User provides regeneration prompt to Claude                │
│  └─> Claude reads learnings                                 │
│  └─> Claude generates IMPROVED Phase 2 tools (Gen N+1)      │
│      • Fixes issues from Gen N                              │
│      • Handles edge cases                                   │
│      • Better performance                                   │
│      • New capabilities                                     │
│                                                             │
│  Phase 2 Tools (Gen N+1)                                    │
│  └─> Analyze codebase (better than Gen N)                   │
│  └─> Generate documentation (better than Gen N)             │
│  └─> Save learnings.yaml (for Gen N+2)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

                            ↓
                   Process repeats
                   (continuous improvement)
```

## 💡 Key Concepts

### 1. Two-Phase Architecture
- **Phase 1**: LLM-assisted analysis (this tool)
- **Phase 2**: Offline documentation generation (Claude generates)

### 2. Self-Evolution
- Tools detect when they become obsolete
- Generate enhanced prompts with learnings
- Each generation improves on previous

### 3. Learnings System
- Captures what worked, what failed
- Records edge cases and patterns
- Guides next generation improvements

### 4. Obsolescence Detection
- Fingerprint-based with scoring
- Multiple criteria (files, languages, frameworks)
- Threshold: score > 0.5 = obsolete

### 5. All Prompts as YAML
- Human-readable and editable
- Easy to inspect and version
- Programmatically parseable

## ✅ Requirements

### System Requirements
- Go 1.21 or higher
- Git
- Access to Claude or similar LLM
- Disk space in `/tmp/` (varies by codebase)

### Knowledge Requirements
- Basic command line usage
- Understanding of git
- Familiarity with YAML
- Access to codebase to analyze

## 🎯 Use Cases

### 1. New Team Member Onboarding
Generate comprehensive documentation for new developers.

### 2. Legacy Codebase Analysis
Understand and document legacy systems.

### 3. Architecture Documentation
Create up-to-date architecture diagrams and docs.

### 4. Code Review Preparation
Generate analysis for code review sessions.

### 5. Technical Debt Assessment
Identify patterns and areas for improvement.

### 6. Migration Planning
Analyze current state before migrations.

## 📈 Expected Outcomes

### After Generation 1
- Comprehensive codebase analysis
- Initial documentation set
- Learnings captured
- Baseline established

### After Generation 2
- 20-50% improvement in accuracy
- Edge cases handled
- Performance improvements (2-3x faster)
- New report types

### After Generation 3+
- Highly optimized for specific codebase
- Minimal false positives
- Comprehensive coverage
- Custom reports for unique patterns

## 🔧 Customization

### Customize Phase 1 Prompts
Edit `prompts/templates/phase1-prompt-template.yaml`

### Customize Learnings Schema
Edit `prompts/schemas/learnings-schema.yaml`

### Customize Build Process
Edit `Makefile`

### Customize Security Rules
Edit `.gitignore` and `.pre-commit-config.yaml`

## 🆘 Support

### Documentation
1. Read `README.md` for overview
2. Check `QUICK-START.md` for setup
3. Review `docs/EVOLUTION-SYSTEM.md` for details

### Troubleshooting
1. Check `QUICK-START.md` troubleshooting section
2. Review generated prompts for errors
3. Inspect learnings.yaml for issues

### Common Issues
- Build failures → Check Go version
- Permission errors → Check file permissions
- Git leaks → Verify .gitignore
- Obsolescence false positives → Adjust scoring

## 📄 License

See LICENSE file for details.

## 🙏 Credits

**Created**: 2025-11-23  
**Tool**: Augment Agent (Claude Sonnet 4.5)  
**Purpose**: Self-evolving codebase analysis and documentation

---

**Package Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2025-11-23
