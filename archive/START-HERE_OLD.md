# 👋 START HERE - Codebase Reviewer Tool

Welcome! This is a **self-contained, self-evolving codebase analysis tool** that works with Claude to generate comprehensive documentation.

## 🎯 What You Have

A complete package that:
1. **Analyzes any codebase** - Scans structure, languages, patterns
2. **Generates LLM prompts** - Creates detailed prompts for Claude
3. **Evolves over time** - Tools improve with each generation
4. **Protects proprietary data** - Multi-layered security

## 📖 Read These Files in Order

### 1️⃣ First: Understand What This Is
- **`README.md`** (5 min read)
  - Overview of the tool
  - Key features
  - How it works

### 2️⃣ Second: Get Started Quickly
- **`QUICK-START.md`** (5 min read + 5 min setup)
  - Build the tool
  - Analyze your first codebase
  - Generate documentation

### 3️⃣ Third: Instructions for Claude
- **`INSTRUCTIONS-FOR-CLAUDE.md`** (10 min read)
  - **CRITICAL**: Read this before providing prompts to Claude
  - Complete workflow
  - Security requirements
  - Example responses

### 4️⃣ Fourth: Deep Dive (Optional)
- **`docs/EVOLUTION-SYSTEM.md`** (15 min read)
  - How the evolution system works
  - Architecture diagrams
  - Best practices

- **`MANIFEST.md`** (10 min read)
  - Complete package contents
  - File-by-file breakdown
  - Key concepts

## 🚀 Quick Start (Right Now!)

```bash
# 1. Build (30 seconds)
cd codebase-reviewer-tool
make build

# 2. Analyze a codebase (1 minute)
./bin/generate-docs -v /path/to/your/codebase

# 3. Get the prompt (10 seconds)
cat /tmp/codebase-reviewer/{codebase-name}/phase1-llm-prompt.md

# 4. Provide to Claude (2 minutes)
# - Open Claude
# - Say: "I have a codebase analysis prompt"
# - Paste the prompt
# - Add: "Please read INSTRUCTIONS-FOR-CLAUDE.md first"

# 5. Done! Claude will generate Phase 2 tools
```

## 🎓 Learning Path

### Beginner (Just Want to Use It)
1. Read `README.md`
2. Follow `QUICK-START.md`
3. Provide prompt to Claude
4. Run generated tools

**Time**: 15 minutes

### Intermediate (Want to Understand It)
1. Read `README.md`
2. Read `QUICK-START.md`
3. Read `INSTRUCTIONS-FOR-CLAUDE.md`
4. Skim `docs/EVOLUTION-SYSTEM.md`
5. Use the tool

**Time**: 30 minutes

### Advanced (Want to Customize It)
1. Read all documentation
2. Study `prompts/templates/` files
3. Review `pkg/learnings/` code
4. Customize prompt templates
5. Extend Phase 2 tools

**Time**: 1-2 hours

## 🔑 Key Concepts (30 Second Version)

**Phase 1**: This tool scans codebases and generates prompts for Claude

**Phase 2**: Claude generates custom tools that create documentation

**Evolution**: Tools detect when they're outdated and regenerate with improvements

**Security**: All proprietary data goes to `/tmp/` - never committed to git

**YAML Prompts**: All LLM prompts are YAML files - easy to inspect and edit

## 📁 File Guide

```
📄 START-HERE.md                    ← You are here
📄 README.md                        ← Overview
📄 QUICK-START.md                   ← 5-minute setup
📄 INSTRUCTIONS-FOR-CLAUDE.md       ← For Claude (CRITICAL)
📄 MANIFEST.md                      ← Package contents

docs/
  📄 EVOLUTION-SYSTEM.md            ← Evolution guide
  📄 EVOLUTION-SUMMARY.md           ← Quick reference
  📄 NEXT-STEPS.md                  ← Detailed usage
  📄 GIT-COMMIT-CHECKLIST.md        ← Security checklist

prompts/
  templates/
    📄 phase1-prompt-template.yaml              ← Initial prompt
    📄 phase1-regeneration-prompt-template.yaml ← Regeneration prompt
  schemas/
    📄 learnings-schema.yaml                    ← Learnings structure

cmd/generate-docs/main.go           ← Phase 1 tool (CLI)
pkg/learnings/                      ← Evolution system
internal/scanner/                   ← Codebase scanner
internal/prompt/                    ← Prompt generator
```

## ✅ Checklist Before First Use

- [ ] Read `README.md`
- [ ] Read `QUICK-START.md`
- [ ] Read `INSTRUCTIONS-FOR-CLAUDE.md`
- [ ] Have Go 1.21+ installed
- [ ] Have access to Claude
- [ ] Understand security requirements
- [ ] Know where outputs go (`/tmp/codebase-reviewer/`)

## 🆘 Common Questions

### Q: What does this tool do?
**A**: Analyzes codebases and generates prompts for Claude to create documentation tools.

### Q: Do I need to know Go?
**A**: No! Just run `make build` and use the tool. Claude generates the Phase 2 tools.

### Q: Is my proprietary code safe?
**A**: Yes! All outputs go to `/tmp/` with multi-layered protection. See `INSTRUCTIONS-FOR-CLAUDE.md`.

### Q: How long does it take?
**A**: 5 minutes to build and analyze, 2 minutes for Claude to generate tools.

### Q: What if my codebase changes?
**A**: Tools detect obsolescence and regenerate with improvements. See `docs/EVOLUTION-SYSTEM.md`.

### Q: Can I customize the prompts?
**A**: Yes! Edit `prompts/templates/*.yaml` files.

### Q: What LLMs are supported?
**A**: Claude (recommended), but any LLM that can read YAML and generate Go code.

## 🎯 Next Steps

1. **Read `README.md`** - Understand what this tool does
2. **Follow `QUICK-START.md`** - Build and run your first analysis
3. **Read `INSTRUCTIONS-FOR-CLAUDE.md`** - Before providing prompts to Claude
4. **Analyze a codebase** - Try it on a real project
5. **Watch it evolve** - See tools improve over generations

## 💡 Pro Tips

1. **Start small** - Try on a small codebase first
2. **Read learnings** - Check `learnings.yaml` after each run
3. **Edit prompts** - Customize YAML prompts before sending to Claude
4. **Keep backups** - Save working tools before regenerating
5. **Check security** - Verify no proprietary data in git

## 🎉 Ready?

```bash
cd codebase-reviewer-tool
make build
./bin/generate-docs -v /path/to/your/codebase
```

Then read the generated prompt and provide it to Claude!

---

**Questions?** Read `README.md` and `INSTRUCTIONS-FOR-CLAUDE.md`
**Issues?** Check `QUICK-START.md` troubleshooting section
**Want to learn more?** Read `docs/EVOLUTION-SYSTEM.md`

**Let's go!** 🚀
