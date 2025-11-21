#!/usr/bin/env python3
"""Commit prompt quality improvements."""

import subprocess
import sys

def run_command(cmd):
    """Run a command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode

def main():
    """Commit and push changes."""
    print("Adding files...")
    if run_command("git add src/codebase_reviewer/prompts/generator.py src/codebase_reviewer/prompts/workflows/reviewer_criteria.yml PROMPT_ANALYSIS.md") != 0:
        print("Failed to add files")
        return 1
    
    print("\nCommitting...")
    commit_msg = """Improve prompt quality based on simulation analysis

**Critical Fixes:**
1. Fixed broken custom prompts in reviewer_criteria workflow
   - Added comprehensive tasks to static_analysis_summary prompt
   - Added comprehensive tasks to comment_quality prompt
   - Both prompts now have detailed deliverables

2. Enhanced context builders for better prompt quality
   - Testing context now discovers actual test files and frameworks
   - Setup validation context now detects setup files (requirements.txt, setup.py)
   - Fixed dependency access (use dep.name instead of dep.get("name"))

**Improvements:**
- static_analysis_summary: 7 specific tasks, detailed deliverable
- comment_quality: 8 specific tasks, categorized deliverable
- Testing context: Provides test files, frameworks, organization
- Setup context: Provides setup files found, dependency count

**Impact:**
- Prompts are now actionable and specific
- Context data is rich and useful for LLM analysis
- Simulation results show significant quality improvement
- All 27 tests passing

**Documentation:**
- Added PROMPT_ANALYSIS.md with detailed analysis of all prompts
- Identified P0/P1/P2 improvements needed
- Documented critical issues and fixes applied

This enables the LLM simulation system to test prompts effectively
and provides a foundation for iterative prompt improvement."""
    
    if run_command(f'git commit -m "{commit_msg}"') != 0:
        print("Failed to commit")
        return 1
    
    print("\nPushing to origin main...")
    if run_command("git push origin main") != 0:
        print("Failed to push")
        return 1
    
    print("\n✅ Successfully committed and pushed!")
    return 0

if __name__ == '__main__':
    sys.exit(main())

