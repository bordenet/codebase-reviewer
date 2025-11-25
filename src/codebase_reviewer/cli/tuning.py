"""Prompt tuning and evolution commands."""

import sys
from pathlib import Path

import click

from codebase_reviewer.tuning.runner import TuningRunner
from codebase_reviewer.metaprompt.generator import MetaPromptGenerator
from codebase_reviewer.phase2.generator import Phase2Generator, Phase2Tools
from codebase_reviewer.phase2.runner import Phase2Runner
from codebase_reviewer.phase2.validator import Phase2Validator
from codebase_reviewer.interactive.workflow import InteractiveWorkflow
from codebase_reviewer.llm.client import create_client, LLMProvider, LLMResponse
from codebase_reviewer.llm.code_extractor import CodeExtractor


def register_tuning_commands(cli):
    """Register tuning commands with the CLI group."""

    @cli.group()
    def tune():
        """Prompt tuning commands for systematic prompt improvement."""

    @tune.command("init")
    @click.option(
        "--output-dir",
        "-o",
        type=click.Path(),
        default="./prompt_tuning_results",
        help="Directory to save tuning results",
    )
    @click.option(
        "--num-tests",
        "-n",
        type=int,
        default=5,
        help="Number of test cases to generate",
    )
    @click.option(
        "--project",
        "-p",
        type=str,
        default="codebase_reviewer",
        help="Project name",
    )
    def tune_init(output_dir, num_tests, project):
        """Initialize a new prompt tuning session."""
        runner = TuningRunner(Path(output_dir))
        session_dir = runner.run_full_tuning_workflow(
            project_name=project,
            num_test_cases=num_tests,
        )
        click.echo(f"\n✅ Tuning session initialized: {session_dir}")

    @tune.command("evaluate")
    @click.argument("session_dir", type=click.Path(exists=True))
    def tune_evaluate(session_dir):
        """Evaluate simulation results and generate recommendations."""
        runner = TuningRunner(Path(session_dir).parent)
        try:
            report_path = runner.evaluate_simulation_results(Path(session_dir))
            click.echo(f"\n✅ Evaluation complete: {report_path}")
        except FileNotFoundError as e:
            click.echo(f"\n❌ Error: {e}", err=True)
            sys.exit(1)

    @cli.command()
    @click.argument("codebase_path", type=click.Path(exists=True))
    @click.option(
        "--ai-response",
        type=click.Path(exists=True),
        help="Path to AI assistant's response (Phase 2 tool code)",
    )
    @click.option(
        "--llm-provider",
        type=click.Choice(["anthropic", "openai"]),
        default="anthropic",
        help="[API MODE] LLM provider to use (default: anthropic)",
    )
    @click.option(
        "--api-key",
        type=str,
        help="[API MODE] API key for LLM provider (or set ANTHROPIC_API_KEY/OPENAI_API_KEY env var)",
    )
    @click.option(
        "--model",
        type=str,
        help="[API MODE] Model to use (default: provider's default model)",
    )
    @click.option(
        "--output-dir",
        type=click.Path(),
        default="/tmp/codebase-reviewer",
        help="Base output directory (default: /tmp/codebase-reviewer)",
    )
    @click.option(
        "--phase1-prompt",
        type=click.Path(exists=True),
        help="Path to existing Phase 1 prompt (skip generation if provided)",
    )
    @click.option(
        "--auto-run",
        is_flag=True,
        help="Automatically run Phase 2 tools after generation",
    )
    @click.option(
        "--generation",
        type=int,
        default=1,
        help="Generation number (1, 2, 3, ...)",
    )
    @click.option(
        "--interactive/--no-interactive",
        default=True,
        help="Use interactive workflow with AI assistant (default: True)",
    )
    def evolve(
        codebase_path,
        ai_response,
        llm_provider,
        api_key,
        model,
        output_dir,
        phase1_prompt,
        auto_run,
        generation,
        interactive,
    ):
        """Generate self-evolving Phase 2 tools for a codebase.

        This is the MAIN MISSION command that works with YOUR AI ASSISTANT:

        INTERACTIVE MODE (default):
        1. Generates Phase 1 prompt
        2. YOU copy prompt to your AI assistant (Claude, ChatGPT, Augment, etc.)
        3. AI generates Phase 2 tool code
        4. YOU paste AI response back
        5. Tool compiles and validates Phase 2 tools
        6. Optionally runs tools to generate initial docs

        API MODE (--no-interactive):
        1. Generates Phase 1 prompt
        2. Automatically sends to LLM API
        3. Extracts Phase 2 tool code from response
        4. Compiles Phase 2 tools
        5. Optionally runs tools to generate initial docs

        Examples:
            # Interactive mode (recommended)
            review-codebase evolve /path/to/codebase --auto-run

            # With existing AI response
            review-codebase evolve /path/to/codebase \\
                --ai-response /tmp/ai-response.md \\
                --auto-run

            # API mode (requires API key)
            review-codebase evolve /path/to/codebase \\
                --no-interactive \\
                --llm-provider anthropic \\
                --api-key $ANTHROPIC_API_KEY \\
                --auto-run
        """
        try:
            codebase_path = Path(codebase_path).resolve()
            output_base = Path(output_dir)

            click.echo("=" * 70)
            click.echo("  🚀 CODEBASE REVIEWER - PHASE 2 TOOL GENERATION")
            click.echo("=" * 70)
            click.echo(f"Codebase: {codebase_path}")
            click.echo(f"Mode: {'Interactive (AI Assistant)' if interactive else f'API ({llm_provider})'}")
            click.echo(f"Output: {output_base}")
            click.echo(f"Generation: {generation}")
            click.echo("")

            # Step 1: Get Phase 1 prompt
            codebase_name = codebase_path.name

            if phase1_prompt:
                click.echo(f"📋 Using provided Phase 1 prompt: {phase1_prompt}")
                phase1_file = Path(phase1_prompt)
            else:
                click.echo("📋 Generating Phase 1 prompt...")
                click.echo("   (Using Go tool: ./bin/generate-docs)")

                # Check if Go tool exists
                go_tool = Path("./bin/generate-docs")
                if not go_tool.exists():
                    click.echo("❌ Error: Go tool not found. Run 'make build' first.")
                    sys.exit(1)

                # Run Go tool to generate prompt
                import subprocess

                result = subprocess.run([str(go_tool), str(codebase_path)], capture_output=True, text=True)

                if result.returncode != 0:
                    click.echo(f"❌ Error generating Phase 1 prompt: {result.stderr}")
                    sys.exit(1)

                # Read generated prompt
                phase1_file = Path(f"/tmp/codebase-reviewer/{codebase_name}/phase1-llm-prompt.md")

                if not phase1_file.exists():
                    click.echo(f"❌ Error: Prompt not generated at {phase1_file}")
                    sys.exit(1)

                click.echo(f"✅ Phase 1 prompt generated: {phase1_file}")

            # Step 2: Generate meta-prompt
            click.echo(f"\n📝 Generating meta-prompt for AI assistant...")
            meta_gen = MetaPromptGenerator()
            meta_prompt = meta_gen.generate(phase1_file, codebase_name, generation=generation)

            # Save meta-prompt
            meta_prompt_file = Path(f"/tmp/codebase-reviewer/{codebase_name}/meta-prompt-gen{generation}.md")
            meta_prompt_file.parent.mkdir(parents=True, exist_ok=True)
            meta_prompt_file.write_text(meta_prompt)
            click.echo(f"✅ Meta-prompt generated: {meta_prompt_file}")

            # Step 3: Get AI response (interactive or API mode)
            if interactive and not ai_response:
                # Interactive mode: Display prompt and wait for user
                InteractiveWorkflow.display_prompt(meta_prompt_file, codebase_name)

                click.echo("\n" + "=" * 70)
                click.echo("  ⏳ Waiting for AI response...")
                click.echo("=" * 70)
                click.echo("\nOptions:")
                click.echo("1. Paste AI response directly (then press Ctrl+D)")
                click.echo("2. Save to file and provide path")
                click.echo("\nPress Ctrl+C to cancel\n")

                ai_response_path = InteractiveWorkflow.wait_for_response(None)

            elif ai_response:
                # User provided AI response file
                ai_response_path = Path(ai_response)
                click.echo(f"\n📄 Using AI response from: {ai_response_path}")

            else:
                # API mode: Send to LLM automatically
                click.echo(f"\n🤖 Sending meta-prompt to {llm_provider}...")
                llm_client = create_client(llm_provider, api_key or "", model)
                click.echo(f"   Model: {llm_client.model}")

                response = llm_client.send_prompt(meta_prompt, max_tokens=16000, temperature=0.3)

                # Save response
                ai_response_path = Path(f"/tmp/codebase-reviewer/{codebase_name}/ai-response-gen{generation}.md")
                ai_response_path.write_text(response.content)
                click.echo(f"✅ AI response received: {ai_response_path}")
                click.echo(f"   Cost: ${response.cost_usd:.4f}")
                click.echo(f"   Tokens: {response.tokens_used:,}")

            # Step 4: Extract and compile Phase 2 tools
            click.echo(f"\n🔧 Extracting and compiling Phase 2 tools...")
            generator = Phase2Generator(output_base)

            # Read AI response
            ai_response_content = ai_response_path.read_text()

            # Create a mock LLM response for the generator
            mock_response = LLMResponse(
                content=ai_response_content,
                provider=LLMProvider.ANTHROPIC if not interactive else LLMProvider.ANTHROPIC,
                model="interactive" if interactive else llm_client.model,
                tokens_used=0,
                cost_usd=0.0,
                metadata={},
            )

            # Generate tools
            source_files = CodeExtractor.extract_go_files(ai_response_content)

            if not source_files:
                click.echo("❌ Error: No Go source files found in AI response")
                click.echo("   Make sure the AI response contains Go code blocks with file paths")
                sys.exit(1)

            # Create Phase2Tools object
            tools_dir = output_base / codebase_name / f"phase2-tools-gen{generation}"
            tools_dir.mkdir(parents=True, exist_ok=True)

            # Write source files
            for file_path, content in source_files.items():
                full_path = tools_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)
                click.echo(f"   ✓ {file_path}")

            # Compile tools
            binary_path = generator.compile_tools(
                Phase2Tools(
                    tools_dir=tools_dir,
                    binary_path=None,
                    source_files=source_files,
                    llm_response=mock_response,
                    generation=generation,
                )
            )

            phase2_tools = Phase2Tools(
                tools_dir=tools_dir,
                binary_path=binary_path,
                source_files=source_files,
                llm_response=mock_response,
                generation=generation,
            )

            # Step 5: Validate tools
            click.echo(f"\n✅ Validating Phase 2 tools...")
            validator = Phase2Validator()
            report = validator.validate_tools(phase2_tools.tools_dir, phase2_tools.binary_path)
            validator.print_report(report)

            if not report.is_valid:
                click.echo("❌ Validation failed - tools may not work correctly")
                sys.exit(1)

            # Step 6: Optionally run tools
            if auto_run:
                click.echo(f"\n🚀 Running Phase 2 tools to generate initial docs...")
                runner = Phase2Runner()
                run_result = runner.run_tools(phase2_tools.binary_path, codebase_path, verbose=True)

                if run_result.success:
                    click.echo(f"\n✅ Documentation generated: {run_result.output_dir}")
                else:
                    click.echo(f"\n❌ Tool execution failed")
                    click.echo(run_result.stderr)
                    sys.exit(1)

            # Summary
            InteractiveWorkflow.display_success(phase2_tools.tools_dir, phase2_tools.binary_path, codebase_path)

        except Exception as e:
            click.echo(f"\n❌ Error: {e}", err=True)
            import traceback

            traceback.print_exc()
            sys.exit(1)

