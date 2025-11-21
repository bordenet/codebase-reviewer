# AI Agent Instructions: LLM Prompt Tuning Workflow

**Purpose**: This document provides step-by-step instructions for an AI agent (like Claude) to systematically tune LLM prompts in any project.

**Context**: Based on successful prompt tuning work in the codebase-reviewer project, this workflow has been generalized for use across multiple projects.

**Target Projects**:
- `one-pager`: JavaScript app with markdown prompt templates
- `product-requirements-assistant`: Go/Python app with JSON prompts

---

## Prerequisites

Before starting, ensure you have:
1. ✅ Read `PROMPT_TUNING_PRD.md` (understand the WHY and WHAT)
2. ✅ Read `PROMPT_TUNING_DESIGN_SPEC.md` (understand the HOW)
3. ✅ Access to target project repository on local filesystem
4. ✅ Understanding of project's purpose and use cases

---

## Workflow Overview

```
Phase 0: Analysis → Phase 1: Decouple (if needed) → Phase 2: Generate Test Data
    ↓
Phase 3: Run Simulations → Phase 4: Evaluate Quality → Phase 5: Recommend Improvements
    ↓
Phase 6: Iterate and Validate → Final Report
```

---

## Phase 0: Analysis and Preparation

### Objective
Understand the current state of prompts in the target project.

### Steps

1. **Locate Prompt Files**
   ```bash
   # For one-pager
   cd /Users/matt/GitHub/Personal/one-pager
   ls -la prompts/
   
   # For product-requirements-assistant
   cd /Users/matt/GitHub/Personal/product-requirements-assistant
   find . -name "*prompt*" -o -name "*template*" | grep -v node_modules | grep -v .git
   ```

2. **Read All Prompt Files**
   - For one-pager: Read `prompts/phase1.md`, `prompts/phase2.md`, `prompts/phase3.md`
   - For product-requirements-assistant: Read `web/data/prompts.json`

3. **Analyze Prompt Structure**
   - Identify variable placeholders (e.g., `{projectName}`, `%s`)
   - Understand prompt flow (single-shot vs. multi-phase)
   - Note any special instructions or constraints
   - Document expected output format

4. **Assess Decoupling Status**
   - ✅ one-pager: Already decoupled (separate .md files)
   - ✅ product-requirements-assistant: Already decoupled (prompts.json)
   - If prompts are embedded in code: Plan extraction strategy

5. **Create Baseline Assessment**
   - Document current prompt structure
   - Identify obvious issues (e.g., vague instructions, missing examples)
   - Note any inconsistencies across phases

### Deliverable
Create `analysis_report_{project}.md` documenting findings.

---

## Phase 1: Decouple Prompts (if needed)

### Objective
Separate prompts from code for easier iteration.

### Condition
**SKIP THIS PHASE** for one-pager and product-requirements-assistant (already decoupled).

### Steps (for future projects with embedded prompts)

1. **Extract Prompts**
   - Identify all prompt strings in code
   - Create separate files (JSON, YAML, or Markdown)
   - Maintain variable placeholders

2. **Update Code**
   - Replace hardcoded prompts with file loading
   - Ensure functionality unchanged

3. **Validate**
   - Run existing tests
   - Verify outputs match original

### Deliverable
Decoupled prompt files + updated code.

---

## Phase 2: Generate Test Data

### Objective
Create realistic, diverse test cases that represent real-world usage.

### Steps

1. **Understand Use Cases**
   - Review project README and documentation
   - Identify typical user scenarios
   - Note edge cases and variations

2. **Generate Test Cases**

   **For one-pager** (5-10 test cases):
   - Vary industries: SaaS, e-commerce, healthcare, fintech, manufacturing
   - Vary project types: new feature, redesign, migration, optimization, integration
   - Vary scopes: small (2-4 weeks), medium (2-3 months), large (6+ months)
   - Vary stakeholder complexity: single team, cross-functional, executive-level

   **For product-requirements-assistant** (5-10 test cases):
   - Vary product types: mobile app, web service, API, platform, internal tool
   - Vary complexity: simple feature, complex system, integration, migration
   - Vary audiences: B2B, B2C, internal, partner-facing
   - Vary constraints: legacy system, greenfield, compliance-heavy, performance-critical

