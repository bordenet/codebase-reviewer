"""Command-line interface for Codebase Reviewer."""

import json
import os
import sys
from pathlib import Path

import click

from codebase_reviewer.ai.fix_generator import FixGenerator
from codebase_reviewer.ai.query_interface import QueryInterface
from codebase_reviewer.analytics.hotspot_detector import HotspotDetector
from codebase_reviewer.analytics.risk_scorer import RiskScorer
from codebase_reviewer.analytics.trend_analyzer import MetricSnapshot, TrendAnalyzer
from codebase_reviewer.analyzers.code import CodeAnalyzer
from codebase_reviewer.compliance.compliance_reporter import ComplianceFramework, ComplianceReporter
from codebase_reviewer.enterprise.dashboard_generator import DashboardGenerator
from codebase_reviewer.enterprise.multi_repo_analyzer import MultiRepoAnalyzer
from codebase_reviewer.exporters.html_exporter import HTMLExporter
from codebase_reviewer.exporters.interactive_html_exporter import InteractiveHTMLExporter
from codebase_reviewer.exporters.json_exporter import JSONExporter
from codebase_reviewer.exporters.sarif_exporter import SARIFExporter
from codebase_reviewer.interactive.workflow import InteractiveWorkflow
from codebase_reviewer.llm.client import create_client
from codebase_reviewer.metaprompt.generator import MetaPromptGenerator
from codebase_reviewer.metrics.productivity_metrics import ProductivityTracker
from codebase_reviewer.metrics.roi_calculator import ROICalculator, ROIMetrics
from codebase_reviewer.orchestrator import AnalysisOrchestrator
from codebase_reviewer.phase2.generator import Phase2Generator
from codebase_reviewer.phase2.runner import Phase2Runner
from codebase_reviewer.phase2.validator import Phase2Validator
from codebase_reviewer.prompt_generator import PromptGenerator
from codebase_reviewer.simulation import LLMSimulator
from codebase_reviewer.tuning.runner import TuningRunner
from codebase_reviewer.prompts.generator_v2 import Phase1PromptGeneratorV2, ScanParameters
from codebase_reviewer.metrics.tracker import MetricsTracker
from codebase_reviewer.obsolescence.detector import ObsolescenceDetector
from codebase_reviewer.validation.schema_validator import SchemaValidator


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
def review(repo_path, output, prompts_output, format, workflow, quiet):  # pylint: disable=redefined-builtin
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
        from codebase_reviewer.llm.client import LLMProvider, LLMResponse

        mock_response = LLMResponse(
            content=ai_response_content,
            provider=LLMProvider.ANTHROPIC if not interactive else LLMProvider.ANTHROPIC,
            model="interactive" if interactive else llm_client.model,
            tokens_used=0,
            cost_usd=0.0,
            metadata={},
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
    type=click.Choice(["json", "html", "interactive-html", "sarif", "markdown"]),
    default="json",
    help="Output format (default: json)",
)
@click.option(
    "--with-analytics",
    is_flag=True,
    help="Include trend analysis, hotspot detection, and risk scoring",
)
@click.option(
    "--track-trends",
    is_flag=True,
    help="Record metrics for trend analysis",
)
def analyze(repo_path, output, format, with_analytics, track_trends):
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

        # Run analytics if requested
        analytics_data = {}
        if with_analytics or track_trends:
            click.echo("📊 Running analytics...")

            # Prepare data for analytics
            file_issues = {}
            file_metrics = {}
            all_issues = []

            if analysis.quality_issues:
                for issue in analysis.quality_issues:
                    file_path = issue.file_path
                    if file_path not in file_issues:
                        file_issues[file_path] = []
                    file_issues[file_path].append(
                        {
                            "id": issue.rule_id,
                            "severity": issue.severity.value,
                            "file_path": file_path,
                            "effort_minutes": 30,  # Default effort
                        }
                    )
                    all_issues.append(
                        {
                            "id": issue.rule_id,
                            "severity": issue.severity.value,
                            "file_path": file_path,
                            "effort_minutes": 30,
                        }
                    )

            # Hotspot detection
            if with_analytics:
                detector = HotspotDetector(Path(repo_path))
                hotspots = detector.detect_hotspots(file_issues, file_metrics)
                analytics_data["hotspots"] = [h.to_dict() for h in hotspots]

                if hotspots:
                    click.echo(f"  🔥 Found {len(hotspots)} hotspots")

                # Risk scoring
                scorer = RiskScorer()
                risk_scores = scorer.score_issues(all_issues, [h.to_dict() for h in hotspots])
                analytics_data["risk_scores"] = [r.to_dict() for r in risk_scores]

                quick_wins = [r for r in risk_scores if r.is_quick_win]
                if quick_wins:
                    click.echo(f"  ⚡ Found {len(quick_wins)} quick wins")

            # Trend tracking
            if track_trends:
                from datetime import datetime

                trend_analyzer = TrendAnalyzer()

                # Count issues by severity
                critical_count = len([i for i in all_issues if i["severity"] == "critical"])
                high_count = len([i for i in all_issues if i["severity"] == "high"])
                medium_count = len([i for i in all_issues if i["severity"] == "medium"])
                low_count = len([i for i in all_issues if i["severity"] == "low"])

                # Create snapshot
                snapshot = MetricSnapshot(
                    timestamp=datetime.now(),
                    total_issues=len(all_issues),
                    critical_issues=critical_count,
                    high_issues=high_count,
                    medium_issues=medium_count,
                    low_issues=low_count,
                    total_files=len(file_issues),
                    total_lines=sum(m.get("lines_of_code", 0) for m in file_metrics.values()),
                    security_issues=len([i for i in all_issues if "SEC" in i.get("id", "")]),
                    quality_issues=len([i for i in all_issues if "QUAL" in i.get("id", "")]),
                )

                trend_analyzer.record_snapshot(snapshot)
                trends = trend_analyzer.get_trends()

                if trends:
                    analytics_data["trends"] = [t.to_dict() for t in trends]
                    click.echo(f"  📈 Recorded metrics snapshot")

                    for trend in trends:
                        if trend.direction == "improving":
                            click.echo(f"  ✅ {trend.metric_name}: {trend.direction} ({trend.change_percent:+.1f}%)")
                        elif trend.direction == "degrading":
                            click.echo(f"  ⚠️  {trend.metric_name}: {trend.direction} ({trend.change_percent:+.1f}%)")

        # Add analytics to analysis object if present
        if analytics_data:
            analysis.analytics = analytics_data

        # Export based on format
        if format == "json":
            exporter = JSONExporter()
            exporter.export(analysis, output)
            click.echo(f"✅ JSON report saved to: {output}")

        elif format == "html":
            exporter = HTMLExporter()
            exporter.export(analysis, output, title=f"Code Analysis - {Path(repo_path).name}")
            click.echo(f"✅ HTML report saved to: {output}")

        elif format == "interactive-html":
            exporter = InteractiveHTMLExporter()
            exporter.export(
                analysis,
                output,
                title=f"Interactive Code Analysis - {Path(repo_path).name}",
            )
            click.echo(f"✅ Interactive HTML report saved to: {output}")
            click.echo(f"💡 Open in browser for filtering, search, and drill-down capabilities")

        elif format == "sarif":
            exporter = SARIFExporter()
            exporter.export(analysis, output, repository_root=repo_path)
            click.echo(f"✅ SARIF report saved to: {output}")

        elif format == "markdown":
            from codebase_reviewer.generators.documentation import DocumentationGenerator

            generator = DocumentationGenerator()
            markdown = generator.generate(analysis, repo_path)
            with open(output, "w", encoding="utf-8") as f:
                f.write(markdown)
            click.echo(f"✅ Markdown report saved to: {output}")

        # Print summary
        total_issues = len(analysis.quality_issues) if analysis.quality_issues else 0
        critical = (
            len([i for i in analysis.quality_issues if i.severity.value == "critical"])
            if analysis.quality_issues
            else 0
        )
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


