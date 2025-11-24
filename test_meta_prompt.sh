#!/bin/bash
# Test meta-prompt generation

set -e

echo "=========================================="
echo "Testing Meta-Prompt Generation"
echo "=========================================="
echo ""

# Use the existing Phase 1 prompt from CallBox
PHASE1_PROMPT="/tmp/codebase-reviewer/CallBox/phase1-llm-prompt.md"

if [ ! -f "$PHASE1_PROMPT" ]; then
    echo "❌ Phase 1 prompt not found: $PHASE1_PROMPT"
    echo "   Run: ./bin/generate-docs /Users/Matt/GitHub/CallBox"
    exit 1
fi

echo "✅ Found Phase 1 prompt: $PHASE1_PROMPT"
echo ""

# Test meta-prompt generation
echo "Generating meta-prompt..."
python3 << 'EOF'
from pathlib import Path
from src.codebase_reviewer.metaprompt.generator import MetaPromptGenerator

# Generate meta-prompt
gen = MetaPromptGenerator()
meta_prompt = gen.generate(
    phase1_prompt_path=Path("/tmp/codebase-reviewer/CallBox/phase1-llm-prompt.md"),
    codebase_name="CallBox",
    generation=1
)

# Save it
output_path = Path("/tmp/test-meta-prompt.md")
output_path.write_text(meta_prompt)

print(f"✅ Meta-prompt generated: {output_path}")
print(f"   Size: {len(meta_prompt):,} bytes")
print(f"   Lines: {len(meta_prompt.splitlines()):,}")
print("")
print("Preview (first 50 lines):")
print("=" * 60)
print("\n".join(meta_prompt.splitlines()[:50]))
print("=" * 60)
EOF

echo ""
echo "=========================================="
echo "✅ Test Complete!"
echo "=========================================="
echo ""
echo "Meta-prompt saved to: /tmp/test-meta-prompt.md"
echo ""
echo "Next steps:"
echo "1. Review the meta-prompt: cat /tmp/test-meta-prompt.md"
echo "2. Copy it to your AI assistant"
echo "3. Ask AI to generate Phase 2 tools"
echo ""

