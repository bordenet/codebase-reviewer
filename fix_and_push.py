#!/usr/bin/env python3
"""Fix formatting and push to fix CI."""

import subprocess
import sys

def run_command(cmd, check=True):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result

# Run black on simulation.py
print("=" * 80)
print("Step 1: Running black on simulation.py")
print("=" * 80)
run_command(["python3", "-m", "black", "--line-length=120", "src/codebase_reviewer/simulation.py"])

# Run pre-commit hooks
print("\n" + "=" * 80)
print("Step 2: Running pre-commit hooks")
print("=" * 80)
result = run_command(["pre-commit", "run", "--all-files"], check=False)

if result.returncode != 0:
    print("\nPre-commit hooks failed. Running again to fix...")
    run_command(["pre-commit", "run", "--all-files"])

# Git add
print("\n" + "=" * 80)
print("Step 3: Git add")
print("=" * 80)
run_command(["git", "add", "-A"])

# Git status
print("\n" + "=" * 80)
print("Step 4: Git status")
print("=" * 80)
run_command(["git", "status"])

# Git commit
print("\n" + "=" * 80)
print("Step 5: Git commit")
print("=" * 80)
commit_msg = """Fix formatting in simulation.py to pass CI

Changes:
- Fixed black formatting issues in simulation.py
- Removed extra blank line at end of file
- All pre-commit hooks now passing

This fixes the CI failure from commit ad93464
"""
run_command(["git", "commit", "-m", commit_msg])

# Git push
print("\n" + "=" * 80)
print("Step 6: Git push")
print("=" * 80)
run_command(["git", "push", "origin", "main"])

print("\n" + "=" * 80)
print("✅ Done! CI should pass now.")
print("=" * 80)