3. **Create Test Data File**

   Format: `test_cases_{project}.json`

   ```json
   {
     "project": "one-pager",
     "version": "1.0",
     "test_cases": [
       {
         "id": "test_001",
         "name": "Customer Portal Redesign",
         "description": "Mid-size SaaS company redesigning customer portal",
         "inputs": {
           "projectName": "Customer Portal Redesign",
           "problemStatement": "Current portal has 45% bounce rate, users struggle to find account settings and billing information. Support tickets increased 30% in last quarter due to navigation issues.",
           "proposedSolution": "Redesign portal with user-centered navigation, prominent search, and contextual help. Implement progressive disclosure for advanced features.",
           "keyGoals": "Reduce bounce rate to <20%, decrease support tickets by 40%, improve user satisfaction score from 6.2 to 8.5+",
           "scopeInScope": "Navigation redesign, search implementation, help system, mobile responsiveness",
           "scopeOutOfScope": "Backend API changes, billing system overhaul, third-party integrations",
           "successMetrics": "Bounce rate <20%, support tickets -40%, NPS >8.5, task completion rate >85%",
           "keyStakeholders": "Product Manager (Sarah Chen), Engineering Lead (Mike Rodriguez), UX Designer (Alex Kim), Customer Success VP (Jennifer Park)",
           "timelineEstimate": "12 weeks (2 weeks discovery, 6 weeks development, 4 weeks testing/rollout)"
         },
         "expected_qualities": {
           "clarity": 4,
           "conciseness": 5,
           "completeness": 4,
           "professionalism": 5,
           "actionability": 4
         }
       }
     ]
   }
   ```

4. **Validate Test Data**
   - Ensure all required fields present
   - Check for realistic, non-trivial content
   - Verify diversity across test cases

### Deliverable
`test_cases_{project}.json` with 5-10 comprehensive test cases.

---

## Phase 3: Run Simulations

### Objective
Execute prompts with test data and capture outputs.

### Steps

1. **For Each Test Case**:

   a. **Load Prompt Template**
      - Read prompt file(s)
      - Parse structure and placeholders

   b. **Substitute Variables**
      - Replace placeholders with test data
      - Ensure proper formatting

   c. **Simulate LLM Execution**
      - **YOU (the AI agent) act as the LLM**
      - Follow the prompt instructions exactly
      - Generate realistic output as if you were the production LLM
      - Don't add extra features or improvements (simulate current prompt as-is)

   d. **Capture Output**
      - Store complete generated output
      - Track metadata (timestamp, token counts)

2. **Handle Multi-Phase Workflows**

   **For one-pager**:
   - Phase 1: Generate initial draft
   - Phase 2: Refine draft (use Phase 1 output as input)
   - Phase 3: Final polish (use Phase 2 output as input)

   **For product-requirements-assistant**:
   - Phase 1: Initial PRD draft
   - Phase 2: Refinement (requires Phase 1 output)
   - Phase 3: Comparison with alternative (requires Phase 1 and Phase 2)

3. **Store Results**

   Format: `simulation_results_{project}_original.json`

   ```json
   {
     "project": "one-pager",
     "prompt_version": "original",
     "timestamp": "2025-11-21T08:00:00Z",
     "results": [
       {
         "test_case_id": "test_001",
         "phase_outputs": {
           "phase1": "...",
           "phase2": "...",
           "phase3": "..."
         },
         "metadata": {
           "execution_time_ms": 5000,
           "estimated_tokens": 4500
         }
       }
     ]
   }
   ```

### Deliverable
`simulation_results_{project}_original.json` with all test case outputs.

---

## Phase 4: Evaluate Quality

