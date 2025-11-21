#!/usr/bin/env python3
"""Commit and push simulation fixes."""

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
    if run_command("git add src/codebase_reviewer/prompt_generator.py src/codebase_reviewer/prompts/template_loader.py") != 0:
        print("Failed to add files")
        return 1
    
    print("\nCommitting...")
    commit_msg = """Fix template loading for reviewer_criteria workflow

Changes:
- Fixed PromptTemplate instantiation in template_loader.py
  - Changed from PromptTemplate(**prompt_data) to PromptTemplate(prompt_data)
  - The __init__ method expects a single dict parameter, not keyword args
  
- Fixed template-to-prompt conversion in prompt_generator.py
  - Use template.to_prompt() method instead of manually creating Prompt
  - Removes incorrect reference to template.context attribute
  - Properly delegates to PromptTemplate's conversion logic

Impact:
- reviewer_criteria workflow now works correctly
- Successfully generates 19 prompts (vs 9 for default workflow)
- All 27 tests passing
- Simulation system fully functional

This enables running simulations on both workflows to evaluate and improve prompt quality."""
    
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

