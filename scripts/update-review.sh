#!/bin/bash
# Wrapper script for analyzing codebases and maintaining review history
# Usage: ./update-review.sh /path/to/codebase [output-dir]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CODEBASE_PATH="${1}"
OUTPUT_DIR="${2:-./reviews}"
KEEP_LAST_N=5
WORKFLOW="reviewer_criteria"

# Validate inputs
if [ -z "$CODEBASE_PATH" ]; then
    echo -e "${RED}Error: Codebase path required${NC}"
    echo "Usage: $0 /path/to/codebase [output-dir]"
    exit 1
fi

if [ ! -d "$CODEBASE_PATH" ]; then
    echo -e "${RED}Error: Codebase path does not exist: $CODEBASE_PATH${NC}"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE_ONLY=$(date +%Y%m%d)

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Codebase Review Updater${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Codebase:${NC} $CODEBASE_PATH"
echo -e "${YELLOW}Output:${NC}   $OUTPUT_DIR"
echo -e "${YELLOW}Workflow:${NC} $WORKFLOW"
echo ""

# Run analysis
echo -e "${GREEN}🔍 Running analysis...${NC}"
review-codebase analyze "$CODEBASE_PATH" \
  --workflow "$WORKFLOW" \
  --output "$OUTPUT_DIR/analysis_$TIMESTAMP.json" \
  --prompts-output "$OUTPUT_DIR/prompts_$TIMESTAMP.md"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Analysis failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Analysis complete!${NC}"
echo ""

# Create symlinks to latest
cd "$OUTPUT_DIR"
ln -sf "analysis_$TIMESTAMP.json" "analysis_latest.json"
ln -sf "prompts_$TIMESTAMP.md" "prompts_latest.md"

# Find previous analysis for comparison
PREV_PROMPTS=$(ls -t prompts_*.md 2>/dev/null | grep -v "prompts_$TIMESTAMP.md" | head -1)

if [ -n "$PREV_PROMPTS" ]; then
    echo -e "${YELLOW}📊 Comparing with previous analysis...${NC}"

    # Generate diff
    diff -u "$PREV_PROMPTS" "prompts_$TIMESTAMP.md" > "diff_$TIMESTAMP.txt" || true

    # Count changes
    ADDED=$(grep -c "^+" "diff_$TIMESTAMP.txt" 2>/dev/null || echo "0")
    REMOVED=$(grep -c "^-" "diff_$TIMESTAMP.txt" 2>/dev/null || echo "0")

    echo -e "  ${GREEN}+${ADDED}${NC} additions, ${RED}-${REMOVED}${NC} deletions"
    echo -e "  Diff saved to: diff_$TIMESTAMP.txt"
    echo ""
fi

# Clean up old analyses
echo -e "${YELLOW}🗂️  Cleaning up old analyses (keeping last $KEEP_LAST_N)...${NC}"
ls -t prompts_*.md 2>/dev/null | tail -n +$((KEEP_LAST_N + 1)) | xargs rm -f 2>/dev/null || true
ls -t analysis_*.json 2>/dev/null | tail -n +$((KEEP_LAST_N + 1)) | xargs rm -f 2>/dev/null || true
ls -t diff_*.txt 2>/dev/null | tail -n +$((KEEP_LAST_N + 1)) | xargs rm -f 2>/dev/null || true

# Summary
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Review Updated Successfully!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📁 Output Files:${NC}"
echo -e "  Latest prompts:  ${GREEN}$OUTPUT_DIR/prompts_latest.md${NC}"
echo -e "  Latest analysis: ${GREEN}$OUTPUT_DIR/analysis_latest.json${NC}"
echo -e "  Timestamped:     ${GREEN}$OUTPUT_DIR/prompts_$TIMESTAMP.md${NC}"
echo ""
echo -e "${YELLOW}📖 Next Steps:${NC}"
echo -e "  1. Review prompts: ${BLUE}cat $OUTPUT_DIR/prompts_latest.md${NC}"
echo -e "  2. View changes:   ${BLUE}cat $OUTPUT_DIR/diff_$TIMESTAMP.txt${NC}"
echo -e "  3. Take action on 🔴 CRITICAL items first"
echo ""
echo -e "${YELLOW}🔄 To update again:${NC}"
echo -e "  ${BLUE}$0 $CODEBASE_PATH $OUTPUT_DIR${NC}"
echo ""
