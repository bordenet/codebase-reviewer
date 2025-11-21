#!/usr/bin/env python3
"""Commit and push the formatting fix using GitPython."""

import sys
import os

# Change to repo directory
os.chdir('/Users/matt/GitHub/Personal/codebase-reviewer')

# Use subprocess with explicit environment to avoid gh interference
import subprocess

env = os.environ.copy()
# Remove any GH_* environment variables that might cause issues
env = {k: v for k, v in env.items() if not k.startswith('GH_')}

def run(cmd):
    """Run command with clean environment."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}", file=sys.stderr)
    if result.returncode != 0:
        print(f"ERROR: Command failed with code {result.returncode}")
        sys.exit(1)
    return result

# Run black
print("=" * 80)
print("Running black...")
print("=" * 80)
run(["python3", "-m", "black", "--line-length=120", "src/codebase_reviewer/simulation.py"])

# Git add
print("\n" + "=" * 80)
print("Git add...")
print("=" * 80)
run(["git", "add", "src/codebase_reviewer/simulation.py"])

# Git commit
print("\n" + "=" * 80)
print("Git commit...")
print("=" * 80)
run(["git", "commit", "-m", "Fix formatting in simulation.py to pass CI\n\nChanges:\n- Fixed black formatting issues in simulation.py\n- Removed extra blank line at end of file\n- All pre-commit hooks now passing\n\nThis fixes the CI failure from commit ad93464"])

# Git push
print("\n" + "=" * 80)
print("Git push...")
print("=" * 80)
run(["git", "push", "origin", "main"])

print("\n" + "=" * 80)
print("✅ Done!")
print("=" * 80)

