#!/bin/bash
# Security validation script for codebase-reviewer
# Ensures no proprietary information leaks to git

set -e

echo "🔒 Running security validation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Check 1: Verify .gitignore covers Acme patterns
echo "📋 Check 1: Verifying .gitignore patterns..."
if grep -q "Acme" .gitignore; then
    echo -e "${GREEN}✓${NC} Acme patterns found in .gitignore"
else
    echo -e "${RED}✗${NC} Acme patterns NOT found in .gitignore"
    ERRORS=$((ERRORS + 1))
fi

# Check 2: Scan Python/Go code files for Acme references (excluding docs/examples)
echo "📋 Check 2: Scanning code files for Acme references..."
ACME_IN_CODE=$(git ls-files | grep -E "\.(py|go)$" | xargs grep -l "Acme" 2>/dev/null | grep -v "test_" || true)
if [ -n "$ACME_IN_CODE" ]; then
    echo -e "${RED}✗${NC} Found Acme references in code files:"
    echo "$ACME_IN_CODE"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} No Acme references in code files"
fi

# Check 3: Scan for actual Acme file paths (not just the word "Acme")
echo "📋 Check 3: Scanning for Acme absolute file paths..."
ACME_PATHS=$(git ls-files | xargs grep -l "/Users/matt/GitHub/Acme/" 2>/dev/null | grep -v "scripts/\|docs/\|test_\|\.md$" || true)
if [ -n "$ACME_PATHS" ]; then
    echo -e "${RED}✗${NC} Found Acme absolute paths in files:"
    echo "$ACME_PATHS"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} No Acme absolute paths in files"
fi

# Check 4: Verify /tmp/ output directory exists and is writable
echo "📋 Check 4: Verifying /tmp/ output directory..."
if [ -w "/tmp" ]; then
    echo -e "${GREEN}✓${NC} /tmp/ is writable"
else
    echo -e "${RED}✗${NC} /tmp/ is not writable!"
    ERRORS=$((ERRORS + 1))
fi

# Check 5: Verify pre-commit hooks are installed
echo "📋 Check 5: Verifying pre-commit hooks..."
if [ -f ".git/hooks/pre-commit" ]; then
    echo -e "${GREEN}✓${NC} Pre-commit hooks are installed"
else
    echo -e "${YELLOW}⚠${NC} Pre-commit hooks not installed (run: pre-commit install)"
fi

# Check 6: Verify no analysis outputs in git (excluding templates)
echo "📋 Check 6: Checking for analysis outputs in git..."
ANALYSIS_FILES=$(git ls-files | grep -E "analysis.*\.(json|md)$|simulation.*\.json$" | grep -v "prompts/templates/" || true)
if [ -n "$ANALYSIS_FILES" ]; then
    echo -e "${RED}✗${NC} Found analysis output files in git:"
    echo "$ANALYSIS_FILES"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} No analysis outputs in git"
fi

# Check 7: Verify .gitignore patterns are comprehensive
echo "📋 Check 7: Verifying comprehensive .gitignore patterns..."
REQUIRED_PATTERNS=(
    "analysis-results.json"
    "simulation_results/"
    "*acme*"
    "*Acme*"
)

for pattern in "${REQUIRED_PATTERNS[@]}"; do
    if grep -q "$pattern" .gitignore; then
        echo -e "${GREEN}  ✓${NC} Pattern: $pattern"
    else
        echo -e "${RED}  ✗${NC} Missing pattern: $pattern"
        ERRORS=$((ERRORS + 1))
    fi
done

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All security checks passed!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
else
    echo -e "${RED}❌ Security validation failed with $ERRORS error(s)!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi

