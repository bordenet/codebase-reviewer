# Quick Start: LLM Prompt Tuning

**Purpose**: Get started tuning LLM prompts in 5 minutes.

---

## What This Is

A **generalized system for systematically improving LLM prompts** using AI-as-evaluator simulation. No real API calls needed during tuning.

**Based on**: Successful work in codebase-reviewer project where prompts improved from minimal context to production-ready quality.

**Target Projects**:
- `one-pager`: JavaScript app with markdown prompt templates
- `product-requirements-assistant`: Go/Python app with JSON prompts

---

## How It Works

```
1. Read existing prompts
2. Generate realistic test data
3. Simulate LLM responses (AI agent acts as LLM)
4. Evaluate outputs using quality rubric
5. Recommend specific improvements
6. Apply changes and validate
```

**Key Insight**: The AI agent (Claude) acts as BOTH the prompt executor AND the evaluator, creating a tight feedback loop.

---

## Quick Start (3 Steps)

### Step 1: Read the Documentation (5 minutes)

1. **PRD** (`PROMPT_TUNING_PRD.md`): Understand WHY and WHAT
2. **Design Spec** (`PROMPT_TUNING_DESIGN_SPEC.md`): Understand HOW
3. **AI Instructions** (`AI_AGENT_PROMPT_TUNING_INSTRUCTIONS.md`): Step-by-step workflow

### Step 2: Choose Your Project

**Option A: one-pager**
- Simpler (3 markdown files)
- Faster to tune (~2 hours)
- Good for learning the workflow

**Option B: product-requirements-assistant**
- More complex (3-phase workflow)
- Longer to tune (~3 hours)
- More comprehensive example

### Step 3: Start the Workflow

Say to the AI agent:

> "I'm ready to tune LLM prompts for [one-pager / product-requirements-assistant]. I've read the PRD and design spec. Let's start with Phase 0: Analysis."

The AI agent will guide you through all phases.

---

## What You'll Get

### Artifacts Generated

```
prompt_tuning_results_{project}/
├── test_cases_{project}.json              # 5-10 realistic test scenarios
├── simulation_results_original.json       # Baseline outputs
├── simulation_results_improved.json       # Improved outputs
├── evaluation_report_original.md          # Baseline scores
├── evaluation_report_improved.md          # Improved scores
├── recommendations_{project}.md           # Specific improvements
├── comparison_report_{project}.md         # Before/after analysis
├── executive_summary_{project}.md         # High-level summary
└── updated_prompts/                       # Improved prompt files
```

### Expected Results

- **Average quality score**: 3.0-3.5 → 4.0+ (out of 5.0)
- **Specific improvements**: Clarity, conciseness, completeness, consistency
- **Actionable recommendations**: Exact prompt changes with before/after examples

---

## Quality Criteria

### For one-pager (5 criteria, 1-5 scale)

1. **Clarity**: Easy to understand?
2. **Conciseness**: Fits on one page?
3. **Completeness**: All sections present?
4. **Professionalism**: Executive-ready?
5. **Actionability**: Clear next steps and metrics?

**Target**: 4.0+ average

### For product-requirements-assistant (7 criteria)

1. **Comprehensiveness**: Covers all aspects?
2. **Clarity**: Requirements unambiguous?
3. **Structure**: Proper section numbering?
4. **Consistency**: Aligned across 3 phases?
5. **Engineering-Ready**: Avoids "how", focuses on "why" and "what"?
6. **No Metadata Table**: Pass/Fail
7. **Section Numbering**: Pass/Fail

**Target**: 4.0+ average, 100% pass on binary checks

---

## Example: What Gets Improved

### Before (Low Conciseness Score)

**Prompt**:
```
Generate a crisp, professional one-pager document.
```

**Output**: 1,200 words (too long!)

### After (High Conciseness Score)

**Prompt**:
```
Generate a crisp, professional one-pager document.

**CRITICAL CONSTRAINT**: The final document MUST fit on a single page
when printed (maximum 600 words). Be ruthlessly concise.
```

**Output**: 580 words ✅

---

## Timeline

- **Phase 0**: Analysis (15 min)
- **Phase 1**: Decouple (SKIP - already done)
- **Phase 2**: Generate test data (30 min)
- **Phase 3**: Run simulations (45 min)
- **Phase 4**: Evaluate quality (45 min)
- **Phase 5**: Recommend improvements (30 min)
- **Phase 6**: Iterate and validate (45 min)
- **Phase 7**: Final report (15 min)

**Total**: ~2-3 hours per project

---

## Success Criteria

Before declaring success:

- ✅ Average score ≥4.0 across all test cases
- ✅ No regressions (no test case dropped >0.5 points)
- ✅ All binary checks passing (if applicable)
- ✅ Specific issues from baseline evaluation resolved
- ✅ Before/after comparison shows clear improvements

---

## Key Principles

1. **AI-as-Evaluator**: AI judges quality (no human in loop during tuning)
2. **Simulation-First**: Test without real API calls
3. **Data-Driven**: Use realistic test cases, not toy examples
4. **Comparative Analysis**: Always compare before/after
5. **Structured Evaluation**: Clear, measurable criteria

---

## Common Pitfalls to Avoid

❌ **Don't**: Generate perfect outputs during simulation (unrealistic)
✅ **Do**: Generate realistic outputs that match real LLM quality

❌ **Don't**: Inflate scores to make results look good
✅ **Do**: Be objective and critical based on rubric

❌ **Don't**: Give vague recommendations like "make it clearer"
✅ **Do**: Provide exact wording changes with before/after examples

❌ **Don't**: Test with trivial examples
✅ **Do**: Use realistic, diverse test cases

❌ **Don't**: Fix outputs manually
✅ **Do**: Fix underlying prompt issues

---

## Next Steps

1. **Read the PRD**: `PROMPT_TUNING_PRD.md` (5 min)
2. **Read the Design Spec**: `PROMPT_TUNING_DESIGN_SPEC.md` (15 min)
3. **Read AI Instructions**: `AI_AGENT_PROMPT_TUNING_INSTRUCTIONS.md` (10 min)
4. **Start tuning**: Say "I'm ready to tune LLM prompts for [project]"

---

## Questions?

Refer to:
- **Why/What**: `PROMPT_TUNING_PRD.md`
- **How**: `PROMPT_TUNING_DESIGN_SPEC.md`
- **Step-by-step**: `AI_AGENT_PROMPT_TUNING_INSTRUCTIONS.md`

---

**Ready to start? Pick a project and let's go!** 🚀