@cli.command()
@click.argument("query", required=True)
@click.option(
    "--results",
    "-r",
    type=click.Path(exists=True),
    help="Path to analysis results JSON file (if not provided, analyzes current directory)",
)
def ask(query, results):
    """Ask natural language questions about code analysis results.

    This command provides a natural language interface for querying
    code analysis results. You can ask questions like:
    - "Show me all SQL injection vulnerabilities"
    - "Find all critical issues"
    - "What's the worst file?"

    Examples:
        codebase-reviewer ask "Show me all SQL injection vulnerabilities"
        codebase-reviewer ask "Find all critical issues" --results analysis.json
        codebase-reviewer ask "How many total issues?"
    """
    try:
        import json
        from pathlib import Path

        # Load or generate analysis results
        if results:
            with open(results, "r") as f:
                data = json.load(f)
                issues = data.get("issues", [])
        else:
            # Run analysis on current directory
            click.echo("📊 Analyzing current directory...")
            from codebase_reviewer.analyzers.quality_checker import QualityChecker

            checker = QualityChecker()
            analysis = checker.check_quality(Path.cwd())
            issues = [
                {
                    "rule_id": issue.rule_id,
                    "file_path": issue.file_path,
                    "line_number": issue.line_number,
                    "severity": issue.severity.value,
                    "description": issue.description,
                }
                for issue in analysis.quality_issues
            ]

        # Execute query
        query_interface = QueryInterface()
        result = query_interface.query(query, issues)

        if result["success"]:
            click.echo(click.style(f"\n✅ {result['message']}", fg="green"))

            # Display matched issues
            if result["issues"]:
                click.echo(f"\n📋 Results ({result['count']} issues):\n")
                for i, issue in enumerate(result["issues"][:10], 1):  # Show first 10
                    severity_color = {
                        "critical": "red",
                        "high": "yellow",
                        "medium": "blue",
                        "low": "white",
                    }.get(issue.get("severity", "low"), "white")

                    click.echo(
                        f"{i}. {click.style(issue.get('severity', 'unknown').upper(), fg=severity_color)} - {issue.get('file_path', 'unknown')}:{issue.get('line_number', 0)}"
                    )
                    click.echo(f"   {issue.get('description', 'No description')}")
                    click.echo()

                if result["count"] > 10:
                    click.echo(f"... and {result['count'] - 10} more issues")
        else:
            click.echo(click.style(f"\n❌ {result['message']}", fg="red"))
            click.echo("\n💡 Try one of these queries:")
            for suggestion in query_interface.get_suggestions()[:5]:
                click.echo(f"  - {suggestion}")

    except Exception as e:
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        import traceback

        traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("repos", nargs=-1, type=click.Path(exists=True), required=True)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    required=True,
    help="Output file path for dashboard HTML",
)
@click.option(
    "--workers",
    "-w",
    type=int,
    default=4,
    help="Number of parallel workers (default: 4)",
)
def multi_repo(repos, output, workers):
    """Analyze multiple repositories and generate aggregate dashboard.

    This command analyzes multiple repositories in parallel and generates
    a comprehensive dashboard with aggregate metrics and per-repo breakdowns.

    Examples:
        codebase-reviewer multi-repo /path/to/repo1 /path/to/repo2 --output dashboard.html
        codebase-reviewer multi-repo ~/projects/* --output team-dashboard.html --workers 8
    """
    try:
        click.echo(f"🏢 Analyzing {len(repos)} repositories...")
        click.echo(f"⚙️  Using {workers} parallel workers")

        # Convert to Path objects
        repo_paths = [Path(r) for r in repos]

        # Run multi-repo analysis
        analyzer = MultiRepoAnalyzer(max_workers=workers)

        def progress_callback(message):
            click.echo(f"  {message}")

        analyses = analyzer.analyze_repos(repo_paths, progress_callback=progress_callback)

        # Get aggregate metrics
        aggregate = analyzer.get_aggregate_metrics()

        # Generate dashboard
        dashboard_gen = DashboardGenerator()
        dashboard_gen.generate_multi_repo_dashboard([a.to_dict() for a in analyses], aggregate.to_dict(), Path(output))

        click.echo(f"\n✅ Dashboard saved to: {output}")

        # Print summary
        click.echo(f"\n📊 Summary:")
        click.echo(f"  Total repositories: {aggregate.total_repos}")
        click.echo(f"  Total issues: {aggregate.total_issues}")
        click.echo(f"  🔴 Critical: {aggregate.total_critical}")
        click.echo(f"  🟠 High: {aggregate.total_high}")
        click.echo(f"  🟡 Medium: {aggregate.total_medium}")
        click.echo(f"  ⚪ Low: {aggregate.total_low}")
        click.echo(f"\n  📈 Average issues per repo: {aggregate.avg_issues_per_repo:.1f}")
        click.echo(f"  🏆 Best repository: {aggregate.best_repo}")
        click.echo(f"  ⚠️  Worst repository: {aggregate.worst_repo}")

        # Exit code based on critical issues
        if aggregate.total_critical > 0:
            click.echo(
                click.style(
                    f"\n❌ Found {aggregate.total_critical} critical issues across repositories",
                    fg="red",
                )
            )
            sys.exit(1)
        else:
            click.echo(click.style("\n✅ No critical issues found", fg="green"))
            sys.exit(0)

    except Exception as e:
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        import traceback

        traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True))
