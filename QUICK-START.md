# Quick Start Guide - Codebase Reviewer

## 🚀 5-Minute Setup

### Step 1: Build the Tool (30 seconds)
```bash
cd codebase-reviewer-tool
make build
```

### Step 2: Analyze Your Codebase (1 minute)
```bash
./bin/generate-docs -v /path/to/your/codebase
```

### Step 3: Get the Prompt (10 seconds)
```bash
cat /tmp/codebase-reviewer/{codebase-name}/phase1-llm-prompt.md
```

### Step 4: Provide to Claude (2 minutes)
1. Open Claude (Augment Agent, Claude.ai, etc.)
2. Say: "I have a codebase analysis prompt for you"
3. Paste the contents of `phase1-llm-prompt.md`
4. Add: "Please read INSTRUCTIONS-FOR-CLAUDE.md first"

### Step 5: Save Phase 2 Tools (1 minute)
Claude will generate Phase 2 tools. Save them to:
```bash
/tmp/codebase-reviewer/{codebase-name}/phase2-tools/
```

### Step 6: Run Phase 2 Tools (30 seconds)
```bash
cd /tmp/codebase-reviewer/{codebase-name}/phase2-tools
make build
./bin/update-docs --path /path/to/your/codebase
```

### Step 7: View Documentation (ongoing)
```bash
ls /tmp/codebase-reviewer/{codebase-name}/reference-materials/
```

## 📋 What You Get

After running Phase 2 tools, you'll have:

```
/tmp/codebase-reviewer/{codebase-name}/
├── phase1-llm-prompt.yaml          # Initial prompt
├── phase1-llm-prompt.md            # (Markdown version)
├── phase2-tools/                   # Generated tools
│   ├── cmd/update-docs/            # Main tool
│   ├── internal/                   # Analysis logic
│   ├── Makefile                    # Build automation
│   └── README.md                   # Tool documentation
├── reference-materials/            # Generated docs
│   ├── architecture/               # Architecture docs
│   ├── services/                   # Service docs
│   ├── development/                # Dev guides
│   └── README.md                   # Doc index
└── learnings.yaml                  # What the tool learned
```

## 🔄 Evolution Workflow

### When Your Codebase Changes

1. **Run Phase 2 tools again**:
   ```bash
   ./bin/update-docs --path /path/to/your/codebase
   ```

2. **If obsolete, tool will tell you**:
   ```
   ⚠️  Tool has become obsolete!
   ⚠️  Obsolescence score: 0.65
   ✅ Regeneration prompt saved to:
      - phase1-regeneration-prompt.yaml
      - phase1-regeneration-prompt.md
   ```

3. **Review what changed**:
   ```bash
   cat /tmp/codebase-reviewer/{name}/phase1-regeneration-prompt.md
   ```

4. **Regenerate**:
   ```bash
   cd codebase-reviewer-tool
   ./bin/generate-docs --scorch /path/to/your/codebase
   ```

5. **Provide regeneration prompt to Claude**:
   - Claude reads learnings from Gen 1
   - Generates improved Gen 2 tools
   - Fixes issues, handles edge cases, adds features

6. **Run improved tools**:
   ```bash
   cd /tmp/codebase-reviewer/{name}/phase2-tools
   make build
   ./bin/update-docs --path /path/to/your/codebase
   ```

## 💡 Pro Tips

### Tip 1: Use Verbose Mode
```bash
./bin/generate-docs -v /path/to/codebase
```
Shows detailed progress and helps with debugging.

### Tip 2: Review Learnings
```bash
cat /tmp/codebase-reviewer/{name}/learnings.yaml
```
See what the tool learned and what it struggled with.

### Tip 3: Edit Prompts Before Sending
```bash
code /tmp/codebase-reviewer/{name}/phase1-llm-prompt.yaml
```
Customize the prompt to focus on specific areas.

### Tip 4: Keep Generations
```bash
cp -r /tmp/codebase-reviewer/{name}/phase2-tools \
      /tmp/codebase-reviewer/{name}/phase2-tools-gen1-backup
```
Backup working tools before regenerating.

### Tip 5: Check Security
```bash
git status
git check-ignore /tmp/codebase-reviewer/{name}/
```
Verify proprietary data is protected.

## 🆘 Troubleshooting

### Problem: "Command not found: generate-docs"
**Solution**: Build the tool first
```bash
cd codebase-reviewer-tool
make build
```

### Problem: "Permission denied"
**Solution**: Make binary executable
```bash
chmod +x bin/generate-docs
```

### Problem: "No such file or directory: /tmp/codebase-reviewer/"
**Solution**: Run Phase 1 tool first
```bash
./bin/generate-docs -v /path/to/codebase
```

### Problem: "Phase 2 tools won't build"
**Solution**: Check Go version
```bash
go version  # Should be 1.21+
cd /tmp/codebase-reviewer/{name}/phase2-tools
go mod tidy
make build
```

### Problem: "Outputs appearing in git"
**Solution**: Check .gitignore
```bash
cat .gitignore | grep tmp
# Should see: /tmp/
```

## 📚 Next Steps

1. **Read the full documentation**:
   - `README.md` - Overview
   - `INSTRUCTIONS-FOR-CLAUDE.md` - For Claude
   - `docs/EVOLUTION-SYSTEM.md` - Evolution guide
   - `docs/NEXT-STEPS.md` - Detailed usage

2. **Customize prompts**:
   - Edit `prompts/templates/phase1-prompt-template.yaml`
   - Add custom analysis tasks
   - Adjust output formats

3. **Extend Phase 2 tools**:
   - Add new report types
   - Implement custom analyzers
   - Create specialized detectors

4. **Share learnings**:
   - Export learnings.yaml
   - Share patterns discovered
   - Contribute improvements

## ✅ Checklist

Before first use:
- [ ] Built Phase 1 tool (`make build`)
- [ ] Read `INSTRUCTIONS-FOR-CLAUDE.md`
- [ ] Understand security requirements
- [ ] Know where outputs go (`/tmp/codebase-reviewer/`)

Before each run:
- [ ] Codebase path is correct
- [ ] Have access to Claude/LLM
- [ ] Enough disk space in `/tmp/`

After each run:
- [ ] Review generated prompt
- [ ] Check learnings.yaml
- [ ] Verify documentation quality
- [ ] Confirm no proprietary data in git

## 🎯 Success Metrics

You'll know it's working when:
- ✅ Phase 1 generates comprehensive prompts
- ✅ Claude generates working Phase 2 tools
- ✅ Phase 2 tools generate useful documentation
- ✅ Learnings are captured after each run
- ✅ Tools detect obsolescence automatically
- ✅ Each generation is measurably better
- ✅ No proprietary data in git

---

**Time to first documentation**: ~10 minutes
**Time to regenerate**: ~5 minutes
**Improvement per generation**: 20-50%

**Ready to start?** Run `make build` and let's go! 🚀
