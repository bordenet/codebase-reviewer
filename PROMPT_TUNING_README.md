# Generalized LLM Prompt Tuning System

**Version**: 1.0  
**Date**: 2025-11-21  
**Status**: Ready for Use

---

## Overview

This directory contains a **complete, generalized system for systematically tuning LLM prompts** across multiple projects. The system enables AI agents (like Claude) to improve prompt quality through simulation, evaluation, and iterative refinement—without requiring real LLM API calls during the tuning process.

**Key Innovation**: The AI agent acts as BOTH the prompt executor AND the evaluator, creating a tight feedback loop for rapid improvement.

**Proven Success**: This approach was successfully used in the codebase-reviewer project to improve 19 prompts from minimal/fake context to production-ready quality with rich, accurate data.

---

## Target Projects

This system is designed for:

1. **one-pager** (`/Users/matt/GitHub/Personal/one-pager`)
   - JavaScript app with markdown prompt templates
   - 3-phase workflow for generating business one-pagers
   - Already decoupled (prompts in separate .md files)

2. **product-requirements-assistant** (`/Users/matt/GitHub/Personal/product-requirements-assistant`)
   - Go/Python app with JSON prompts
   - 3-phase workflow for generating comprehensive PRDs
   - Already decoupled (prompts in prompts.json)

---

## Documentation Structure

### 📋 Start Here

**[QUICK_START_PROMPT_TUNING.md](QUICK_START_PROMPT_TUNING.md)** (5 min read)
- Get started in 5 minutes
- Understand the workflow at a glance
- See example improvements

### 📖 Core Documentation

1. **[PROMPT_TUNING_PRD.md](PROMPT_TUNING_PRD.md)** (10 min read)
   - **WHY**: Problem statement and business context
   - **WHAT**: Solution overview and success criteria
   - **WHO**: Stakeholders and target users
   - **WHEN**: Timeline and dependencies

2. **[PROMPT_TUNING_DESIGN_SPEC.md](PROMPT_TUNING_DESIGN_SPEC.md)** (20 min read)
   - **HOW**: Detailed technical design
   - **Architecture**: System components and workflow
   - **Project Configs**: Specific settings for one-pager and product-requirements-assistant
   - **Quality Rubrics**: Detailed evaluation criteria
   - **Report Templates**: Output formats

3. **[AI_AGENT_PROMPT_TUNING_INSTRUCTIONS.md](AI_AGENT_PROMPT_TUNING_INSTRUCTIONS.md)** (30 min read)
   - **Step-by-step workflow**: Complete instructions for AI agent
   - **Phase-by-phase guide**: From analysis to final report
   - **Quality gates**: Checkpoints for each phase
   - **Examples**: Concrete examples of each step

---

## Quick Start

### 1. Read the Documentation (30 minutes)

```bash
# Quick overview
cat QUICK_START_PROMPT_TUNING.md

# Understand WHY and WHAT
cat PROMPT_TUNING_PRD.md

# Understand HOW
cat PROMPT_TUNING_DESIGN_SPEC.md

# Get step-by-step instructions
cat AI_AGENT_PROMPT_TUNING_INSTRUCTIONS.md
```

### 2. Choose a Project

**Recommended for first time**: Start with `one-pager` (simpler, faster)

### 3. Start the Workflow

Say to your AI agent (Claude):

> "I'm ready to tune LLM prompts for one-pager. I've read the PRD and design spec. Let's start with Phase 0: Analysis."

The AI agent will guide you through all 7 phases.

---

## Workflow Overview

```
Phase 0: Analysis
    ↓
Phase 1: Decouple Prompts (if needed)
    ↓
Phase 2: Generate Test Data
    ↓
Phase 3: Run Simulations
    ↓
Phase 4: Evaluate Quality
    ↓
Phase 5: Recommend Improvements
    ↓
Phase 6: Iterate and Validate
    ↓
Phase 7: Final Report
```

**Total Time**: ~2-3 hours per project

---

## Expected Results

### Quantitative Improvements

- **Average quality score**: 3.0-3.5 → 4.0+ (out of 5.0)
- **Score improvement**: ≥0.5 points across all criteria
- **Test case pass rate**: 100% (no regressions)

### Qualitative Improvements

- **Clarity**: Prompts produce clearer, more understandable outputs
- **Consistency**: Outputs more consistent across test cases
- **Completeness**: All required sections/elements present
- **Actionability**: Outputs more useful for end users

### Artifacts Generated

