#!/bin/bash
# Example: Comprehensive codebase analysis workflow
# This script demonstrates all the analysis features

set -e

PROJECT_PATH="${1:-.}"
OUTPUT_DIR="${2:-./analysis-results}"

echo "🚀 Codebase Reviewer - Comprehensive Analysis"
echo "=============================================="
echo "Project: $PROJECT_PATH"
echo "Output: $OUTPUT_DIR"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# 1. Run security and quality analysis
echo "📊 Step 1: Running security and quality analysis..."
python3 -m codebase_reviewer.cli analyze "$PROJECT_PATH" \
    --format json \
    --output "$OUTPUT_DIR/analysis.json"

python3 -m codebase_reviewer.cli analyze "$PROJECT_PATH" \
    --format html \
    --output "$OUTPUT_DIR/analysis.html"

python3 -m codebase_reviewer.cli analyze "$PROJECT_PATH" \
    --format interactive-html \
    --output "$OUTPUT_DIR/interactive-report.html"

echo "✅ Analysis complete!"
echo ""

# 2. Generate compliance reports
echo "📋 Step 2: Generating compliance reports..."
for framework in soc2 hipaa pci_dss; do
    echo "  - $framework compliance..."
    python3 -m codebase_reviewer.cli compliance "$PROJECT_PATH" \
        --framework "$framework" \
        --output "$OUTPUT_DIR/compliance-$framework.json" || true
done
echo "✅ Compliance reports complete!"
echo ""

# 3. Calculate productivity metrics
echo "📈 Step 3: Calculating productivity metrics..."
python3 -m codebase_reviewer.cli productivity "$PROJECT_PATH" \
    --days 30 > "$OUTPUT_DIR/productivity-30days.txt" || true

python3 -m codebase_reviewer.cli productivity "$PROJECT_PATH" \
    --days 90 > "$OUTPUT_DIR/productivity-90days.txt" || true
echo "✅ Productivity metrics complete!"
echo ""

# 4. Calculate ROI
echo "💰 Step 4: Calculating ROI..."
# Extract issue counts from analysis
CRITICAL=$(cat "$OUTPUT_DIR/analysis.json" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for i in data.get('quality_issues', []) if i.get('severity') == 'critical'))")
HIGH=$(cat "$OUTPUT_DIR/analysis.json" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for i in data.get('quality_issues', []) if i.get('severity') == 'high'))")
MEDIUM=$(cat "$OUTPUT_DIR/analysis.json" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for i in data.get('quality_issues', []) if i.get('severity') == 'medium'))")
LOW=$(cat "$OUTPUT_DIR/analysis.json" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for i in data.get('quality_issues', []) if i.get('severity') == 'low'))")

python3 -m codebase_reviewer.cli roi \
    --team-size 5 \
    --salary 120000 \
    --critical "$CRITICAL" \
    --high "$HIGH" \
    --medium "$MEDIUM" \
    --low "$LOW" \
    --months 12 > "$OUTPUT_DIR/roi-analysis.txt"
echo "✅ ROI calculation complete!"
echo ""

# 5. Summary
echo "🎉 Analysis Complete!"
echo "===================="
echo ""
echo "📁 Results saved to: $OUTPUT_DIR"
echo ""
echo "📊 Reports generated:"
echo "  - analysis.json (structured data)"
echo "  - analysis.html (visual report)"
echo "  - interactive-report.html (interactive dashboard)"
echo "  - compliance-*.json (compliance reports)"
echo "  - productivity-*.txt (productivity metrics)"
echo "  - roi-analysis.txt (ROI calculation)"
echo ""
echo "🌐 Open the interactive report:"
echo "  open $OUTPUT_DIR/interactive-report.html"
echo ""
echo "📈 View ROI analysis:"
echo "  cat $OUTPUT_DIR/roi-analysis.txt"
echo ""
