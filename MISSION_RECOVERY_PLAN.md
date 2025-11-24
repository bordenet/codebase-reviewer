# 🎯 Mission Recovery Plan: Build the REAL System

**Date**: 2025-11-24
**Goal**: Complete the Phase 1 → LLM → Phase 2 → Self-Evolution pipeline

---

## 📋 THE REAL COMMAND YOU WANT

```bash
# ONE COMMAND that does everything:
review-codebase evolve /Users/Matt/GitHub/CallBox \
  --llm-provider anthropic \
  --api-key $ANTHROPIC_API_KEY \
  --output-dir /tmp/callbox-reviewer \
  --auto-run \
  --watch

# This should:
# 1. Analyze CallBox codebase
# 2. Generate Phase 1 prompt
# 3. Send to Claude API automatically
# 4. Extract Phase 2 tool code from response
# 5. Compile Phase 2 tools (Go)
# 6. Run Phase 2 tools to generate docs
# 7. Compare LLM output vs Tool output
# 8. Watch for changes and re-run
# 9. Detect obsolescence and regenerate
```

**Current Status**: ❌ **NONE OF THIS EXISTS**

---

## 🏗️ BUILD PLAN (4 Phases)

### Phase A: LLM Integration (Week 1)
**Goal**: Automate LLM interaction

**Tasks**:
1. Create `src/codebase_reviewer/llm/` module
2. Implement Claude API client
3. Implement OpenAI API client (fallback)
4. Add prompt sending + response parsing
5. Add code extraction from markdown responses
6. Add error handling and retries

**Deliverables**:
```python
# src/codebase_reviewer/llm/client.py
class LLMClient:
    def send_prompt(self, prompt: str) -> LLMResponse
    def extract_code_blocks(self, response: str) -> Dict[str, str]
    def validate_response(self, response: LLMResponse) -> bool

# src/codebase_reviewer/llm/providers/anthropic.py
class AnthropicProvider(LLMClient):
    def send_prompt(self, prompt: str) -> LLMResponse

# src/codebase_reviewer/llm/providers/openai.py
class OpenAIProvider(LLMClient):
    def send_prompt(self, prompt: str) -> LLMResponse
```

**Test**:
```bash
review-codebase test-llm \
  --provider anthropic \
  --prompt "Generate a simple Go hello world program" \
  --extract-code
```

### Phase B: Phase 2 Tool Generation (Week 2)
**Goal**: Automatically generate and compile offline tools

**Tasks**:
1. Create `src/codebase_reviewer/phase2/` module
2. Implement tool code extraction
3. Implement Go project scaffolding
4. Implement automatic compilation
5. Implement tool validation
6. Add security checks (no proprietary code in git)

**Deliverables**:
```python
# src/codebase_reviewer/phase2/generator.py
class Phase2Generator:
    def generate_from_llm(
        self,
        codebase_path: Path,
        llm_client: LLMClient
    ) -> Phase2Tools:
        """Full pipeline: analyze → prompt → LLM → extract → compile."""
        pass
    
    def compile_tools(self, tools_dir: Path) -> bool:
        """Compile Go tools and validate."""
        pass
    
    def validate_tools(self, tools_dir: Path) -> ValidationReport:
        """Ensure tools work correctly."""
        pass

# src/codebase_reviewer/phase2/runner.py
class Phase2Runner:
    def run_tools(self, tools_dir: Path, codebase_path: Path) -> Path:
        """Execute Phase 2 tools to generate docs."""
        pass
```

**Test**:
```bash
review-codebase generate-phase2-tools /Users/Matt/GitHub/CallBox \
  --llm-provider anthropic \
  --output /tmp/callbox-tools \
  --compile \
  --validate
```

### Phase C: Comparison & Validation (Week 3)
**Goal**: Prove tools reproduce LLM quality

**Tasks**:
1. Create `src/codebase_reviewer/validation/` module
2. Implement LLM vs Tool output comparison
3. Implement quality metrics
4. Implement fidelity scoring
5. Generate comparison reports

**Deliverables**:
```python
# src/codebase_reviewer/validation/comparator.py
class ArtifactComparator:
    def compare_outputs(
        self,
        llm_output: Path,
        tool_output: Path
    ) -> ComparisonReport:
        """Compare LLM-generated vs tool-generated docs."""
        pass
    
    def calculate_fidelity_score(self, report: ComparisonReport) -> float:
        """Score 0-1: how well tools reproduce LLM output."""
        pass
    
    def generate_report(self, report: ComparisonReport) -> str:
        """Human-readable comparison report."""
        pass
```