```
prompt_tuning_results_{project}/
├── test_cases_{project}.json
├── simulation_results_{project}_original.json
├── simulation_results_{project}_improved_v1.json
├── evaluation_report_{project}_original.md
├── evaluation_report_{project}_improved_v1.md
├── recommendations_{project}.md
├── comparison_report_{project}.md
├── executive_summary_{project}.md
└── updated_prompts/
    └── [improved prompt files]
```

---

## Key Features

### ✅ Simulation-Based Testing
- No real LLM API calls needed during tuning
- AI agent simulates LLM responses
- Fast iteration cycles

### ✅ Objective Evaluation
- Structured quality rubrics (1-5 scale)
- Specific, measurable criteria
- Consistent scoring across test cases

### ✅ Data-Driven Improvements
- 5-10 realistic test cases per project
- Before/after comparisons
- Quantified impact predictions

### ✅ Actionable Recommendations
- Specific prompt changes with before/after examples
- Prioritized by impact (HIGH/MEDIUM/LOW)
- Expected score improvements estimated

### ✅ Validation and Iteration
- Re-test with same data after changes
- Verify improvements, catch regressions
- Iterate until target score achieved

---

## Quality Criteria

### one-pager (5 criteria)

1. **Clarity** (1-5): Easy to understand?
2. **Conciseness** (1-5): Fits on one page?
3. **Completeness** (1-5): All sections present?
4. **Professionalism** (1-5): Executive-ready?
5. **Actionability** (1-5): Clear next steps and metrics?

**Target**: 4.0+ average

### product-requirements-assistant (7 criteria)

1. **Comprehensiveness** (1-5): Covers all aspects?
2. **Clarity** (1-5): Requirements unambiguous?
3. **Structure** (1-5): Proper section numbering?
4. **Consistency** (1-5): Aligned across 3 phases?
5. **Engineering-Ready** (1-5): Avoids "how", focuses on "why" and "what"?
6. **No Metadata Table** (Pass/Fail): Follows user requirement?
7. **Section Numbering** (Pass/Fail): ## and ### levels numbered?

**Target**: 4.0+ average, 100% pass on binary checks

---

## Success Criteria

Before declaring the work complete:

- ✅ Average score ≥4.0 across all test cases
- ✅ No regressions (no test case dropped >0.5 points)
- ✅ All binary checks passing (if applicable)
- ✅ Specific issues from baseline evaluation resolved
- ✅ Before/after comparison shows clear improvements
- ✅ All artifacts generated and organized
- ✅ Documentation complete

---

## Lessons from codebase-reviewer

This system is based on successful prompt tuning work in the codebase-reviewer project:

### What Worked Well

1. **Tight Feedback Loop**: Simulation → Evaluation → Improvement → Re-test
2. **AI-as-Evaluator**: No human bottleneck during iteration
3. **Structured Rubrics**: Clear, measurable quality criteria
4. **Specific Recommendations**: Exact prompt changes, not vague advice
5. **Comparative Analysis**: Always show before/after

### Key Improvements Achieved

- **Architecture Validation**: Fake data → Real codebase structure
- **Call Graph**: External deps → Internal module dependencies
- **Git Hotspots**: Wrong context → Actual commit history
- **Observability**: Minimal data → Comprehensive logging analysis
- **Structured Output**: Generic → Industry-standard formats (OWASP, CWE)

**Result**: 19 prompts improved from 32% "working well" to production-ready quality

---

## Next Steps

1. ✅ Read `QUICK_START_PROMPT_TUNING.md` (5 min)
2. ✅ Read `PROMPT_TUNING_PRD.md` (10 min)
3. ✅ Read `PROMPT_TUNING_DESIGN_SPEC.md` (20 min)
4. ✅ Read `AI_AGENT_PROMPT_TUNING_INSTRUCTIONS.md` (30 min)
5. ⏳ Start tuning `one-pager` prompts
6. ⏳ Start tuning `product-requirements-assistant` prompts
7. ⏳ Document lessons learned for future projects

---

## Contributing

This system is designed to be generalized for any project with LLM prompts. If you use it for other projects:

1. Document project-specific configurations
2. Share quality rubrics that worked well
3. Contribute improvements to the workflow
4. Report issues or edge cases

---

## License

Same as parent project (codebase-reviewer).

---

**Ready to improve your LLM prompts? Start with [QUICK_START_PROMPT_TUNING.md](QUICK_START_PROMPT_TUNING.md)!** 🚀

