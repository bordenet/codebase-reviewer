# Design Specification: Generalized LLM Prompt Tuning System

**Version**: 1.0
**Date**: 2025-11-21
**Related**: PROMPT_TUNING_PRD.md

---

## 1. System Overview

### 1.1 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent (Claude)                        │
│  - Reads existing prompts                                   │
│  - Generates test data                                      │
│  - Simulates prompt execution                               │
│  - Evaluates output quality                                 │
│  - Recommends improvements                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Tuning Workflow                           │
│  1. Analyze existing prompts                                │
│  2. Decouple from code (if needed)                          │
│  3. Generate test data                                      │
│  4. Run simulations                                         │
│  5. Evaluate results                                        │
│  6. Iterate and improve                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Output Artifacts                           │
│  - Improved prompt files                                    │
│  - Evaluation reports                                       │
│  - Before/after comparisons                                 │
│  - Recommendations document                                 │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Core Components

1. **Prompt Analyzer**: Examines existing prompts and their structure
2. **Test Data Generator**: Creates realistic input scenarios
3. **Simulation Engine**: Executes prompts with test data
4. **Quality Evaluator**: Scores outputs against defined criteria
5. **Improvement Engine**: Suggests specific prompt enhancements
6. **Report Generator**: Produces human-readable analysis

---

## 2. Project-Specific Configurations

### 2.1 one-pager Project

**Current State**:
- **Location**: `/Users/matt/GitHub/Personal/one-pager/prompts/`
- **Format**: Markdown files (phase1.md, phase2.md, phase3.md)
- **Language**: JavaScript (frontend)
- **Prompt Structure**: Template strings with `{variable}` placeholders
- **Use Case**: Generate concise one-page business documents

**Prompt Decoupling Status**: ✅ Already decoupled (separate .md files)

**Test Data Requirements**:
- Project names (e.g., "Customer Portal Redesign", "API Gateway Migration")
- Problem statements (2-3 sentences)
- Proposed solutions (3-4 sentences)
- Key goals/benefits (3-5 bullet points)
- Scope items (in-scope and out-of-scope)
- Success metrics (quantifiable KPIs)
- Stakeholders (roles and names)
- Timeline estimates (weeks/months)

**Quality Criteria**:
1. **Clarity** (1-5): Is the one-pager easy to understand?
2. **Conciseness** (1-5): Is it truly one page? No fluff?
3. **Completeness** (1-5): Are all sections present and meaningful?
4. **Professionalism** (1-5): Appropriate tone and formatting?
5. **Actionability** (1-5): Clear next steps and success metrics?

**Target Score**: 4.0+ average across all criteria

### 2.2 product-requirements-assistant Project

**Current State**:
- **Location**: `/Users/matt/GitHub/Personal/product-requirements-assistant/web/data/prompts.json`
- **Format**: JSON object with numbered keys ("1", "2", "3")
- **Language**: Go (backend), Python (scripts)
- **Prompt Structure**: String templates with `%s` placeholders
- **Use Case**: Generate comprehensive PRDs through 3-phase workflow

**Prompt Decoupling Status**: ✅ Already decoupled (prompts.json)

**Test Data Requirements**:
- PRD titles (e.g., "Mobile App Offline Mode", "Real-time Collaboration Feature")
- Problem descriptions (business context, user pain points)
- Context/considerations (technical constraints, business requirements)
- Phase 1 output (initial PRD draft)
- Phase 2 output (refined PRD)

**Quality Criteria**:
1. **Comprehensiveness** (1-5): Does PRD cover all necessary aspects?
2. **Clarity** (1-5): Are requirements unambiguous?
3. **Structure** (1-5): Proper section numbering and organization?
4. **Consistency** (1-5): Aligned across 3-phase workflow?
5. **Engineering-Ready** (1-5): Avoids "how", focuses on "why" and "what"?
6. **No Metadata Table** (Pass/Fail): Follows user's explicit requirement?
7. **Section Numbering** (Pass/Fail): ## and ### levels numbered?

**Target Score**: 4.0+ average across scored criteria, Pass on all binary checks

---

## 3. Detailed Workflow

### 3.1 Phase 0: Analysis and Preparation

**Inputs**: Project repository path

