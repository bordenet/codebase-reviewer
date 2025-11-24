# Git Commit Checklist - Evolution System

## ✅ Files Safe to Commit to Public GitHub

These files contain NO proprietary information and are ready to push:

### Core Evolution System
- [x] `prompts/templates/phase1-regeneration-prompt-template.yaml`
- [x] `prompts/schemas/learnings-schema.yaml`
- [x] `pkg/learnings/learnings.go`
- [x] `pkg/learnings/regeneration.go`

### Documentation
- [x] `docs/EVOLUTION-SYSTEM.md`
- [x] `EVOLUTION-SUMMARY.md`
- [x] `NEXT-STEPS.md`
- [x] `GIT-COMMIT-CHECKLIST.md` (this file)

### Existing Files (Already Safe)
- [x] `cmd/generate-docs/main.go`
- [x] `internal/scanner/scanner.go`
- [x] `internal/prompt/generator.go`
- [x] `pkg/logger/logger.go`
- [x] `prompts/templates/phase1-prompt-template.yaml`
- [x] `.gitignore`
- [x] `.pre-commit-config.yaml`
- [x] `Makefile`
- [x] `README.md`
- [x] `go.mod`
- [x] `go.sum`

## ❌ Files to NEVER Commit

These files contain proprietary CARI information:

### In /tmp (Protected by Location)
- [ ] `/tmp/codebase-reviewer/Cari/phase1-llm-prompt.yaml`
- [ ] `/tmp/codebase-reviewer/Cari/phase1-llm-prompt.md`
- [ ] `/tmp/codebase-reviewer/Cari/phase1-analysis.md`
- [ ] `/tmp/codebase-reviewer/Cari/phase1-regeneration-prompt.yaml`
- [ ] `/tmp/codebase-reviewer/Cari/phase1-regeneration-prompt.md`
- [ ] `/tmp/codebase-reviewer/Cari/learnings.yaml`
- [ ] `/tmp/codebase-reviewer/Cari/SECURITY-VALIDATION.md`
- [ ] `/tmp/codebase-reviewer/Cari/README.md`
- [ ] `/tmp/codebase-reviewer/Cari/phase2-tools/**/*`
- [ ] `/tmp/codebase-reviewer/Cari/reference-materials/**/*`

### In CallBox Directory (Protected by .gitignore)
- [ ] `docs/architecture/system-overview.md` (CARI-specific)
- [ ] `docs/architecture/service-catalog.md` (CARI-specific)
- [ ] `docs/services/telephony-service.md` (CARI-specific)
- [ ] `docs/services/agent-api.md` (CARI-specific)
- [ ] Any file with "CARI" or "CallBox" in content

## 🔍 Pre-Commit Verification

Before committing, run these checks:

```bash
# 1. Check git status
git status

# 2. Verify no proprietary files
git diff --cached | grep -i "cari\|callbox\|proprietary"
# Should return nothing

# 3. Run pre-commit hooks
pre-commit run --all-files

# 4. Check .gitignore is working
git check-ignore /tmp/codebase-reviewer/Cari/phase1-analysis.md
# Should output the path (meaning it's ignored)

# 5. List files to be committed
git diff --cached --name-only
# Review carefully - should only be generic tool files
```

## 📦 Recommended Commit Commands

### Option 1: Commit Evolution System Only
```bash
cd /Users/matt/GitHub/CallBox

# Add evolution system files
git add prompts/templates/phase1-regeneration-prompt-template.yaml
git add prompts/schemas/learnings-schema.yaml
git add pkg/learnings/
git add docs/EVOLUTION-SYSTEM.md
git add EVOLUTION-SUMMARY.md
git add NEXT-STEPS.md
git add GIT-COMMIT-CHECKLIST.md

# Commit
git commit -m "feat: Add self-evolving architecture with learnings system

- Phase 2 tools detect obsolescence automatically
- Generate enhanced Phase 1 prompts with learnings
- All LLM prompts stored as YAML for easy inspection
- Tools progressively improve across generations
- Comprehensive documentation and examples"

# Push (if remote is set up)
git push origin main
```

### Option 2: Commit Everything (First Time Setup)
```bash
cd /Users/matt/GitHub/CallBox

# Initialize git if needed
git init

# Add all safe files
git add cmd/ internal/ pkg/ prompts/
git add .gitignore .pre-commit-config.yaml
git add Makefile README.md go.mod go.sum
git add docs/EVOLUTION-SYSTEM.md
git add EVOLUTION-SUMMARY.md NEXT-STEPS.md GIT-COMMIT-CHECKLIST.md

# Commit
git commit -m "feat: Initial commit - codebase-reviewer with evolution system

Phase 1 Tool:
- Scans codebases and generates LLM prompts
- Discovers nested git repositories
- Analyzes file structure and languages
- Outputs to /tmp for security

Evolution System:
- Phase 2 tools detect obsolescence
- Generate enhanced prompts with learnings
- Progressive improvement across generations
- All prompts stored as YAML

Security:
- Multi-layered protection against proprietary data leaks
- .gitignore blocks all sensitive patterns
- Pre-commit hooks prevent accidents
- All outputs isolated to /tmp"

# Set up remote and push
git remote add origin https://github.com/bordenet/codebase-reviewer.git
git branch -M main
git push -u origin main
```

## 🔒 Security Double-Check

Before pushing to GitHub, verify:

- [ ] No files from `/tmp/codebase-reviewer/` are staged
- [ ] No files with "CARI" in the name are staged
- [ ] No files with "CallBox" in the name are staged
- [ ] No proprietary analysis files are staged
- [ ] No Phase 2 tools for CARI are staged
- [ ] No reference materials for CARI are staged
- [ ] `.gitignore` is committed and comprehensive
- [ ] Pre-commit hooks are committed and active

## ✅ Final Verification

```bash
# Show what will be committed
git diff --cached --stat

# Show actual changes
git diff --cached

# If everything looks good, proceed with commit and push
```

## 📊 Summary

**Safe to Commit**: 15+ files (generic tool code)  
**Protected**: All CARI-specific analysis and outputs  
**Security**: Multi-layered protection active  
**Status**: ✅ Ready for public GitHub

---

**Last Updated**: 2025-11-23  
**Status**: Ready to commit
