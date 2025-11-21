#!/bin/bash
set -e

echo "Running black..."
python3 -m black --line-length=120 src/codebase_reviewer/simulation.py

echo "Running pre-commit..."
pre-commit run --all-files || pre-commit run --all-files

echo "Git add..."
git add -A

echo "Git status..."
git status

echo "Git commit..."
git commit -m "Fix formatting in simulation.py to pass CI

Changes:
- Fixed black formatting issues in simulation.py  
- Removed extra blank line at end of file
- All pre-commit hooks now passing

This fixes the CI failure from commit ad93464"

echo "Git push..."
git push origin main

echo "Done!"

