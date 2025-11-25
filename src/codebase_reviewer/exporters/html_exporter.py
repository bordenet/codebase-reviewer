"""HTML exporter for analysis results."""

from typing import List

from ..models import CodeAnalysis, Issue


class HTMLExporter:
    """Export analysis results to HTML format."""

    def export(
        self,
        analysis: CodeAnalysis,
        output_path: str,
        title: str = "Code Analysis Report",
    ) -> None:
        """Export analysis to HTML file.

        Args:
            analysis: Code analysis results
            output_path: Path to output HTML file
            title: Report title
        """
        html = self.to_html(analysis, title)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    def to_html(
        self, analysis: CodeAnalysis, title: str = "Code Analysis Report"
    ) -> str:
        """Convert analysis to HTML.

        Args:
            analysis: Code analysis results
            title: Report title

        Returns:
            HTML string
        """
        issues = analysis.quality_issues if analysis.quality_issues else []

        # Calculate summary stats
        total_files = (
            sum(lang.file_count for lang in analysis.structure.languages)
            if analysis.structure and analysis.structure.languages
            else 0
        )
        total_issues = len(issues)
        critical_count = len([i for i in issues if i.severity.value == "critical"])
        high_count = len([i for i in issues if i.severity.value == "high"])
        medium_count = len([i for i in issues if i.severity.value == "medium"])
        low_count = len([i for i in issues if i.severity.value == "low"])

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .metric-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .issues {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .issue {{
            border-left: 4px solid #ddd;
            padding: 15px;
            margin-bottom: 15px;
            background: #f9f9f9;
        }}
        .issue.critical {{ border-left-color: #dc3545; }}
        .issue.high {{ border-left-color: #fd7e14; }}
        .issue.medium {{ border-left-color: #ffc107; }}
        .issue.low {{ border-left-color: #28a745; }}
        .issue-title {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .issue-location {{
            color: #666;
            font-size: 0.9em;
            font-family: monospace;
        }}
        .severity-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 10px;
        }}
        .severity-critical {{ background: #dc3545; color: white; }}
        .severity-high {{ background: #fd7e14; color: white; }}
        .severity-medium {{ background: #ffc107; color: black; }}
        .severity-low {{ background: #28a745; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>Comprehensive code analysis report</p>
    </div>

    <div class="summary">
        <div class="metric">
            <div class="metric-value">{total_files}</div>
            <div class="metric-label">Total Files</div>
        </div>
        <div class="metric">
            <div class="metric-value">{total_issues}</div>
            <div class="metric-label">Total Issues</div>
        </div>
        <div class="metric">
            <div class="metric-value">{critical_count}</div>
            <div class="metric-label">Critical Issues</div>
        </div>
        <div class="metric">
            <div class="metric-value">{high_count}</div>
            <div class="metric-label">High Issues</div>
        </div>
    </div>

    <div class="issues">
        <h2>Issues Found</h2>
"""

        # Add issues
        for issue in issues[:100]:  # Limit to 100 issues for performance
            severity_class = issue.severity.value
            html += f"""
        <div class="issue {severity_class}">
            <div class="issue-title">
                <span class="severity-badge severity-{severity_class}">{severity_class.upper()}</span>
                {self._escape_html(issue.title)}
            </div>
            <div class="issue-location">{self._escape_html(issue.source)}</div>
            <div>{self._escape_html(issue.description.split(chr(10))[0])}</div>
        </div>
"""

        html += """
    </div>
</body>
</html>
"""
        return html

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )
