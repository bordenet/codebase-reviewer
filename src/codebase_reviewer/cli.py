"""Command-line interface for Codebase Reviewer."""

import json
import sys
from pathlib import Path
import os

import click

from codebase_reviewer.orchestrator import AnalysisOrchestrator
from codebase_reviewer.prompt_generator import PromptGenerator
from codebase_reviewer.simulation import LLMSimulator
from codebase_reviewer.tuning.runner import TuningRunner
from codebase_reviewer.llm.client import create_client
from codebase_reviewer.phase2.generator import Phase2Generator
from codebase_reviewer.phase2.runner import Phase2Runner
from codebase_reviewer.phase2.validator import Phase2Validator
from codebase_reviewer.interactive.workflow import InteractiveWorkflow
from codebase_reviewer.metaprompt.generator import MetaPromptGenerator
from codebase_reviewer.analyzers.code import CodeAnalyzer
from codebase_reviewer.exporters.json_exporter import JSONExporter
from codebase_reviewer.exporters.html_exporter import HTMLExporter
from codebase_reviewer.exporters.sarif_exporter import SARIFExporter


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Codebase Reviewer - AI-powered codebase analysis and onboarding tool."""


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file for analysis results (JSON)",
)
@click.option(
    "--prompts-output",
    "-p",
    type=click.Path(),
    help="Output file for generated prompts (Markdown)",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "markdown", "both"]),
    default="both",
    help="Output format for prompts",
)
@click.option(
    "--workflow",
    "-w",
    type=str,
    default="default",
    help="Workflow to use (default, reviewer_criteria, etc.)",
)
@click.option("--quiet", "-q", is_flag=True, help="Suppress progress output")
def analyze(repo_path, output, prompts_output, format, workflow, quiet):  # pylint: disable=redefined-builtin
    """Analyze a codebase and generate AI review prompts."""
    try:
        # Resolve absolute path
        repo_path = str(Path(repo_path).resolve())

        if not quiet:
            click.echo(
                click.style(
                    f"\nCodebase Reviewer - Analyzing: {repo_path}\n",
                    fg="cyan",
                    bold=True,
                )
            )

        # Run analysis
        orchestrator = AnalysisOrchestrator()

        def progress_callback(message):
            if not quiet:
                click.echo(f"  {message}")

        analysis = orchestrator.run_full_analysis(repo_path, progress_callback=progress_callback, workflow=workflow)

        # Save analysis results if requested
        if output:
            output_data = {
                "repository_path": analysis.repository_path,
                "timestamp": analysis.timestamp.isoformat(),
                "duration_seconds": analysis.analysis_duration_seconds,
                "documentation": {
                    "total_docs": len(analysis.documentation.discovered_docs) if analysis.documentation else 0,
                    "completeness_score": (analysis.documentation.completeness_score if analysis.documentation else 0),
                    "claims_count": (len(analysis.documentation.claims) if analysis.documentation else 0),
                },
                "code": {
                    "languages": [
                        {"name": l.name, "percentage": l.percentage}
                        for l in (
                            analysis.code.structure.languages if analysis.code and analysis.code.structure else []
                        )
                    ],
                    "frameworks": [
                        f.name
                        for f in (
                            analysis.code.structure.frameworks if analysis.code and analysis.code.structure else []
                        )
                    ],
                    "quality_issues_count": (len(analysis.code.quality_issues) if analysis.code else 0),
                },
                "validation": {
                    "drift_severity": (analysis.validation.drift_severity.value if analysis.validation else "unknown"),
                    "architecture_drift_count": (
                        len(analysis.validation.architecture_drift) if analysis.validation else 0
                    ),
                    "setup_drift_count": (len(analysis.validation.setup_drift) if analysis.validation else 0),
                },
                "prompts": {
                    "total_count": (len(analysis.prompts.all_prompts()) if analysis.prompts else 0),
                    "by_phase": {
                        f"phase{i}": (len(getattr(analysis.prompts, f"phase{i}")) if analysis.prompts else 0)
                        for i in range(5)
                    },
                },
            }

            with open(output, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2)

            if not quiet:
                click.echo(click.style(f"\n✓ Analysis results saved to: {output}", fg="green"))

        # Save prompts
        if analysis.prompts:
            prompt_gen = PromptGenerator()

            # Determine output file
            if not prompts_output:
                prompts_output = "prompts.md" if format != "json" else "prompts.json"

            if format in ["markdown", "both"]:
                md_output = prompts_output if prompts_output.endswith(".md") else f"{prompts_output}.md"
                markdown_content = prompt_gen.export_prompts_markdown(analysis.prompts)
                with open(md_output, "w", encoding="utf-8") as f:
                    f.write(markdown_content)

                if not quiet:
                    click.echo(click.style(f"✓ Prompts saved to: {md_output}", fg="green"))

            if format in ["json", "both"]:
                json_output = prompts_output if prompts_output.endswith(".json") else f"{prompts_output}.json"
                json_content = prompt_gen.export_prompts_json(analysis.prompts)
                with open(json_output, "w", encoding="utf-8") as f:
                    f.write(json_content)

                if not quiet:
                    click.echo(click.style(f"✓ Prompts saved to: {json_output}", fg="green"))

        # Display summary
        if not quiet:
            display_summary(analysis)

    except Exception as e:  # pylint: disable=broad-except
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        if not quiet:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def display_summary(analysis):
    """Display analysis summary."""
    click.echo(click.style("\n" + "=" * 60, fg="cyan"))
    click.echo(click.style("ANALYSIS SUMMARY", fg="cyan", bold=True))
    click.echo(click.style("=" * 60, fg="cyan"))

    # Documentation
    if analysis.documentation:
        click.echo(click.style("\nDocumentation:", fg="yellow", bold=True))
        click.echo(f"  Files found: {len(analysis.documentation.discovered_docs)}")
        click.echo(f"  Completeness: {analysis.documentation.completeness_score:.1f}%")
        click.echo(f"  Claims extracted: {len(analysis.documentation.claims)}")

        if analysis.documentation.claimed_architecture:
            arch = analysis.documentation.claimed_architecture
            if arch.pattern:
                click.echo(f"  Architecture: {arch.pattern}")

    # Code
    if analysis.code and analysis.code.structure:
        click.echo(click.style("\nCode Structure:", fg="yellow", bold=True))
        for lang in analysis.code.structure.languages[:5]:
            click.echo(f"  {lang.name}: {lang.percentage:.1f}%")

        if analysis.code.structure.frameworks:
            click.echo(f"  Frameworks: {', '.join(f.name for f in analysis.code.structure.frameworks)}")

        if analysis.code.quality_issues:
            click.echo(f"  Quality issues: {len(analysis.code.quality_issues)}")

    # Validation
    if analysis.validation:
        click.echo(click.style("\nValidation:", fg="yellow", bold=True))
        click.echo(f"  Drift severity: {analysis.validation.drift_severity.value.upper()}")
        drift_total = (
            len(analysis.validation.architecture_drift)
            + len(analysis.validation.setup_drift)
            + len(analysis.validation.api_drift)
        )
        click.echo(f"  Drift issues: {drift_total}")

        if analysis.validation.undocumented_features:
            click.echo(f"  Undocumented features: {len(analysis.validation.undocumented_features)}")

    # Prompts
    if analysis.prompts:
        click.echo(click.style("\nGenerated Prompts:", fg="yellow", bold=True))
        total = len(analysis.prompts.all_prompts())
        click.echo(f"  Total prompts: {total}")
        for phase in range(5):
            count = len(getattr(analysis.prompts, f"phase{phase}"))
            if count > 0:
                phase_names = {
                    0: "Documentation Review",
                    1: "Architecture Analysis",
                    2: "Implementation Deep-Dive",
                    3: "Development Workflow",
                    4: "Interactive Remediation",
                }
                click.echo(f"  Phase {phase} ({phase_names[phase]}): {count}")

    click.echo(
        click.style(
            f"\nCompleted in {analysis.analysis_duration_seconds:.2f} seconds\n",
            fg="green",
        )
    )


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True))
@click.option(
    "--phase",
    "-p",
    type=click.IntRange(0, 4),
    help="Show only specific phase (0-4)",
)
def prompts(repo_path, phase):
    """Generate and display prompts for a repository."""
    try:
        repo_path = str(Path(repo_path).resolve())

        click.echo(click.style(f"\nGenerating prompts for: {repo_path}\n", fg="cyan", bold=True))

        orchestrator = AnalysisOrchestrator()
        analysis = orchestrator.run_full_analysis(repo_path)

        if not analysis.prompts:
            click.echo(click.style("No prompts generated", fg="red"), err=True)
            sys.exit(1)

        # Display prompts
        phases_to_show = [phase] if phase is not None else range(5)

        for phase_num in phases_to_show:
            phase_prompts = getattr(analysis.prompts, f"phase{phase_num}")
            if not phase_prompts:
                continue

            phase_names = {
                0: "Documentation Review",
                1: "Architecture Analysis",
                2: "Implementation Deep-Dive",
                3: "Development Workflow",
                4: "Interactive Remediation",
            }

            click.echo(
                click.style(
                    f"\n{'=' * 60}\n" f"PHASE {phase_num}: {phase_names[phase_num]}\n" f"{'=' * 60}\n",
                    fg="cyan",
                    bold=True,
                )
            )

            for prompt in phase_prompts:
                click.echo(click.style(f"\n[{prompt.prompt_id}] {prompt.title}", bold=True))
                click.echo(f"\nObjective: {prompt.objective}\n")
                click.echo("Tasks:")
                for task in prompt.tasks:
                    click.echo(f"  • {task}")
                click.echo(f"\nDeliverable: {prompt.deliverable}\n")
                click.echo("-" * 60)

    except Exception as e:  # pylint: disable=broad-except
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--host",
    "-h",
    default="127.0.0.1",
    help="Host to bind to (default: 127.0.0.1)",
)
@click.option(
    "--port",
    "-p",
    default=3000,
    type=int,
    help="Port to bind to (default: 3000)",
)
@click.option("--debug", is_flag=True, help="Run in debug mode")
def web(host, port, debug):
    """Start the web interface."""
    try:
        from codebase_reviewer.web import run_server

        run_server(host=host, port=port, debug=debug)
    except ImportError as e:
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        click.echo("\nMake sure Flask is installed: pip install Flask")
        sys.exit(1)
    except Exception as e:  # pylint: disable=broad-except
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True))
@click.option(
    "--workflow",
    "-w",
    default="default",
    help="Workflow to use for simulation (default, reviewer_criteria, etc.)",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    help="Directory to save simulation results (default: ./simulation_results)",
)
def simulate(repo_path, workflow, output_dir):
    """Run LLM simulation to test and tune prompts.

    This command simulates running the prompts against a repository,
    allowing you to review and tune the prompt quality before using
    them with a real LLM.

    Example:
        codebase-reviewer simulate . --workflow reviewer_criteria
    """
    try:
        click.echo(click.style("\n🎯 Starting LLM Simulation", fg="cyan", bold=True))
        click.echo(f"Repository: {repo_path}")
        click.echo(f"Workflow: {workflow}")

        # Run simulation
        simulator = LLMSimulator(output_dir=output_dir)
        result = simulator.run_simulation(repo_path, workflow=workflow)

        # Print summary
        simulator.print_summary(result)

        click.echo(click.style("\n✅ Simulation complete!", fg="green", bold=True))
        click.echo(f"\nResults saved to: {simulator.output_dir}")
        click.echo("\nNext steps:")
        click.echo("1. Review the generated prompts in the markdown report")
        click.echo("2. Identify prompts that need improvement")
        click.echo("3. Update the prompt templates in src/codebase_reviewer/prompts/templates/")
        click.echo("4. Re-run the simulation to verify improvements")

    except Exception as e:  # pylint: disable=broad-except
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        import traceback

        traceback.print_exc()
        sys.exit(1)


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
    interactive
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
            result = subprocess.run(
                [str(go_tool), str(codebase_path)],
                capture_output=True,
                text=True
            )

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
        meta_prompt = meta_gen.generate(
            phase1_file,
            codebase_name,
            generation=generation
        )

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

            response = llm_client.send_prompt(
                meta_prompt,
                max_tokens=16000,
                temperature=0.3
            )

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
        from codebase_reviewer.llm.client import LLMResponse, LLMProvider
        mock_response = LLMResponse(
            content=ai_response_content,
            provider=LLMProvider.ANTHROPIC if not interactive else LLMProvider.ANTHROPIC,
            model="interactive" if interactive else llm_client.model,
            tokens_used=0,
            cost_usd=0.0,
            metadata={}
        )

        # Generate tools
        from codebase_reviewer.llm.code_extractor import CodeExtractor
        source_files = CodeExtractor.extract_go_files(ai_response_content)

        if not source_files:
            click.echo("❌ Error: No Go source files found in AI response")
            click.echo("   Make sure the AI response contains Go code blocks with file paths")
            sys.exit(1)

        # Create Phase2Tools object
        from codebase_reviewer.phase2.generator import Phase2Tools
        tools_dir = output_base / codebase_name / f"phase2-tools-gen{generation}"
        tools_dir.mkdir(parents=True, exist_ok=True)

        # Write source files
        for file_path, content in source_files.items():
            full_path = tools_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            click.echo(f"   ✓ {file_path}")

        # Compile tools
        binary_path = generator.compile_tools(Phase2Tools(
            tools_dir=tools_dir,
            binary_path=None,
            source_files=source_files,
            llm_response=mock_response,
            generation=generation
        ))

        phase2_tools = Phase2Tools(
            tools_dir=tools_dir,
            binary_path=binary_path,
            source_files=source_files,
            llm_response=mock_response,
            generation=generation
        )

        # Step 5: Validate tools
        click.echo(f"\n✅ Validating Phase 2 tools...")
        validator = Phase2Validator()
        report = validator.validate_tools(
            phase2_tools.tools_dir,
            phase2_tools.binary_path
        )
        validator.print_report(report)

        if not report.is_valid:
            click.echo("❌ Validation failed - tools may not work correctly")
            sys.exit(1)

        # Step 6: Optionally run tools
        if auto_run:
            click.echo(f"\n🚀 Running Phase 2 tools to generate initial docs...")
            runner = Phase2Runner()
            run_result = runner.run_tools(
                phase2_tools.binary_path,
                codebase_path,
                verbose=True
            )

            if run_result.success:
                click.echo(f"\n✅ Documentation generated: {run_result.output_dir}")
            else:
                click.echo(f"\n❌ Tool execution failed")
                click.echo(run_result.stderr)
                sys.exit(1)

        # Summary
        InteractiveWorkflow.display_success(
            phase2_tools.tools_dir,
            phase2_tools.binary_path,
            codebase_path
        )

    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    required=True,
    help="Output file path",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "html", "sarif", "markdown"]),
    default="json",
    help="Output format (default: json)",
)
def analyze(repo_path, output, format):
    """Run code analysis and export results in specified format.

    This command analyzes the codebase for security issues, code quality problems,
    and generates comprehensive reports in various formats.

    Examples:
        codebase-reviewer analyze . --output report.json --format json
        codebase-reviewer analyze /path/to/repo --output report.html --format html
        codebase-reviewer analyze . --output results.sarif --format sarif
    """
    try:
        click.echo(f"🔍 Analyzing codebase at: {repo_path}")
        click.echo(f"📊 Output format: {format}")

        # Run analysis
        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze(repo_path)

        # Export based on format
        if format == "json":
            exporter = JSONExporter()
            exporter.export(analysis, output)
            click.echo(f"✅ JSON report saved to: {output}")

        elif format == "html":
            exporter = HTMLExporter()
            exporter.export(analysis, output, title=f"Code Analysis - {Path(repo_path).name}")
            click.echo(f"✅ HTML report saved to: {output}")

        elif format == "sarif":
            exporter = SARIFExporter()
            exporter.export(analysis, output, repository_root=repo_path)
            click.echo(f"✅ SARIF report saved to: {output}")

        elif format == "markdown":
            from codebase_reviewer.generators.documentation import DocumentationGenerator
            generator = DocumentationGenerator()
            markdown = generator.generate(analysis, repo_path)
            with open(output, 'w', encoding='utf-8') as f:
                f.write(markdown)
            click.echo(f"✅ Markdown report saved to: {output}")

        # Print summary
        total_issues = len(analysis.quality_issues) if analysis.quality_issues else 0
        critical = len([i for i in analysis.quality_issues if i.severity.value == "critical"]) if analysis.quality_issues else 0
        high = len([i for i in analysis.quality_issues if i.severity.value == "high"]) if analysis.quality_issues else 0

        click.echo(f"\n📈 Summary:")
        click.echo(f"  Total issues: {total_issues}")
        click.echo(f"  🔴 Critical: {critical}")
        click.echo(f"  🟠 High: {high}")

        # Exit code based on critical issues
        if critical > 0:
            click.echo(click.style("\n❌ Quality gate failed: Critical issues found", fg="red"))
            sys.exit(1)
        else:
            click.echo(click.style("\n✅ Quality gate passed", fg="green"))
            sys.exit(0)

    except Exception as e:
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
