"""Analysis and query commands."""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import click

from codebase_reviewer.analytics.hotspot_detector import HotspotDetector
from codebase_reviewer.analytics.risk_scorer import RiskScorer
from codebase_reviewer.analytics.trend_analyzer import MetricSnapshot, TrendAnalyzer
from codebase_reviewer.analyzers.code import CodeAnalyzer
from codebase_reviewer.exporters.html_exporter import HTMLExporter
from codebase_reviewer.exporters.interactive_html_exporter import InteractiveHTMLExporter
from codebase_reviewer.exporters.json_exporter import JSONExporter
from codebase_reviewer.exporters.sarif_exporter import SARIFExporter
from codebase_reviewer.metrics.tracker import MetricsTracker
from codebase_reviewer.prompts.generator_v2 import Phase1PromptGeneratorV2, ScanParameters


def register_analysis_commands(cli):
    """Register analysis commands with the CLI group."""

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
            analytics_data: Dict[str, Any] = {}
            if with_analytics or track_trends:
                click.echo("📊 Running analytics...")

                # Prepare data for analytics
                file_issues: Dict[str, List[Dict[str, Any]]] = {}
                file_metrics: Dict[str, Dict[str, Any]] = {}
                all_issues: List[Dict[str, Any]] = []

                if analysis.quality_issues:
                    for issue in analysis.quality_issues:
                        # Extract file path from source (format: "file:line" or just "file")
                        file_path = issue.source.split(":")[0] if ":" in issue.source else issue.source
                        if file_path not in file_issues:
                            file_issues[file_path] = []
                        file_issues[file_path].append(
                            {
                                "id": issue.title,
                                "severity": issue.severity.value,
                                "file_path": file_path,
                                "effort_minutes": 30,  # Default effort
                            }
                        )
                        all_issues.append(
                            {
                                "id": issue.title,
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
                        total_lines=sum(int(m.get("lines_of_code", 0)) for m in file_metrics.values()),
                        security_issues=len([i for i in all_issues if "SEC" in str(i.get("id", ""))]),
                        quality_issues=len([i for i in all_issues if "QUAL" in str(i.get("id", ""))]),
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
                                click.echo(
                                    f"  ⚠️  {trend.metric_name}: {trend.direction} ({trend.change_percent:+.1f}%)"
                                )

            # Add analytics to analysis object if present
            if analytics_data:
                analysis.analytics = analytics_data

            # Export based on format
            if format == "json":
                json_exporter = JSONExporter()
                json_exporter.export(analysis, output)
                click.echo(f"✅ JSON report saved to: {output}")

            elif format == "html":
                html_exporter = HTMLExporter()
                html_exporter.export(analysis, output, title=f"Code Analysis - {Path(repo_path).name}")
                click.echo(f"✅ HTML report saved to: {output}")

            elif format == "interactive-html":
                interactive_exporter = InteractiveHTMLExporter()
                interactive_exporter.export(
                    analysis,
                    output,
                    title=f"Interactive Code Analysis - {Path(repo_path).name}",
                )
                click.echo(f"✅ Interactive HTML report saved to: {output}")
                click.echo(f"💡 Open in browser for filtering, search, and drill-down capabilities")

            elif format == "sarif":
                sarif_exporter = SARIFExporter()
                sarif_exporter.export(analysis, output, repository_root=repo_path)
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
            high = (
                len([i for i in analysis.quality_issues if i.severity.value == "high"])
                if analysis.quality_issues
                else 0
            )

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
            metrics_tracker = MetricsTracker(Path(repo_name), Path(output_path) if output_path else None)

            # Scan the codebase to collect initial metrics
            if not quiet:
                click.echo("📈 Collecting initial metrics...")

            # Count files
            total_files = 0
            for root, _, files in os.walk(repo_path):
                # Skip common ignore patterns
                if any(skip in root for skip in [".git", "node_modules", "__pycache__", ".venv", "venv"]):
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