### Objective
Score outputs against defined quality criteria.

### Steps

1. **Load Quality Rubric**
   - For one-pager: 5 criteria (Clarity, Conciseness, Completeness, Professionalism, Actionability)
   - For product-requirements-assistant: 7 criteria (see PROMPT_TUNING_DESIGN_SPEC.md section 4.2)

2. **Evaluate Each Test Case**

   For each simulation result:
   
   a. **Read the output carefully**
   
   b. **Score each criterion**
      - Use 1-5 scale for scored criteria
      - Use Pass/Fail for binary checks
      - Cite specific examples from output
      - Be objective and consistent

   c. **Document issues**
      - Note specific problems with line/section references
      - Explain why score was given
      - Suggest what would improve the score

3. **Calculate Aggregate Scores**
   - Average score per criterion across all test cases
   - Overall average score
   - Pass rate for binary checks

4. **Identify Patterns**
   - Which criteria consistently score low?
   - Which test cases struggle most?
   - Are there common failure modes?

5. **Create Evaluation Report**

   Format: `evaluation_report_{project}_original.md`

   Use template from PROMPT_TUNING_DESIGN_SPEC.md Appendix A.1

### Deliverable
`evaluation_report_{project}_original.md` with detailed scoring and analysis.

---

## Phase 5: Recommend Improvements

### Objective
Generate specific, actionable prompt improvements based on evaluation results.

### Steps

1. **Analyze Evaluation Results**
   - Review all scores and identified issues
   - Look for patterns across test cases
   - Prioritize by impact (frequency × severity)

2. **Trace Issues to Prompt Structure**
   - For each pattern, identify root cause in prompt
   - Ask: "What in the prompt caused this issue?"
   - Examples:
     - Low clarity → Vague instructions, no examples
     - Low conciseness → No word limit specified
     - Missing sections → Prompt doesn't require them
     - Inconsistency → Phases don't reference each other

3. **Propose Specific Changes**

   For each issue, create a recommendation:

   ```markdown
   ## Recommendation #1: Add Explicit Word Limit

   ### Issue Identified
   Conciseness scores averaged 2.8/5.0 across all test cases. Outputs ranged from 800-2000 words, often exceeding one page.

   ### Root Cause
   Current prompt says "concise one-pager" but doesn't specify word limit or page constraint.

   ### Proposed Change

   **Current Prompt (excerpt)**:
   ```
   Generate a crisp, professional one-pager document based on the information provided.
   ```

   **Improved Prompt (excerpt)**:
   ```
   Generate a crisp, professional one-pager document based on the information provided.

   **CRITICAL CONSTRAINT**: The final document MUST fit on a single page when printed (maximum 600 words).
   Be ruthlessly concise. Every sentence must add value.
   ```

   ### Expected Impact
   - Conciseness: 2.8 → 4.5
   - Affected test cases: All (test_001 through test_010)

   ### Priority: HIGH
   ```

4. **Prioritize Recommendations**
   - **HIGH**: Affects multiple test cases, significant score impact
   - **MEDIUM**: Affects some test cases, moderate score impact
   - **LOW**: Edge cases, minor score impact

5. **Predict Impact**
   - Estimate new scores for each affected criterion
   - Ensure no negative side effects (e.g., clarity vs. conciseness trade-off)

6. **Create Recommendations Document**

   Format: `recommendations_{project}.md`

   Include:
   - Executive summary (top 3-5 recommendations)
   - Detailed recommendations (all issues)
   - Implementation priority order
   - Expected overall score improvement

### Deliverable
`recommendations_{project}.md` with prioritized, specific prompt improvements.

---

## Phase 6: Iterate and Validate

### Objective
Apply improvements, re-test, and verify results.

### Steps

1. **Apply Recommended Changes**
   - Modify prompt files based on recommendations
   - Start with HIGH priority changes
   - Apply one recommendation at a time (or related group)

