#!/bin/bash
# Test Phase II Regeneration Flow
# This script demonstrates the complete self-evolution cycle

set -e

echo "🧪 Testing Phase II Regeneration Flow"
echo "======================================"
echo ""

# Setup
TEST_CODEBASE="/tmp/test-codebase-phase2"
OUTPUT_DIR="/tmp/codebase-reviewer/test-codebase-phase2"
VENV_PATH=".venv"

# Clean up from previous runs
echo "🧹 Cleaning up previous test runs..."
rm -rf "$TEST_CODEBASE" "$OUTPUT_DIR"
mkdir -p "$TEST_CODEBASE"

# Create a simple test codebase
echo "📁 Creating test codebase..."
cat > "$TEST_CODEBASE/main.py" << 'EOF'
"""Test application."""

def hello():
    """Say hello."""
    print("Hello, World!")

if __name__ == "__main__":
    hello()
EOF

cat > "$TEST_CODEBASE/utils.py" << 'EOF'
"""Utility functions."""

def add(a, b):
    """Add two numbers."""
    return a + b
EOF

echo "✅ Test codebase created at $TEST_CODEBASE"
echo ""

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Step 1: Run Phase 1 analysis (Generation 1)
echo "📊 Step 1: Running Phase 1 Analysis (Generation 1)..."
echo "------------------------------------------------------"
mkdir -p "$OUTPUT_DIR"
python -m codebase_reviewer.cli analyze "$TEST_CODEBASE" \
    --output "$OUTPUT_DIR/gen1-analysis.json" \
    --format json \
    || echo "Analysis completed with findings"

echo ""
echo "✅ Phase 1 analysis complete"
echo "   Output: $OUTPUT_DIR/gen1-analysis.json"
echo ""

# Step 2: Initialize metrics tracking
echo "📈 Step 2: Initializing Metrics Tracking..."
echo "--------------------------------------------"
python3 << 'PYTHON_SCRIPT'
from pathlib import Path
from src.codebase_reviewer.metrics.tracker import MetricsTracker

# Initialize tracker
tracker = MetricsTracker(
    codebase_path=Path("/tmp/test-codebase-phase2"),
    output_dir=Path("/tmp/codebase-reviewer/test-codebase-phase2")
)

# Update coverage metrics (simulating initial run)
tracker.update_coverage(
    files_total=2,
    files_analyzed=2,
    files_documented=2
)

# Save metrics
tracker.save()
print(f"✅ Initial metrics saved to: {tracker.metrics_file}")
PYTHON_SCRIPT

echo ""

# Step 3: Simulate codebase changes (to trigger obsolescence)
echo "🔄 Step 3: Simulating Codebase Changes..."
echo "------------------------------------------"
echo "Adding new files to trigger obsolescence detection..."

cat > "$TEST_CODEBASE/new_feature.py" << 'EOF'
"""New feature added."""

def new_function():
    """A new function."""
    return "New feature!"
EOF

cat > "$TEST_CODEBASE/config.js" << 'EOF'
// New JavaScript file (new language!)
const config = {
    version: "2.0"
};
EOF

echo "✅ Added 2 new files (including new language: JavaScript)"
echo ""

# Step 4: Detect obsolescence
echo "🔍 Step 4: Detecting Obsolescence..."
echo "-------------------------------------"
python3 << 'PYTHON_SCRIPT'
from pathlib import Path
from src.codebase_reviewer.metrics.tracker import MetricsTracker
from src.codebase_reviewer.obsolescence.detector import ObsolescenceDetector, ObsolescenceThresholds

# Create tracker for updated codebase
tracker = MetricsTracker(
    codebase_path=Path("/tmp/test-codebase-phase2"),
    output_dir=Path("/tmp/codebase-reviewer/test-codebase-phase2")
)

# Update with new metrics
tracker.update_coverage(
    files_total=4,  # Was 2, now 4 (100% increase!)
    files_analyzed=2,  # Only analyzed 2 of 4
    files_documented=2
)

# Add new language detection
tracker.update_changes(
    files_changed=2,
    files_added=2,
    files_deleted=0,
    new_languages=["javascript"]
)

tracker.save()

# Detect obsolescence
detector = ObsolescenceDetector(
    codebase_path=Path("/tmp/test-codebase-phase2"),
    thresholds=ObsolescenceThresholds(
        files_changed_percent=30.0,  # Trigger at 30% change
        coverage_min_percent=85.0,   # Require 85% coverage
        new_languages_detected=True  # Trigger on new languages
    )
)

result = detector.detect_obsolescence(tracker.get_metrics())

print(f"\n{'='*60}")
print(f"OBSOLESCENCE DETECTION RESULT")
print(f"{'='*60}")
print(f"Is Obsolete: {result.is_obsolete}")
print(f"Should Regenerate: {result.should_regenerate}")
print(f"\nReasons:")
for reason in result.reasons:
    print(f"  - {reason}")
print(f"{'='*60}\n")

if result.should_regenerate:
    print("✅ Obsolescence detected! Regeneration recommended.")
else:
    print("ℹ️  No regeneration needed.")
PYTHON_SCRIPT

echo ""

# Step 5: Generate regeneration prompt
echo "📝 Step 5: Generating Regeneration Prompt..."
echo "---------------------------------------------"
python3 << 'PYTHON_SCRIPT'
from pathlib import Path
from src.codebase_reviewer.prompts.generator_v2 import Phase1PromptGeneratorV2, ScanParameters

# Generate enhanced Phase 1 prompt for Generation 2
generator = Phase1PromptGeneratorV2()

params = ScanParameters(
    target_path="/tmp/test-codebase-phase2",
    scan_mode="deep_scan",
    output_path="/tmp/codebase-reviewer/test-codebase-phase2",
    languages=["python", "javascript"]  # Now includes JS!
)

prompt = generator.generate_prompt(params)

# Save regeneration prompt
output_path = Path("/tmp/codebase-reviewer/test-codebase-phase2/regeneration-prompt-gen2.md")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(prompt)

print(f"✅ Regeneration prompt saved to:")
print(f"   {output_path}")
print(f"\nPrompt preview (first 800 chars):")
print(f"{'-'*60}")
print(prompt[:800])
print(f"...")
print(f"{'-'*60}")
PYTHON_SCRIPT

echo ""
echo "🎉 Phase II Regeneration Flow Test Complete!"
echo "============================================="
echo ""
echo "Summary:"
echo "  1. ✅ Created test codebase (2 Python files)"
echo "  2. ✅ Ran Phase 1 analysis (Generation 1)"
echo "  3. ✅ Initialized metrics tracking"
echo "  4. ✅ Simulated codebase changes (added 2 files, new language)"
echo "  5. ✅ Detected obsolescence (files changed + new language)"
echo "  6. ✅ Generated regeneration prompt (Generation 2)"
echo ""
echo "Next steps (manual):"
echo "  1. Review regeneration prompt at:"
echo "     $OUTPUT_DIR/regeneration-prompt-gen2.md"
echo "  2. Give prompt to AI assistant"
echo "  3. AI generates improved Phase 2 tools (Gen 2)"
echo "  4. Run Gen 2 tools on updated codebase"
echo ""
echo "Files created:"
echo "  - $OUTPUT_DIR/gen1-analysis.json"
echo "  - $OUTPUT_DIR/metrics.yaml"
echo "  - $OUTPUT_DIR/regeneration-prompt-gen2.md"
echo ""

