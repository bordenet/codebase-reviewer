# Prompt Quality Analysis and Improvement Plan

**Date:** 2025-11-21
**Analyst:** AI Assistant (Claude Sonnet 4.5)
**Simulation Results Analyzed:**
- `simulation_default_20251121_065933.md` (9 prompts)
- `simulation_reviewer_criteria_20251121_065936.md` (19 prompts)

## Executive Summary

After analyzing simulation results from both workflows, I've identified **critical issues** that would make these prompts **unhelpful** in real-world usage:

### Critical Issues Found

1. **Missing Tasks/Deliverables** - Several prompts have empty or incomplete task lists
2. **Vague Objectives** - Many prompts lack specific, actionable guidance
3. **Poor Context Usage** - Prompts don't effectively leverage the rich context data provided
4. **Redundancy** - Significant overlap between prompts in different workflows
5. **Lack of Specificity** - Generic prompts that could apply to any codebase

### Impact Assessment

**Current State:** ❌ Prompts would produce generic, unhelpful responses
**Target State:** ✅ Prompts that produce specific, actionable insights

## Detailed Analysis by Prompt

### Phase 0: Documentation Review

#### Prompt 0.1: README Analysis & Claims Extraction
**Status:** ⚠️ Needs Improvement
**Issues:**
- Good objective and task list
- **Missing:** Specific output format/structure
- **Missing:** Guidance on how to handle missing README
- Context data is excellent (full README content provided)

**Improvements Needed:**
- Add structured output format (JSON schema or markdown template)
- Add handling for repos without README
- Add examples of "testable claims"

#### Prompt: static_analysis_summary
**Status:** ❌ CRITICAL - Broken
**Issues:**
- **EMPTY TASKS** - No tasks specified!
- **EMPTY DELIVERABLE** - No deliverable specified!
- This prompt is completely unusable

**Improvements Needed:**
- Add comprehensive task list for static analysis
- Specify deliverable format
- Add context about which tools to simulate (pylint, mypy, etc.)

### Phase 1: Architecture Analysis

#### Prompt 1.1: Validate Documented Architecture
**Status:** ⚠️ Needs Improvement
**Issues:**
- Good task list
- Context data shows hardcoded assumptions (pattern: 'microservices', components list)
- **Problem:** Context shows "Found 0/5 claimed components" - the context builder is broken!

**Improvements Needed:**
- Fix context builder to actually extract components from code
- Remove hardcoded architecture assumptions
- Add guidance on what to do when no architecture is documented

### Security Prompts (reviewer_criteria workflow)

#### Prompt security.1: Vulnerability Assessment
**Status:** ⚠️ Needs Improvement
**Issues:**
- Tasks are too generic
- No specific vulnerability categories mentioned
- Missing OWASP Top 10 reference
- No guidance on severity classification
- Good context data (shows actual security issues found: eval(), exec())

**Improvements Needed:**
- Reference OWASP Top 10 and CWE categories
- Add severity classification guidance (Critical/High/Medium/Low)
- Specify output format for vulnerability reports
- Add examples of common Python vulnerabilities

#### Prompt: comment_quality
**Status:** ❌ CRITICAL - Broken
**Issues:**
- **EMPTY TASKS** - No tasks specified!
- **EMPTY DELIVERABLE** - No deliverable specified!
- Context data is in wrong format (should be dict, not string)
- This prompt is completely unusable

**Improvements Needed:**
- Add comprehensive task list
- Specify deliverable format
- Fix context data format

#### Prompt arch.1: Call Graph & Dependency Tracing
**Status:** ✅ Good - Minor Improvements
**Issues:**
- Excellent task list
- Good deliverable structure with sections
- **Problem:** Context shows external dependencies, not internal code dependencies
- Missing guidance on tools/techniques for call graph analysis

**Improvements Needed:**
- Fix context builder to provide internal module dependencies
- Add file structure/imports data to context
- Add guidance on static analysis techniques

### Phase 3: Development Workflow

#### Prompt 3.1: Validate Setup Instructions
**Status:** ⚠️ Needs Improvement
**Issues:**
- Good task list
- **Problem:** Context shows empty data (prerequisites: [], build_steps: [], env_vars: [])
- Context builder is not extracting setup information properly

**Improvements Needed:**
- Fix context builder to extract setup steps from README
- Add parsing for requirements.txt, setup.py, pyproject.toml
- Add detection of environment variables from code

#### Prompt 3.2: Testing Strategy Review
**Status:** ❌ CRITICAL - Useless Context
**Issues:**
- Good task list
- **CRITICAL:** Context only contains `{'repository_path': '.'}`
- No test file information, no coverage data, nothing useful!
- LLM would have to guess everything

**Improvements Needed:**
- Add test file discovery and listing
- Add test framework detection (pytest, unittest, etc.)
- Add coverage data if available
- Add test file count and organization structure
- Add sample test names/patterns

## Summary of Critical Issues

### Broken Prompts (Unusable)
1. **static_analysis_summary** - Empty tasks and deliverable
2. **comment_quality** - Empty tasks and deliverable
3. **3.2 (Testing Strategy)** - Useless context (only repo path)

### Context Builder Issues
1. **Architecture validation** - Hardcoded assumptions, finds 0/5 components
2. **Setup validation** - Returns empty data
3. **Call graph analysis** - Shows external deps instead of internal structure
4. **Testing review** - Provides no useful data

### Missing Improvements
1. No structured output formats (JSON schemas, markdown templates)
2. No severity/priority classification guidance
3. No examples of good vs bad patterns
4. No handling of edge cases (missing files, empty repos)
5. Generic tasks that don't leverage context data

## Improvement Priority

### P0 - Critical (Must Fix)
1. Fix broken prompts (static_analysis_summary, comment_quality)
2. Fix testing strategy context builder
3. Fix setup validation context builder
4. Fix architecture validation context builder

### P1 - High (Should Fix)
1. Add structured output formats to all prompts
2. Add severity classification to security prompts
3. Improve call graph context to show internal dependencies
4. Add examples and guidance to vague prompts

### P2 - Medium (Nice to Have)
1. Add edge case handling
2. Add more specific Python-focused guidance
3. Reduce redundancy between workflows
4. Add cross-references between related prompts

## Next Steps

1. **Fix P0 issues** - Update YAML templates for broken prompts
2. **Fix context builders** - Update PhaseGenerator to provide useful data
3. **Re-run simulation** - Verify improvements
4. **Iterate** - Continue improving based on results