2. **Re-run Simulations**
   - Use SAME test data from Phase 2
   - Execute prompts with improved versions
   - Capture new outputs
   - Store as `simulation_results_{project}_improved_v1.json`

3. **Re-evaluate Outputs**
   - Use SAME rubric from Phase 4
   - Score new outputs
   - Store as `evaluation_report_{project}_improved_v1.md`

4. **Compare Before/After**

   Create comparison report:

   ```markdown
   # Before/After Comparison: one-pager

   ## Summary

   | Metric | Before | After | Delta |
   |--------|--------|-------|-------|
   | Average Score | 3.2 | 4.1 | +0.9 ✅ |
   | Clarity | 3.5 | 4.3 | +0.8 |
   | Conciseness | 2.8 | 4.5 | +1.7 |
   | Completeness | 3.4 | 3.9 | +0.5 |
   | Professionalism | 3.8 | 4.2 | +0.4 |
   | Actionability | 3.1 | 3.8 | +0.7 |

   ## Test Case Details

   ### test_001: Customer Portal Redesign
   - Before: 3.4/5.0
   - After: 4.2/5.0
   - Delta: +0.8 ✅

   **Key Improvements**:
   - Conciseness: 650 words → 580 words (within limit)
   - Actionability: Added specific metrics with targets
   - Professionalism: Improved formatting consistency

   **Example Output Comparison**:

   **Before (Success Metrics section)**:
   ```
   We will measure success through various metrics including user satisfaction,
   support ticket volume, and overall engagement with the portal.
   ```

   **After (Success Metrics section)**:
   ```
   ## Success Metrics
   - Bounce rate: <20% (current: 45%)
   - Support tickets: -40% reduction
   - NPS score: >8.5 (current: 6.2)
   - Task completion: >85%
   ```
   ```

5. **Validate Improvements**

   Check:
   - ✅ Average score improved by ≥0.5 points
   - ✅ No test case regressed by >0.5 points
   - ✅ All binary checks still passing
   - ✅ Specific issues from evaluation are resolved

6. **Iterate if Needed**
   - If validation fails: Analyze why, adjust recommendations
   - If validation passes but score <4.0: Apply more recommendations
   - If validation passes and score ≥4.0: Proceed to final report

### Deliverable
- `simulation_results_{project}_improved_v1.json`
- `evaluation_report_{project}_improved_v1.md`
- `comparison_report_{project}.md`
- Updated prompt files

---

## Phase 7: Final Report and Handoff

### Objective
Document the complete tuning process and results.

### Steps

1. **Create Executive Summary**

   ```markdown
   # Prompt Tuning Summary: {project}

   **Date**: 2025-11-21
   **Iterations**: {count}
   **Final Score**: {score}/5.0 (up from {baseline})

   ## Key Achievements
   - ✅ Improved average score by {delta} points
   - ✅ All test cases now score ≥{min_score}
   - ✅ {count} specific issues resolved

   ## Changes Applied
   1. {Change 1}: {brief description}
   2. {Change 2}: {brief description}
   3. {Change 3}: {brief description}

   ## Recommendations for Future
   - {Recommendation 1}
   - {Recommendation 2}
   ```

