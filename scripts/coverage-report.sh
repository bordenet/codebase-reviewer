#!/bin/bash
# Generate a code coverage report across all repositories in a workspace
# Usage: ./coverage-report.sh [workspace-path] [-v|--verbose]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
WORKSPACE="${1:-$HOME/GitHub/Personal}"
VERBOSE=false
START_TIME=$(date +%s)

# Parse args
for arg in "$@"; do
    case $arg in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [workspace-path] [-v|--verbose]"
            echo ""
            echo "Options:"
            echo "  -v, --verbose   Show detailed output for each repo"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Scans all repos in workspace and reports coverage by language."
            exit 0
            ;;
    esac
done

log_info() { echo -e "${BLUE}ℹ${NC} $*"; }
log_success() { echo -e "${GREEN}✓${NC} $*"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $*"; }
log_error() { echo -e "${RED}✗${NC} $*" >&2; }

# Validate workspace
if [ ! -d "$WORKSPACE" ]; then
    log_error "Workspace path does not exist: $WORKSPACE"
    exit 1
fi

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Code Coverage Report${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Workspace:${NC} $WORKSPACE"
echo -e "${YELLOW}Date:${NC}      $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Results arrays (using temp files for compatibility)
REPORT_FILE=$(mktemp)

# Function to get JS/TS coverage
get_js_coverage() {
    local dir="$1"
    if [ -f "$dir/package.json" ] && grep -q '"jest"' "$dir/package.json" 2>/dev/null; then
        local result
        result=$(cd "$dir" && npm test -- --coverage --silent 2>&1 | grep -E "All files\s*\|" | head -1)
        if [ -n "$result" ]; then
            echo "$result" | awk -F'|' '{gsub(/[[:space:]]/, "", $2); print $2}'
        fi
    fi
}

# Function to get Go coverage
get_go_coverage() {
    local dir="$1"
    if [ -f "$dir/go.mod" ]; then
        local result
        result=$(cd "$dir" && go test -coverprofile=/tmp/cover.out ./... 2>&1 | grep -oE '[0-9]+\.[0-9]+%' | tail -1)
        if [ -z "$result" ]; then
            result=$(cd "$dir" && go tool cover -func=/tmp/cover.out 2>/dev/null | grep total | awk '{print $3}')
        fi
        echo "$result"
    fi
}

# Function to get Python coverage
get_python_coverage() {
    local dir="$1"
    if [ -f "$dir/pytest.ini" ] || [ -f "$dir/pyproject.toml" ] || [ -d "$dir/tests" ]; then
        local result
        result=$(cd "$dir" && python3 -m pytest --cov=. --cov-report=term-missing -q 2>&1 | grep "TOTAL" | awk '{print $NF}')
        echo "$result"
    fi
}

# Scan repos
log_info "Scanning repositories..."
echo ""

for repo in "$WORKSPACE"/*/ "$WORKSPACE"/*/*/; do
    [ -d "$repo/.git" ] || continue

    name=$(basename "$repo")
    lang=""
    coverage=""

    # Detect language and get coverage
    if [ -f "$repo/go.mod" ]; then
        lang="Go"
        coverage=$(get_go_coverage "$repo")
    elif [ -f "$repo/package.json" ]; then
        lang="JS/TS"
        coverage=$(get_js_coverage "$repo")
    elif [ -f "$repo/pytest.ini" ] || [ -f "$repo/pyproject.toml" ]; then
        lang="Python"
        coverage=$(get_python_coverage "$repo")
    fi

    if [ -n "$lang" ]; then
        [ -z "$coverage" ] && coverage="N/A"
        echo "$name|$lang|$coverage" >> "$REPORT_FILE"

        if $VERBOSE; then
            echo -e "  ${GREEN}✓${NC} $name ($lang): $coverage"
        fi
    fi
done

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
printf "%-35s %-10s %s\n" "Repository" "Language" "Coverage"
echo "─────────────────────────────────────────────────────────────────"
sort -t'|' -k3 -rn "$REPORT_FILE" | while IFS='|' read -r name lang cov; do
    # Color based on coverage
    if [[ "$cov" =~ ^[0-9] ]]; then
        num=$(echo "$cov" | sed 's/%//')
        if (( $(echo "$num >= 75" | bc -l) )); then
            color=$GREEN
        elif (( $(echo "$num >= 50" | bc -l) )); then
            color=$YELLOW
        else
            color=$RED
        fi
    else
        color=$NC
    fi
    printf "%-35s %-10s ${color}%s${NC}\n" "$name" "$lang" "$cov"
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo -e "${GREEN}✓ Report complete${NC} (${DURATION}s)"

rm -f "$REPORT_FILE"
