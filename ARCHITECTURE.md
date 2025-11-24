# 🔄 Self-Evolving Architecture

## Overview

This system creates **self-evolving documentation tools** through collaboration between:
- **Phase 1 Tool** (Go): Analyzes codebase, dialogues with user
- **AI Assistant** (You/Claude/GPT): Generates code and meta-prompts
- **Phase 2 Tools** (Go, AI-generated): Run offline, detect obsolescence, trigger regeneration

---

## The Complete Cycle

### **Phase 1: Interactive Dialogue & Analysis**

**Actors**: Go tool, User, AI Assistant

**Flow**:
```
1. User runs: review-codebase evolve /path/to/codebase
2. Go tool analyzes codebase (git repos, languages, structure)
3. Go tool dialogues with user:
   - "What documentation do you need?"
   - "What are your quality standards?"
   - "What patterns should I look for?"
   - "What should trigger regeneration?"
4. Go tool generates Phase 1 materials
5. User brings materials to AI Assistant
```

**Output**: Phase 1 materials ready for AI

---

### **Phase 2: Meta-Prompt Generation**

**Actors**: User, AI Assistant

**Flow**:
```
6. User: "Here's my codebase analysis. Generate Phase 2 tools."
7. AI Assistant (me) generates:
   a. Comprehensive meta-prompt (the "DNA" of the tools)
   b. Go code for Phase 2 tools
   c. Obsolescence detection logic
   d. Self-evolution triggers
```

**The Meta-Prompt Contains**:
- Codebase structure and patterns
- User requirements and quality standards
- Documentation generation instructions
- Code examples and templates
- **Self-evolution logic**: When and how to regenerate
- **Learnings from previous generations** (Gen 2+)

**The Go Tools Contain**:
- Documentation generation code
- **The meta-prompt baked in as a constant**
- Metrics tracking (files changed, patterns detected, errors)
- Obsolescence detection (thresholds)
- Meta-prompt re-emission logic

**Output**: 
- `phase2-tools-gen1/` directory with Go code
- `meta-prompt.md` baked into the tools
- Compiled binary ready to run

---

### **Phase 3: Offline Operation**

**Actors**: Phase 2 Tools (autonomous)

**Flow**:
```
8. Tools run offline: ./bin/generate-docs /path/to/codebase
9. Tools generate documentation
10. Tools track metrics:
    - Files analyzed: 1,234
    - Files changed since last run: 45 (3.6%)
    - New patterns detected: 2
    - Coverage: 94%
    - Staleness: 12 days
11. Tools check obsolescence thresholds:
    - Files changed > 20%? NO (3.6%)
    - New languages detected? NO
    - Error rate > 10%? NO
    - Staleness > 30 days? NO
    ✅ Still valid - continue running
```

**Output**: Documentation generated, metrics tracked

---

### **Phase 4: Obsolescence Detection & Regeneration**

**Actors**: Phase 2 Tools, User, AI Assistant

**Flow**:
```
12. Tools detect threshold breach:
    - Files changed: 287 (23.2%) ⚠️ > 20% threshold
    - New language detected: Rust ⚠️
    - Coverage dropped: 94% → 67% ⚠️
    
13. Tools emit regeneration prompt:
    
    ╔════════════════════════════════════════════════════════════╗
    ║  🔄 REGENERATION NEEDED                                    ║
    ╚════════════════════════════════════════════════════════════╝
    
    Obsolescence detected:
    - 23.2% of files changed (threshold: 20%)
    - New language: Rust
    - Coverage dropped: 94% → 67%
    
    📋 Meta-prompt saved to:
    /tmp/codebase-reviewer/MyProject/regeneration-prompt-gen2.md
    
    🤖 Next steps:
    1. Review the meta-prompt
    2. Give it to your AI assistant
    3. Ask AI to generate Gen 2 tools
    4. Replace Gen 1 tools with Gen 2 tools
    
    The meta-prompt includes:
    ✅ Original codebase analysis
    ✅ Learnings from Gen 1 (287 files changed, Rust added)
    ✅ Quality metrics (coverage, accuracy, performance)
    ✅ Improvement recommendations
    
14. User copies meta-prompt to AI Assistant

15. AI Assistant generates Gen 2 tools:
    - Incorporates learnings from Gen 1
    - Handles Rust files
    - Improved coverage logic
    - Updated meta-prompt for Gen 3
    
16. User replaces tools:
    mv phase2-tools-gen1 phase2-tools-gen1-backup
    # (Gen 2 tools compiled to phase2-tools-gen2/)
    
17. Cycle continues with Gen 2 tools...
```

**Output**: Improved Gen 2 tools, cycle continues

---

## Key Components

### 1. **Meta-Prompt** (The "DNA")

The meta-prompt is a comprehensive document that contains:

```markdown
# Meta-Prompt for Phase 2 Tool Generation

## Codebase Analysis
- Structure: 28 git repositories, 1,234 files
- Languages: Go (60%), Python (30%), JavaScript (10%)
- Patterns: Microservices, REST APIs, Event-driven

## User Requirements
- Documentation: Architecture diagrams, API docs, setup guides
- Quality: 95% coverage, <5% error rate
- Update frequency: Daily

## Generation Instructions
[Detailed instructions for AI to generate Go tools]

## Self-Evolution Logic
- Regenerate when:
  - Files changed > 20%
  - New language detected
  - Coverage < 90%
  - Staleness > 30 days

## Learnings (Gen 2+)
- Gen 1 → Gen 2: Added Rust support, improved coverage
- Gen 2 → Gen 3: Optimized performance, added caching
```

### 2. **Phase 2 Tools** (AI-Generated Go Code)

```go
package main

// META_PROMPT is baked into the binary
const META_PROMPT = `
# Meta-Prompt for Phase 2 Tool Generation
[... full meta-prompt ...]
`

func main() {
    // Generate documentation
    docs := generateDocs(codebasePath)
    
    // Track metrics
    metrics := trackMetrics(docs)
    
    // Check obsolescence
    if isObsolete(metrics) {
        emitRegenerationPrompt(META_PROMPT, metrics)
    }
}

func isObsolete(m Metrics) bool {
    return m.FilesChangedPercent > 20 ||
           m.NewLanguagesDetected ||
           m.Coverage < 90 ||
           m.StaleDays > 30
}

func emitRegenerationPrompt(metaPrompt string, m Metrics) {
    // Add learnings to meta-prompt
    enhanced := addLearnings(metaPrompt, m)
    
    // Save to file
    savePath := "/tmp/codebase-reviewer/.../regeneration-prompt-gen2.md"
    ioutil.WriteFile(savePath, []byte(enhanced), 0644)
    
    // Tell user
    fmt.Println("🔄 REGENERATION NEEDED")
    fmt.Println("Meta-prompt saved to:", savePath)
    fmt.Println("Give this to your AI assistant to generate Gen 2 tools")
}
```

---

## Benefits

### **For User**
- ✅ One-time AI interaction per generation
- ✅ Infinite offline runs between regenerations
- ✅ Tools improve over time (Gen 1 → Gen 2 → Gen 3)
- ✅ No API costs for daily runs
- ✅ Full control over when to regenerate

### **For AI Assistant**
- ✅ Clear, comprehensive prompts
- ✅ Learnings from previous generations
- ✅ Concrete metrics to optimize
- ✅ Iterative improvement

### **For Tools**
- ✅ Self-aware (know when they're obsolete)
- ✅ Self-documenting (meta-prompt explains everything)
- ✅ Self-evolving (trigger regeneration)
- ✅ Autonomous (run offline)

---

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| **Fidelity** | ≥95% | Compare AI-generated docs vs tool-generated docs |
| **Coverage** | ≥90% | % of files documented |
| **Staleness** | <30 days | Days since last regeneration |
| **Regeneration Frequency** | ~Monthly | Triggered by thresholds |
| **Cost** | <$5/year | One AI interaction per regeneration |

---

## The Magic

The **meta-prompt** is the key innovation:
- It's the "DNA" that gets passed from generation to generation
- It accumulates learnings over time
- It's baked into the tools themselves
- It enables true self-evolution

**Without meta-prompt**: Tools are static, become obsolete  
**With meta-prompt**: Tools know when they're obsolete and how to regenerate