@click.option(
    "--framework",
    "-f",
    type=click.Choice(["soc2", "hipaa", "pci_dss"], case_sensitive=False),
    required=True,
    help="Compliance framework to check against",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file for compliance report",
)
def compliance(repo_path, framework, output):
    """Generate compliance report (SOC2, HIPAA, PCI-DSS)."""
    try:
        click.echo(f"🔍 Analyzing {repo_path} for {framework.upper()} compliance...")

        # Run security analysis first
        from codebase_reviewer.analyzers.quality_checker import QualityChecker

        checker = QualityChecker()
        issues = checker.analyze_quality(repo_path)

        # Generate compliance report
        reporter = ComplianceReporter()
        framework_enum = ComplianceFramework(framework.lower())

        analysis_results = {"security_issues": issues}

        report = reporter.generate_report(framework_enum, analysis_results)

        # Display results
        click.echo(f"\n📊 {framework.upper()} Compliance Report")
        click.echo("=" * 60)
        click.echo(f"Total Controls: {report.total_controls}")
        click.echo(f"Passing Controls: {report.passing_controls}")
        click.echo(f"Failing Controls: {report.failing_controls}")
        click.echo(f"Compliance Score: {report.compliance_score:.1f}%")
        click.echo("=" * 60)

        if report.violations:
            click.echo(f"\n⚠️  Found {len(report.violations)} compliance violations:")
            for v in report.violations[:10]:  # Show first 10
                click.echo(f"\n  Control: {v.control.control_id} - {v.control.name}")
                click.echo(f"  File: {v.file_path}:{v.line_number}")
                click.echo(f"  Issue: {v.description}")

        # Save to file if requested
        if output:
            report_data = {
                "framework": framework.upper(),
                "total_controls": report.total_controls,
                "passing_controls": report.passing_controls,
                "failing_controls": report.failing_controls,
                "compliance_score": report.compliance_score,
                "violations": [
                    {
                        "control_id": v.control.control_id,
                        "control_name": v.control.name,
                        "file": v.file_path,
                        "line": v.line_number,
                        "description": v.description,
                        "remediation": v.remediation,
                    }
                    for v in report.violations
                ],
            }

            Path(output).write_text(json.dumps(report_data, indent=2))
            click.echo(f"\n✅ Compliance report saved to: {output}")

    except Exception as e:
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True))
@click.option(
    "--days",
    "-d",
    type=int,
    default=30,
    help="Number of days to analyze (default: 30)",
)
@click.option(
    "--author",
    "-a",
    help="Git author to filter by (default: all)",
)
def productivity(repo_path, days, author):
    """Generate developer productivity metrics."""
    try:
        click.echo(f"📊 Analyzing productivity for {repo_path} (last {days} days)...")

        tracker = ProductivityTracker(Path(repo_path))
        report = tracker.generate_report(days=days, author=author)

        # Display results
        click.echo(f"\n📈 Productivity Report")
        click.echo("=" * 60)
        click.echo(f"Period: {report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}")
        click.echo(f"Productivity Score: {report.productivity_score:.1f}/100")
        click.echo("=" * 60)

        click.echo(f"\n📝 Metrics:")
        click.echo(f"  Commits: {report.metrics.commits_count}")
        click.echo(f"  Files Changed: {report.metrics.files_changed}")
        click.echo(f"  Lines of Code: {report.metrics.lines_of_code}")
        click.echo(f"  Code Churn: {report.metrics.code_churn:.1f}%")

        if report.insights:
            click.echo(f"\n💡 Insights:")
            for insight in report.insights:
                click.echo(f"  • {insight}")

        if report.recommendations:
            click.echo(f"\n🎯 Recommendations:")
            for rec in report.recommendations:
                click.echo(f"  • {rec}")

    except Exception as e:
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--team-size",
    "-t",
    type=int,
    required=True,
    help="Team size (number of developers)",
)
@click.option(
    "--salary",
    "-s",
    type=float,
    required=True,
    help="Average developer salary (annual)",
)
@click.option(
    "--critical",
    type=int,
    default=0,
    help="Number of critical issues found",
)
@click.option(
    "--high",
    type=int,
    default=0,
    help="Number of high severity issues found",
)
@click.option(
    "--medium",
    type=int,
    default=0,
    help="Number of medium severity issues found",
)
@click.option(
    "--low",
    type=int,
    default=0,
    help="Number of low severity issues found",
)
@click.option(
    "--months",
    "-m",
    type=int,
    default=12,
    help="Number of months to calculate ROI for (default: 12)",
)
def roi(team_size, salary, critical, high, medium, low, months):
    """Calculate ROI for code analysis tool."""
    try:
        click.echo(f"💰 Calculating ROI for {months} months...")

        metrics = ROIMetrics(
            team_size=team_size,
            avg_developer_salary=salary,
            critical_issues_found=critical,
            high_issues_found=high,
            medium_issues_found=medium,
            low_issues_found=low,
        )

        calculator = ROICalculator()
        report = calculator.calculate_roi(metrics, months=months)

        # Display report
        text = calculator.generate_report_text(report)
        click.echo(f"\n{text}")

    except Exception as e:
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    default="/tmp/codebase-reviewer",
    help="Output directory for analysis results (default: /tmp/codebase-reviewer)",
)
@click.option(
    "--scan-mode",
    "-m",
    type=click.Choice(["review", "deep_scan", "scorch"]),
    default="review",
    help="Scan mode: review (quick), deep_scan (thorough), scorch (exhaustive)",
)
@click.option(
    "--exclude",
    "-e",
    multiple=True,
    help="Patterns to exclude (can be specified multiple times)",
)
@click.option(
    "--include",
    "-i",
    multiple=True,
    help="Patterns to include (can be specified multiple times)",
)
@click.option(
    "--languages",
    "-l",
    multiple=True,
    help="Languages to analyze (can be specified multiple times)",
)
@click.option("--quiet", "-q", is_flag=True, help="Suppress progress output")
def analyze_v2(repo_path, output_dir, scan_mode, exclude, include, languages, quiet):
    """Run Phase 1 analysis using v2.0 architecture (SECURITY: outputs to /tmp only)."""
    try:
        # Resolve absolute path
        repo_path = str(Path(repo_path).resolve())

        # Extract repo name for output directory
        repo_name = Path(repo_path).name
        output_path = os.path.join(output_dir, repo_name)

        if not quiet:
            click.echo(click.style(f"\n🔍 Codebase Reviewer v2.0 - Phase 1 Analysis\n", fg="cyan", bold=True))
            click.echo(f"  Target: {repo_path}")
            click.echo(f"  Mode: {scan_mode}")
            click.echo(f"  Output: {output_path}")
            click.echo("")

        # Security check: Ensure output is in /tmp
        if not output_path.startswith("/tmp/"):
            click.echo(
                click.style(
                    "⚠️  WARNING: Output directory must be in /tmp/ for security. Using /tmp/codebase-reviewer instead.",
                    fg="yellow",
                ),
                err=True,
            )
            output_path = f"/tmp/codebase-reviewer/{repo_name}"

        # Create scan parameters
        params = ScanParameters(
            target_path=repo_path,
            scan_mode=scan_mode,
            output_path=output_path,
            exclude_patterns=list(exclude) if exclude else None,
            include_patterns=list(include) if include else None,
            languages=list(languages) if languages else None,
        )

        # Generate Phase 1 prompt
        if not quiet:
            click.echo("📝 Generating Phase 1 prompt...")

        generator = Phase1PromptGeneratorV2()
        prompt = generator.generate_prompt(params)
        prompt_file = generator.save_prompt(prompt, output_path)

        if not quiet:
            click.echo(click.style(f"✓ Prompt saved: {prompt_file}", fg="green"))
            click.echo("")
            click.echo("📊 Next steps:")
            click.echo(f"  1. Review the prompt: {prompt_file}")
            click.echo(f"  2. Send to LLM for analysis")
            click.echo(f"  3. Save LLM response to: {output_path}/phase1_response.json")
            click.echo(f"  4. Validate response with: codebase-reviewer validate-v2 {output_path}")
            click.echo("")

        # Initialize metrics tracker
        metrics_tracker = MetricsTracker(repo_name, output_path)

        # Scan the codebase to collect initial metrics
        if not quiet:
            click.echo("📈 Collecting initial metrics...")

        # Count files
        total_files = 0
        for root, _, files in os.walk(repo_path):
            # Skip common ignore patterns
            if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']):
                continue
            total_files += len(files)

        metrics_tracker.update_coverage(
            files_total=total_files,
            files_analyzed=0,  # Will be updated after LLM analysis
            files_documented=0,
        )

        metrics_tracker.save()

        if not quiet:
            click.echo(click.style(f"✓ Metrics initialized: {total_files} files found", fg="green"))
            click.echo("")

        click.echo(click.style("✅ Phase 1 prompt generation complete!", fg="green", bold=True))
        click.echo(f"📁 All outputs saved to: {output_path}")

    except Exception as e:
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
        import traceback
        if not quiet:
            traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
