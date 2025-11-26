"""Enterprise and compliance commands."""

import json
import sys
from pathlib import Path

import click

from codebase_reviewer.ai.query_interface import QueryInterface
from codebase_reviewer.analyzers.quality_checker import QualityChecker
from codebase_reviewer.compliance.compliance_reporter import ComplianceFramework, ComplianceReporter
from codebase_reviewer.enterprise.dashboard_generator import DashboardGenerator
from codebase_reviewer.enterprise.multi_repo_analyzer import MultiRepoAnalyzer
from codebase_reviewer.metrics.productivity_metrics import ProductivityTracker
from codebase_reviewer.metrics.roi_calculator import ROICalculator, ROIMetrics


def register_enterprise_commands(cli):
    """Register enterprise commands with the CLI group."""

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
            # Load or generate analysis results
            if results:
                with open(results, "r") as f:
                    data = json.load(f)
                    issues = data.get("issues", [])
            else:
                # Run analysis on current directory
                click.echo("📊 Analyzing current directory...")

                checker = QualityChecker()
                quality_issues = checker.analyze_quality(str(Path.cwd()))
                issues = [
                    {
                        "rule_id": issue.title,
                        "file_path": issue.source.split(":")[0] if ":" in issue.source else issue.source,
                        "line_number": int(issue.source.split(":")[1]) if ":" in issue.source else 0,
                        "severity": issue.severity.value,
                        "description": issue.description,
                    }
                    for issue in quality_issues
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
            dashboard_gen.generate_multi_repo_dashboard(
                [a.to_dict() for a in analyses], aggregate.to_dict(), Path(output)
            )

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
            click.echo(
                f"Period: {report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}"
            )
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
