#!/bin/bash
# ============================================================================
# IP Protection Test Script
# ============================================================================
# Tests that .gitignore and pre-commit hooks properly block sensitive data
# ============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🧪 Testing IP Protection Measures${NC}"
echo ""

TESTS_PASSED=0
TESTS_FAILED=0

# Create temporary test directory
TEST_DIR="__test_ip_protection__"
mkdir -p "$TEST_DIR"

cleanup() {
    echo ""
    echo "Cleaning up test files..."
    rm -rf "$TEST_DIR"
    git reset HEAD . 2>/dev/null || true
}

trap cleanup EXIT

# ============================================================================
# TEST 1: Verify .gitignore blocks analysis outputs
# ============================================================================
echo -e "${YELLOW}Test 1: .gitignore blocks analysis outputs${NC}"

# Create fake analysis file
cat > "$TEST_DIR/analysis.json" << 'EOF'
{
  "repository": "/Users/matt/GitHub/CallBox/Cari",
  "analysis": {
    "files": ["src/index.ts", "src/api.ts"],
    "code_snippets": ["const api = require('./api');"]
  }
}
EOF

# Check if git ignores it
if git check-ignore -q "$TEST_DIR/analysis.json"; then
    echo -e "${GREEN}✓ PASS: analysis.json is ignored${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}✗ FAIL: analysis.json is NOT ignored${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ============================================================================
# TEST 2: Verify .gitignore blocks prompt files
# ============================================================================
echo -e "${YELLOW}Test 2: .gitignore blocks prompt files${NC}"

cat > "$TEST_DIR/prompts.md" << 'EOF'
# Generated Prompts

## Prompt 1
Analyze the following code from /Users/matt/GitHub/CallBox/Cari/src/index.ts
EOF

if git check-ignore -q "$TEST_DIR/prompts.md"; then
    echo -e "${GREEN}✓ PASS: prompts.md is ignored${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}✗ FAIL: prompts.md is NOT ignored${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ============================================================================
# TEST 3: Verify .gitignore blocks simulation results
# ============================================================================
echo -e "${YELLOW}Test 3: .gitignore blocks simulation results${NC}"

mkdir -p "$TEST_DIR/simulation_results"
cat > "$TEST_DIR/simulation_results/test.json" << 'EOF'
{"simulation": "data"}
EOF

if git check-ignore -q "$TEST_DIR/simulation_results/test.json"; then
    echo -e "${GREEN}✓ PASS: simulation_results/ is ignored${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}✗ FAIL: simulation_results/ is NOT ignored${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ============================================================================
# TEST 4: Verify .gitignore blocks tuning results
# ============================================================================
echo -e "${YELLOW}Test 4: .gitignore blocks tuning results${NC}"

mkdir -p "$TEST_DIR/prompt_tuning_results"
cat > "$TEST_DIR/prompt_tuning_results/test_cases.json" << 'EOF'
{"test_cases": []}
EOF

if git check-ignore -q "$TEST_DIR/prompt_tuning_results/test_cases.json"; then
    echo -e "${GREEN}✓ PASS: prompt_tuning_results/ is ignored${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}✗ FAIL: prompt_tuning_results/ is NOT ignored${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ============================================================================
# TEST 5: Verify .gitignore blocks repo-specific files
# ============================================================================
echo -e "${YELLOW}Test 5: .gitignore blocks repo-specific files${NC}"

cat > "$TEST_DIR/cari_analysis.json" << 'EOF'
{"repo": "cari", "data": "sensitive"}
EOF

if git check-ignore -q "$TEST_DIR/cari_analysis.json"; then
    echo -e "${GREEN}✓ PASS: cari_analysis.json is ignored${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}✗ FAIL: cari_analysis.json is NOT ignored${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ============================================================================
# TEST 6: Verify pre-commit hook blocks sensitive files
# ============================================================================
echo -e "${YELLOW}Test 6: Pre-commit hook blocks sensitive files${NC}"

# Create a file that should be blocked
cat > "$TEST_DIR/test_blocked.json" << 'EOF'
{
  "repository_path": "/Users/matt/GitHub/CallBox/Cari",
  "analysis": "sensitive data"
}
EOF

# Try to stage it
git add "$TEST_DIR/test_blocked.json" 2>/dev/null || true

# Try to commit (should fail)
if git commit -m "Test commit" 2>&1 | grep -q "COMMIT BLOCKED"; then
    echo -e "${GREEN}✓ PASS: Pre-commit hook blocked sensitive file${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    git reset HEAD . 2>/dev/null || true
else
    # Check if it was ignored instead
    if git check-ignore -q "$TEST_DIR/test_blocked.json"; then
        echo -e "${GREEN}✓ PASS: File was ignored by .gitignore${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL: Pre-commit hook did not block sensitive file${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    git reset HEAD . 2>/dev/null || true
fi

# ============================================================================
# TEST 7: Verify allowed files can be committed
# ============================================================================
echo -e "${YELLOW}Test 7: Allowed files can be committed${NC}"

cat > "$TEST_DIR/safe_file.txt" << 'EOF'
This is a safe file with no sensitive data.
EOF

git add "$TEST_DIR/safe_file.txt" 2>/dev/null || true

if git diff --cached --name-only | grep -q "safe_file.txt"; then
    echo -e "${GREEN}✓ PASS: Safe files can be staged${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}✗ FAIL: Safe files cannot be staged${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

git reset HEAD . 2>/dev/null || true

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo -e "Test Results: ${GREEN}$TESTS_PASSED passed${NC}, ${RED}$TESTS_FAILED failed${NC}"
echo "═══════════════════════════════════════════════════════════════"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All IP protection tests passed!${NC}"
    echo -e "${GREEN}✓ Safe to push to GitHub${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed - DO NOT PUSH${NC}"
    exit 1
fi