**Test**:
```bash
# Generate docs both ways
review-codebase analyze /Users/Matt/GitHub/CallBox \
  --output /tmp/llm_output.md

/tmp/callbox-tools/bin/generate-docs /Users/Matt/GitHub/CallBox
# → /tmp/codebase-reviewer/CallBox/docs/

# Compare
review-codebase compare \
  --llm-output /tmp/llm_output.md \
  --tool-output /tmp/codebase-reviewer/CallBox/docs/ \
  --report /tmp/comparison_report.md

# Should show: "Fidelity: 95%+ ✅"
```

### Phase D: Self-Evolution Loop (Week 4)
**Goal**: Automatic regeneration when obsolete

**Tasks**:
1. Implement obsolescence detection
2. Implement learnings capture
3. Implement regeneration prompt generation
4. Implement automatic re-generation
5. Add watch mode for continuous monitoring

**Deliverables**:
```python
# src/codebase_reviewer/evolution/detector.py
class ObsolescenceDetector:
    def detect_obsolescence(
        self,
        codebase_path: Path,
        tools_dir: Path
    ) -> ObsolescenceReport:
        """Check if tools are still valid for codebase."""
        pass

# src/codebase_reviewer/evolution/learnings.py
class LearningsCapture:
    def capture_learnings(
        self,
        execution_log: Path
    ) -> Learnings:
        """Extract what worked/failed from tool execution."""
        pass

# src/codebase_reviewer/evolution/regenerator.py
class Regenerator:
    def generate_regeneration_prompt(
        self,
        learnings: Learnings,
        obsolescence: ObsolescenceReport
    ) -> str:
        """Create improved Phase 1 prompt with learnings."""
        pass
    
    def regenerate_tools(
        self,
        codebase_path: Path,
        llm_client: LLMClient
    ) -> Phase2Tools:
        """Full regeneration cycle."""
        pass
```

**Test**:
```bash
# Watch mode
review-codebase watch /Users/Matt/GitHub/CallBox \
  --tools-dir /tmp/callbox-tools \
  --check-interval 3600 \
  --auto-regenerate \
  --llm-provider anthropic

# Should:
# - Run tools every hour
# - Detect if codebase changed significantly
# - Trigger regeneration if obsolete
# - Capture learnings
# - Generate improved Gen 2 tools
```

---

## 🧪 VALIDATION CRITERIA

### Success Metrics

1. **LLM Integration**: ✅
   - Can send prompts to Claude API
   - Can extract code from responses
   - 95%+ success rate

2. **Phase 2 Generation**: ✅
   - Tools compile without errors
   - Tools run successfully
   - Tools generate valid output

3. **Fidelity**: ✅
   - Tool output ≥ 95% similar to LLM output
   - All critical information preserved
   - Format and structure match

4. **Self-Evolution**: ✅
   - Detects obsolescence correctly
   - Captures meaningful learnings
   - Gen 2 tools better than Gen 1

5. **End-to-End**: ✅
   - One command does everything
   - No manual intervention needed
   - Works on CallBox codebase

---

## 📅 TIMELINE

| Week | Phase | Deliverable | Test |
|------|-------|-------------|------|
| 1 | LLM Integration | API clients working | Send prompt, get response |
| 2 | Phase 2 Generation | Tools compile and run | Generate tools for CallBox |
| 3 | Validation | Comparison framework | Prove 95%+ fidelity |
| 4 | Self-Evolution | Watch mode working | Detect changes, regenerate |

**Total**: 4 weeks (80-120 hours)

---

## 🚨 SECURITY REQUIREMENTS

### IP Protection (CRITICAL)

```bash
# Add to .gitignore (already done):
/tmp/callbox-*
/tmp/codebase-reviewer/CallBox/
*CallBox*
*callbox*

# Ensure all outputs go to /tmp:
review-codebase evolve /Users/Matt/GitHub/CallBox \
  --output-dir /tmp/callbox-reviewer  # ← MUST be /tmp

# Never commit:
# - Analysis results
# - Generated tools
# - Documentation
# - Prompts containing code snippets
```

### Validation Before Commit

```bash
# Before any git commit:
git status | grep -i callbox && echo "⚠️  STOP! CallBox files detected!"
git diff --cached | grep -i "CallBox\|/Users/Matt" && echo "⚠️  STOP! Proprietary paths!"
```

---

## 🎯 IMMEDIATE NEXT STEP

**Decision Point**: Do you want me to:

**Option A**: Build the full system (4 weeks)
- Implement all 4 phases
- Complete LLM integration
- Achieve the mission

**Option B**: Prototype Phase A first (1 week)
- Just LLM integration
- Prove it works
- Then decide on rest

**Option C**: Manual test first (1 day)
- Use existing Go tool to generate prompt
- Manually send to Claude
- Manually save and compile Phase 2 tools
- Prove the concept works end-to-end
- Then automate

**Recommendation**: **Option C** → **Option B** → **Option A**

Test manually first, then automate incrementally.

