"""Core CLI commands for codebase analysis."""

import sys
from pathlib import Path

import click

from codebase_reviewer.interactive.workflow import InteractiveWorkflow
from codebase_reviewer.orchestrator import AnalysisOrchestrator
from codebase_reviewer.prompt_generator import PromptGenerator


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


def register_core_commands(cli):
    """Register core commands with the CLI group."""

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
                from codebase_reviewer.exporters.json_exporter import JSONExporter

                exporter = JSONExporter(analysis)
                exporter.export_to_file(output)
                if not quiet:
                    click.echo(f"\nAnalysis results saved to: {output}")

            # Save prompts if requested
            if prompts_output:
                if format in ["markdown", "both"]:
                    with open(prompts_output, "w", encoding="utf-8") as f:
                        f.write(analysis.prompts.to_markdown())
                    if not quiet:
                        click.echo(f"Prompts saved to: {prompts_output}")

                if format in ["json", "both"]:
                    import json

                    json_path = (
                        prompts_output.replace(".md", ".json")
                        if prompts_output.endswith(".md")
                        else f"{prompts_output}.json"
                    )
                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(analysis.prompts.to_dict(), f, indent=2)
                    if not quiet:
                        click.echo(f"Prompts (JSON) saved to: {json_path}")

            # Display summary
            if not quiet:
                display_summary(analysis)

        except Exception as e:  # pylint: disable=broad-except
            click.echo(click.style(f"\nError: {str(e)}", fg="red"), err=True)
            if not quiet:
                import traceback

                traceback.print_exc()
            sys.exit(1)

    @cli.command()
    @click.argument("repo_path", type=click.Path(exists=True))
    @click.option(
        "--phase",
        "-p",
        type=int,
        help="Generate prompts for a specific phase (0-4)",
    )
    @click.option(
        "--workflow",
        "-w",
        type=str,
        default="default",
        help="Workflow to use",
    )
    @click.option(
        "--output",
        "-o",
        type=click.Path(),
        help="Output file (default: stdout)",
    )
    def prompts(repo_path, phase, workflow, output):
        """Generate AI prompts without full analysis."""
        try:
            repo_path = str(Path(repo_path).resolve())
            orchestrator = AnalysisOrchestrator()
            analysis = orchestrator.run_full_analysis(repo_path, workflow=workflow)

            if phase is not None:
                prompt_gen = PromptGenerator()
                prompt = prompt_gen.generator.generate(phase, analysis)
                content = prompt if isinstance(prompt, str) else str(prompt)
            else:
                content = analysis.prompts.to_markdown()

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                click.echo(f"Prompts saved to: {output}")
            else:
                click.echo(content)

        except Exception as e:  # pylint: disable=broad-except
            click.echo(click.style(f"\nError: {str(e)}", fg="red"), err=True)
            sys.exit(1)

    @cli.command()
    @click.option(
        "--host",
        "-h",
        default="127.0.0.1",
        help="Host to bind to",
    )
    @click.option(
        "--port",
        "-p",
        default=5000,
        type=int,
        help="Port to bind to",
    )
    @click.option("--debug", is_flag=True, help="Enable debug mode")
    def web(host, port, debug):
        """Launch interactive web interface."""
        from codebase_reviewer.web import app

        click.echo(f"Starting web interface at http://{host}:{port}")
        app.run(host=host, port=port, debug=debug)

    @cli.command()
    @click.argument("repo_path", type=click.Path(exists=True))
    @click.option(
        "--workflow",
        "-w",
        type=str,
        default="default",
        help="Workflow to use",
    )
    def simulate(repo_path, workflow):
        """Run interactive workflow simulation."""
        try:
            repo_path = str(Path(repo_path).resolve())
            click.echo(f"\nStarting interactive workflow for: {repo_path}\n")

            workflow_runner = InteractiveWorkflow(repo_path, workflow=workflow)
            workflow_runner.run()

            click.echo(click.style("\nWorkflow completed!", fg="green", bold=True))

        except KeyboardInterrupt:
            click.echo(click.style("\n\nWorkflow interrupted by user.", fg="yellow"))
            sys.exit(0)
        except Exception as e:  # pylint: disable=broad-except
            click.echo(click.style(f"\nError: {str(e)}", fg="red"), err=True)
            sys.exit(1)