2. **Organize Artifacts**

   Create directory structure:
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
       ├── phase1.md (or prompts.json)
       ├── phase2.md
       └── phase3.md
   ```

3. **Document Lessons Learned**

   ```markdown
   ## Lessons Learned: {project}

   ### What Worked Well
   - {Insight 1}
   - {Insight 2}

   ### Challenges Encountered
   - {Challenge 1}: {How resolved}
   - {Challenge 2}: {How resolved}

   ### Recommendations for Next Project
   - {Recommendation 1}
   - {Recommendation 2}
   ```

4. **Create Handoff Checklist**

   ```markdown
   ## Handoff Checklist

   - [ ] All test cases passing with score ≥4.0
   - [ ] Updated prompt files reviewed
   - [ ] Comparison report shows clear improvements
   - [ ] No regressions identified
   - [ ] Documentation complete
   - [ ] Artifacts organized and accessible
   - [ ] Lessons learned documented
   ```

### Deliverable
Complete `prompt_tuning_results_{project}/` directory with all artifacts.

---

## Critical Success Factors

### 1. Objectivity in Evaluation
- **DO**: Score based on rubric, cite specific examples
- **DON'T**: Inflate scores or be overly lenient

### 2. Realism in Simulation
- **DO**: Generate outputs that match real-world LLM quality
- **DON'T**: Generate perfect outputs that no LLM could produce

### 3. Specificity in Recommendations
- **DO**: Provide exact wording changes with before/after
- **DON'T**: Give vague advice like "make it clearer"

### 4. Consistency Across Test Cases
- **DO**: Apply same standards to all test cases
- **DON'T**: Be stricter on some test cases than others

### 5. Focus on Root Causes
- **DO**: Fix underlying prompt issues
- **DON'T**: Just tweak outputs manually

---

## Quality Gates

Before proceeding to next phase, verify:

**After Phase 2 (Test Data)**:
- [ ] 5-10 diverse, realistic test cases created
- [ ] All required input fields populated
- [ ] Test cases cover different scenarios/industries/complexities

**After Phase 3 (Simulation)**:
- [ ] All test cases executed successfully
- [ ] Outputs captured for all phases
- [ ] Outputs are realistic (not perfect, not terrible)

**After Phase 4 (Evaluation)**:
- [ ] All test cases scored using rubric
- [ ] Specific issues documented with examples
- [ ] Aggregate scores calculated
- [ ] Patterns identified

**After Phase 5 (Recommendations)**:
- [ ] At least 3-5 specific recommendations created
- [ ] Each recommendation has before/after examples
- [ ] Recommendations prioritized by impact
- [ ] Expected score improvements estimated

**After Phase 6 (Validation)**:
- [ ] Average score improved by ≥0.5 points
- [ ] No regressions >0.5 points
- [ ] Target score ≥4.0 achieved
- [ ] Comparison report shows clear improvements

---

## Example Execution Timeline

**For one-pager** (estimated 2-3 hours):
- Phase 0: 15 minutes (read prompts, analyze structure)
- Phase 1: SKIP (already decoupled)
- Phase 2: 30 minutes (generate 5-10 test cases)
- Phase 3: 45 minutes (run simulations for all test cases × 3 phases)
- Phase 4: 45 minutes (evaluate all outputs)
- Phase 5: 30 minutes (create recommendations)
- Phase 6: 45 minutes (apply changes, re-test, validate)
- Phase 7: 15 minutes (final report)

**For product-requirements-assistant** (estimated 2-3 hours):
- Similar timeline, potentially longer due to more complex 3-phase workflow

---

## Final Checklist

Before declaring the work complete:

- [ ] Read PROMPT_TUNING_PRD.md ✅
- [ ] Read PROMPT_TUNING_DESIGN_SPEC.md ✅
- [ ] Completed Phase 0: Analysis ✅
- [ ] Completed Phase 1: Decouple (or skipped if N/A) ✅
- [ ] Completed Phase 2: Test Data Generation ✅
- [ ] Completed Phase 3: Simulation Execution ✅
- [ ] Completed Phase 4: Quality Evaluation ✅
- [ ] Completed Phase 5: Improvement Recommendations ✅
- [ ] Completed Phase 6: Iteration and Validation ✅
- [ ] Completed Phase 7: Final Report ✅
- [ ] Average score ≥4.0 achieved ✅
- [ ] No regressions identified ✅
- [ ] All artifacts organized ✅
- [ ] Ready for human review ✅

---

## Getting Started

To begin prompt tuning for a project, say:

> "I'm ready to tune LLM prompts for [one-pager / product-requirements-assistant]. I've read the PRD and design spec. Let's start with Phase 0: Analysis."

The AI agent will then guide you through each phase systematically.

---

**End of Instructions**



