"""Interactive workflow for collaborating with AI assistant."""

import sys
from pathlib import Path
from typing import Optional


class InteractiveWorkflow:
    """Manages interactive workflow with AI assistant."""

    @staticmethod
    def display_prompt(prompt_path: Path, codebase_name: str):
        """Display Phase 1 prompt for user to copy to AI assistant.

        Args:
            prompt_path: Path to Phase 1 prompt file
            codebase_name: Name of codebase being analyzed
        """
        print("\n" + "=" * 80)
        print("  📋 PHASE 1 PROMPT GENERATED")
        print("=" * 80)
        print(f"\nCodebase: {codebase_name}")
        print(f"Prompt saved to: {prompt_path}")
        print(f"Prompt size: {prompt_path.stat().st_size:,} bytes")
        print(f"Lines: {len(prompt_path.read_text().splitlines()):,}")

        print("\n" + "─" * 80)
        print("  🤖 NEXT STEP: Give this prompt to your AI assistant")
        print("─" * 80)
        print("\n1. Copy the prompt:")
        print(f"   cat {prompt_path} | pbcopy")
        print("\n2. Paste it to your AI assistant (e.g., Claude, ChatGPT, Augment)")
        print("\n3. Ask the AI to generate Phase 2 Go tools")
        print("\n4. Copy the AI's response to a file:")
        print(f"   # Paste AI response, then press Ctrl+D")
        print(f"   cat > /tmp/ai-response.md")
        print("\n5. Continue with this tool:")
        print(f"   review-codebase evolve {codebase_name} \\")
        print(f"     --ai-response /tmp/ai-response.md \\")
        print(f"     --auto-run")

        print("\n" + "=" * 80)
        print("  💡 TIP: The AI assistant will generate Go code for offline tools")
        print("=" * 80)
        print("\nThe AI will create tools that can regenerate documentation")
        print("WITHOUT needing the AI again - infinite free runs!")
        print("\n" + "=" * 80 + "\n")

    @staticmethod
    def wait_for_response(response_path: Optional[Path] = None) -> Path:
        """Wait for user to provide AI response.

        Args:
            response_path: Optional path to AI response file

        Returns:
            Path to AI response file

        Raises:
            FileNotFoundError: If response file doesn't exist
        """
        if response_path and response_path.exists():
            return response_path

        print("\n" + "=" * 80)
        print("  ⏳ WAITING FOR AI RESPONSE")
        print("=" * 80)
        print("\nPlease provide the AI assistant's response.")
        print("\nOption 1: Paste directly (then press Ctrl+D)")
        print("─" * 80)

        try:
            print("\nPaste AI response here:\n")
            lines = []
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break

            if not lines:
                print("\n❌ No response provided")
                sys.exit(1)

            # Save to temp file
            temp_response = Path("/tmp/ai-response.md")
            temp_response.write_text("\n".join(lines))

            print(f"\n✅ Response saved to: {temp_response}")
            return temp_response

        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            sys.exit(1)

    @staticmethod
    def display_success(tools_dir: Path, binary_path: Path, codebase_path: Path):
        """Display success message with next steps.

        Args:
            tools_dir: Directory containing generated tools
            binary_path: Path to compiled binary
            codebase_path: Path to codebase
        """
        print("\n" + "=" * 80)
        print("  🎉 PHASE 2 TOOLS GENERATED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\nTools Location: {tools_dir}")
        print(f"Binary: {binary_path}")

        print("\n" + "─" * 80)
        print("  🚀 NEXT STEPS: Use your offline tools")
        print("─" * 80)
        print("\n1. Run tools to generate documentation:")
        print(f"   {binary_path} {codebase_path}")
        print("\n2. View generated docs:")
        print(f"   ls /tmp/codebase-reviewer/{codebase_path.name}/")
        print("\n3. Re-run anytime (no AI needed!):")
        print(f"   {binary_path} {codebase_path}")

        print("\n" + "─" * 80)
        print("  💰 COST ANALYSIS")
        print("─" * 80)
        print("\n✅ One-time AI interaction: DONE")
        print("✅ Future runs: $0.00 (offline, no AI needed)")
        print("✅ Speed: 10x faster than AI")
        print("✅ Frequency: Unlimited")

        print("\n" + "=" * 80)
        print("  🎯 MISSION ACCOMPLISHED!")
        print("=" * 80)
        print("\nYou now have self-contained tools that can regenerate")
        print("documentation as your codebase evolves - no AI required!")
        print("\n" + "=" * 80 + "\n")

    @staticmethod
    def display_error(error: str):
        """Display error message.

        Args:
            error: Error message to display
        """
        print("\n" + "=" * 80)
        print("  ❌ ERROR")
        print("=" * 80)
        print(f"\n{error}")
        print("\n" + "=" * 80 + "\n")