**Steps**:
1. Locate prompt files (prompts/*.md or web/data/prompts.json)
2. Parse prompt structure and identify variables
3. Understand prompt flow (single-shot vs. multi-phase)
4. Identify any code coupling (prompts embedded in .js/.go files)
5. Document current prompt format and structure

**Outputs**:
- Prompt inventory document
- Variable/placeholder catalog
- Coupling assessment
- Baseline quality assessment

### 3.2 Phase 1: Decoupling (if needed)

**Condition**: Only if prompts are embedded in code

**Steps**:
1. Extract prompts to separate files
2. Create configuration format (JSON, YAML, or Markdown)
3. Update code to load prompts from files
4. Verify functionality unchanged

**Outputs**:
- Decoupled prompt files
- Updated code with file loading
- Migration documentation

**Note**: Both target projects already have decoupled prompts, so this phase can be skipped.

### 3.3 Phase 2: Test Data Generation

**Objective**: Create realistic, diverse test cases

**For one-pager**:
Generate 5-10 test scenarios covering:
- Different industries (SaaS, e-commerce, healthcare, fintech)
- Different project types (new feature, redesign, migration, optimization)
- Different scopes (small, medium, large)
- Different stakeholder configurations

**For product-requirements-assistant**:
Generate 5-10 test scenarios covering:
- Different product types (mobile app, web service, API, platform)
- Different complexity levels (simple feature, complex system, integration)
- Different audiences (B2B, B2C, internal tools)
- Different technical constraints (legacy system, greenfield, migration)

**Output Format**:
```json
{
  "test_cases": [
    {
      "id": "test_001",
      "name": "Customer Portal Redesign",
      "inputs": {
        "projectName": "Customer Portal Redesign",
        "problemStatement": "...",
        "proposedSolution": "...",
        ...
      },
      "expected_qualities": {
        "clarity": 4,
        "conciseness": 5,
        ...
      }
    }
  ]
}
```

### 3.4 Phase 3: Simulation Execution

**Objective**: Run prompts with test data and capture outputs

**Process**:
1. For each test case:
   - Load prompt template
   - Substitute variables with test data
   - Simulate LLM execution (AI agent acts as the LLM)
   - Capture generated output
   - Store for evaluation

**For one-pager**:
- Execute all 3 phases sequentially (phase1 → phase2 → phase3)
- Each phase builds on previous output
- Final output is the polished one-pager

**For product-requirements-assistant**:
- Execute 3-phase workflow:
  - Phase 1: Initial PRD draft
  - Phase 2: Refinement (requires Phase 1 output as input)
  - Phase 3: Comparison with alternative (requires both Phase 1 and Phase 2)
- Track outputs at each phase

**Output Format**:
```json
{
  "simulation_results": [
    {
      "test_case_id": "test_001",
      "prompt_version": "original",
      "phase_outputs": {
        "phase1": "...",
        "phase2": "...",
        "phase3": "..."
      },
      "execution_metadata": {
        "timestamp": "2025-11-21T07:45:00Z",
        "prompt_tokens": 1500,
        "completion_tokens": 3000
      }
    }
  ]
}
```

### 3.5 Phase 4: Quality Evaluation

**Objective**: Score outputs against defined criteria

**Evaluation Process**:
1. For each simulation result:
   - Apply quality criteria rubric
   - Score each criterion (1-5 or Pass/Fail)
   - Calculate aggregate score
   - Identify specific weaknesses
   - Document examples of issues

**Evaluation Rubric Template**:

```markdown
## Evaluation: Test Case {id}

### Criterion 1: {Name} (Score: {1-5})
- **Definition**: {What this measures}
- **Score**: {1-5}
- **Rationale**: {Why this score}
- **Examples**: {Specific instances from output}

### Criterion 2: {Name} (Score: {1-5})
...

### Overall Score: {average}

### Key Strengths:
- {Strength 1}
- {Strength 2}

### Key Weaknesses:
- {Weakness 1}
- {Weakness 2}

### Specific Issues:
1. {Issue with line/section reference}
2. {Issue with line/section reference}
```

**Aggregation**:
- Calculate average score across all test cases
- Identify patterns (e.g., "Clarity consistently low")
- Rank issues by frequency and severity

### 3.6 Phase 5: Improvement Recommendations

**Objective**: Generate specific, actionable prompt improvements

**Analysis Process**:
1. Review all evaluation results
2. Identify common failure patterns
3. Trace failures back to prompt structure/wording
4. Propose specific changes to prompts
5. Predict impact of each change

**Recommendation Format**:

```markdown
## Improvement Recommendation #{n}

### Issue Identified
{Description of the problem}

### Root Cause
{Why the current prompt produces this issue}

### Proposed Change
**Current Prompt (excerpt)**:
```
{relevant section of current prompt}
```

**Improved Prompt (excerpt)**:
```
{proposed new version}
```

### Expected Impact
- {Criterion 1}: {current score} → {expected score}
- {Criterion 2}: {current score} → {expected score}

### Affected Test Cases
- test_001: {specific improvement}
- test_003: {specific improvement}

### Priority: {High/Medium/Low}
```

### 3.7 Phase 6: Iteration and Validation

**Objective**: Apply improvements and verify results

**Process**:
1. Apply recommended prompt changes
2. Re-run simulations with same test data
3. Re-evaluate outputs
4. Compare before/after scores
5. Verify improvements (no regressions)
6. Iterate if needed

**Validation Criteria**:
- ✅ Average score improved by ≥0.5 points
- ✅ No test case regressed by >0.5 points
- ✅ All binary checks (Pass/Fail) still passing
- ✅ Specific issues documented in evaluation are resolved

**Output**: Before/After Comparison Report

---

## 4. Evaluation Criteria Details

### 4.1 one-pager Quality Rubric

#### Clarity (1-5)
- **5**: Crystal clear, no ambiguity, anyone can understand
- **4**: Clear with minor ambiguities
- **3**: Mostly clear but some confusing sections
- **2**: Significant clarity issues
- **1**: Confusing and hard to understand

#### Conciseness (1-5)
- **5**: Perfectly concise, every word counts, fits on one page
- **4**: Mostly concise with minor verbosity
- **3**: Some unnecessary content but still one page
- **2**: Verbose, struggles to fit on one page
- **1**: Way too long, multiple pages

#### Completeness (1-5)
- **5**: All required sections present and meaningful
- **4**: All sections present, one minor gap
- **3**: Missing one section or several sections shallow
- **2**: Multiple missing or incomplete sections
- **1**: Severely incomplete

#### Professionalism (1-5)
- **5**: Executive-ready, perfect tone and formatting
- **4**: Professional with minor formatting issues
- **3**: Acceptable but not polished
- **2**: Unprofessional tone or poor formatting
- **1**: Inappropriate for business use

#### Actionability (1-5)
- **5**: Crystal clear next steps and measurable success metrics
- **4**: Clear next steps, minor gaps in metrics
- **3**: Some actionable items but vague
- **2**: Mostly vague, hard to act on
- **1**: No clear actions or metrics

### 4.2 product-requirements-assistant Quality Rubric

#### Comprehensiveness (1-5)
- **5**: Covers all aspects: problem, solution, requirements, success metrics, risks
- **4**: Covers most aspects, one minor gap
- **3**: Covers core aspects but missing important details
- **2**: Significant gaps in coverage
- **1**: Severely incomplete

#### Clarity (1-5)
- **5**: All requirements unambiguous, engineering team can implement directly
- **4**: Mostly clear, minor ambiguities
- **3**: Some ambiguous requirements
- **2**: Many ambiguous requirements
- **1**: Highly ambiguous, unusable

#### Structure (1-5)
- **5**: Perfect section numbering, logical flow, easy to navigate
- **4**: Good structure, minor numbering issues
- **3**: Acceptable structure but some disorganization
- **2**: Poor structure, hard to navigate
- **1**: No clear structure

#### Consistency (1-5)
- **5**: Perfectly aligned across all 3 phases, no contradictions
- **4**: Mostly consistent, one minor contradiction
- **3**: Some inconsistencies between phases
- **2**: Multiple contradictions
- **1**: Severely inconsistent

#### Engineering-Ready (1-5)
- **5**: Focuses purely on "why" and "what", zero "how"
- **4**: Mostly avoids "how", one minor slip
- **3**: Some implementation details leaked in
- **2**: Significant "how" content
- **1**: Reads like a technical spec, not a PRD

#### No Metadata Table (Pass/Fail)
- **Pass**: No metadata table at top of document
- **Fail**: Metadata table present (violates user requirement)

#### Section Numbering (Pass/Fail)
- **Pass**: ## and ### levels properly numbered
- **Fail**: Missing or incorrect section numbering

---

## 5. Implementation Checklist

### 5.1 For one-pager

- [ ] Read all 3 prompt files (phase1.md, phase2.md, phase3.md)
- [ ] Generate 5-10 diverse test cases
- [ ] Run simulations for each test case (all 3 phases)
- [ ] Evaluate outputs using 5-criterion rubric
- [ ] Calculate aggregate scores
- [ ] Identify improvement opportunities
- [ ] Recommend specific prompt changes
- [ ] Apply changes and re-test
- [ ] Generate before/after comparison report

### 5.2 For product-requirements-assistant

- [ ] Read prompts.json (3 prompts)
- [ ] Generate 5-10 diverse test cases
- [ ] Run simulations for each test case (3-phase workflow)
- [ ] Evaluate outputs using 7-criterion rubric
- [ ] Calculate aggregate scores
- [ ] Identify improvement opportunities
- [ ] Recommend specific prompt changes
- [ ] Apply changes and re-test
- [ ] Generate before/after comparison report

---

## 6. Output Artifacts

### 6.1 Required Deliverables

1. **Test Data File**: `test_cases_{project}.json`
2. **Simulation Results**: `simulation_results_{project}_{version}.json`
3. **Evaluation Report**: `evaluation_report_{project}_{version}.md`
4. **Improvement Recommendations**: `recommendations_{project}.md`
5. **Before/After Comparison**: `comparison_report_{project}.md`
6. **Updated Prompts**: Modified prompt files with improvements

### 6.2 Report Templates

See Appendix A for detailed report templates.

---

## 7. Success Metrics

### 7.1 Quantitative Metrics

- **Average Quality Score**: Target ≥4.0 (up from baseline)
- **Improvement Delta**: Target ≥0.5 points increase
- **Test Case Pass Rate**: Target 100% (no regressions)
- **Binary Checks**: Target 100% pass rate

### 7.2 Qualitative Metrics

- **Prompt Clarity**: Are prompts easier to understand?
- **Output Consistency**: Are outputs more consistent across test cases?
- **Actionability**: Are outputs more useful for end users?

---

## 8. Appendix A: Report Templates

### A.1 Evaluation Report Template

```markdown
# Prompt Evaluation Report: {project}

**Version**: {original/improved}
**Date**: {timestamp}
**Test Cases**: {count}

## Executive Summary

- **Average Score**: {score}/5.0
- **Pass Rate**: {percentage}%
- **Key Strengths**: {list}
- **Key Weaknesses**: {list}

## Detailed Results

### Test Case: {id} - {name}

#### Input Summary
- {key input 1}: {value}
- {key input 2}: {value}

#### Output Summary
{brief description of generated output}

#### Quality Scores
| Criterion | Score | Notes |
|-----------|-------|-------|
| {Criterion 1} | {score}/5 | {rationale} |
| {Criterion 2} | {score}/5 | {rationale} |

#### Specific Issues
1. {Issue description with reference}
2. {Issue description with reference}

---

## Aggregate Analysis

### Score Distribution
{chart or table showing score distribution}

### Common Patterns
- **Strength**: {pattern observed across multiple test cases}
- **Weakness**: {pattern observed across multiple test cases}

### Recommendations
{high-level recommendations for improvement}
```

### A.2 Comparison Report Template

```markdown
# Before/After Comparison: {project}

**Date**: {timestamp}
**Test Cases**: {count}

## Summary

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Average Score | {score} | {score} | {+/-delta} |
| Pass Rate | {%} | {%} | {+/-delta} |
| {Criterion 1} Avg | {score} | {score} | {+/-delta} |
| {Criterion 2} Avg | {score} | {score} | {+/-delta} |

## Improvements

### Test Case: {id}

**Before Score**: {score}/5.0
**After Score**: {score}/5.0
**Delta**: {+delta}

**Key Improvements**:
- {Criterion}: {before} → {after} ({reason})
- {Criterion}: {before} → {after} ({reason})

**Example Output Comparison**:

**Before**:
```
{excerpt from original output showing issue}
```

**After**:
```
{excerpt from improved output showing fix}
```

---

## Regressions (if any)

{List any test cases that scored lower after changes}

---

## Conclusion

{Summary of overall improvement and recommendations for next steps}
```

---

## 9. AI Agent Instructions

### 9.1 Self-Evaluation Guidelines

When acting as the evaluator, the AI agent should:

1. **Be Objective**: Score based on rubric, not personal preference
2. **Be Specific**: Cite exact examples from outputs
3. **Be Consistent**: Apply same standards across all test cases
4. **Be Critical**: Don't inflate scores; identify real issues
5. **Be Constructive**: Suggest specific improvements, not just criticisms

### 9.2 Simulation Guidelines

When simulating LLM responses, the AI agent should:

1. **Follow the prompt exactly**: Don't add extra features
2. **Use realistic data**: Generate outputs that match real-world quality
3. **Vary responses**: Different test cases should produce different outputs
4. **Respect constraints**: Honor word limits, format requirements, etc.
5. **Be consistent**: Same test case should produce similar output across runs

### 9.3 Improvement Guidelines

When recommending prompt improvements, the AI agent should:

1. **Target root causes**: Fix underlying issues, not symptoms
2. **Be specific**: Provide exact wording changes
3. **Predict impact**: Estimate which scores will improve
4. **Prioritize**: Focus on high-impact changes first
5. **Validate**: Ensure changes don't break existing functionality

---

## 10. Next Steps

1. ✅ Review and approve this design spec
2. ⏳ Begin implementation for one-pager
3. ⏳ Begin implementation for product-requirements-assistant
4. ⏳ Document lessons learned for future projects
