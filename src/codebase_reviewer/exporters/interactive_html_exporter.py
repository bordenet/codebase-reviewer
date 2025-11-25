"""Interactive HTML exporter with filtering, search, and drill-down capabilities."""

import json
from typing import Dict, List

from ..models import CodeAnalysis, Issue


class InteractiveHTMLExporter:
    """Export analysis results to interactive HTML format."""

    def export(
        self,
        analysis: CodeAnalysis,
        output_path: str,
        title: str = "Interactive Code Analysis Report",
    ) -> None:
        """Export analysis to interactive HTML file.

        Args:
            analysis: Code analysis results
            output_path: Path to output HTML file
            title: Report title
        """
        html = self.to_html(analysis, title)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    def to_html(self, analysis: CodeAnalysis, title: str = "Interactive Code Analysis Report") -> str:
        """Convert analysis to interactive HTML.

        Args:
            analysis: Code analysis results
            title: Report title

        Returns:
            HTML string
        """
        issues = analysis.quality_issues if analysis.quality_issues else []

        # Convert issues to JSON for JavaScript
        issues_json = json.dumps(
            [
                {
                    "id": i.title,
                    "file": i.source.split(":")[0] if ":" in i.source else i.source,
                    "line": i.source.split(":")[1] if ":" in i.source and len(i.source.split(":")) > 1 else "0",
                    "severity": i.severity.value,
                    "description": i.description,
                    "category": "security" if "SEC" in i.title else "quality",
                }
                for i in issues
            ]
        )

        # Calculate summary stats
        total_issues = len(issues)
        critical_count = len([i for i in issues if i.severity.value == "critical"])
        high_count = len([i for i in issues if i.severity.value == "high"])
        medium_count = len([i for i in issues if i.severity.value == "medium"])
        low_count = len([i for i in issues if i.severity.value == "low"])
        security_count = len([i for i in issues if "SEC" in i.title])
        quality_count = len([i for i in issues if "QUAL" in i.title])

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; font-size: 1.1em; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .controls {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .controls h2 {{ margin-bottom: 15px; color: #2c3e50; }}
        .filter-group {{ display: flex; gap: 15px; flex-wrap: wrap; margin-bottom: 15px; }}
        .filter-btn {{ padding: 10px 20px; border: 2px solid #e0e0e0; background: white; border-radius: 8px; cursor: pointer; transition: all 0.3s; font-size: 0.9em; }}
        .filter-btn:hover {{ border-color: #667eea; background: #f0f4ff; }}
        .filter-btn.active {{ border-color: #667eea; background: #667eea; color: white; }}
        .search-box {{ width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1em; }}
        .search-box:focus {{ outline: none; border-color: #667eea; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }}
        .stat-value {{ font-size: 2.5em; font-weight: bold; margin-bottom: 5px; }}
        .stat-label {{ color: #7f8c8d; font-size: 0.9em; }}
        .stat-card.critical .stat-value {{ color: #e74c3c; }}
        .stat-card.high .stat-value {{ color: #e67e22; }}
        .stat-card.medium .stat-value {{ color: #f39c12; }}
        .stat-card.low .stat-value {{ color: #95a5a6; }}
        .stat-card.security .stat-value {{ color: #e74c3c; }}
        .stat-card.quality .stat-value {{ color: #3498db; }}
        .issues-container {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .issue-card {{ padding: 15px; border-left: 4px solid #3498db; margin-bottom: 15px; background: #f8f9fa; border-radius: 8px; cursor: pointer; transition: all 0.3s; }}
        .issue-card:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.15); transform: translateY(-2px); }}
        .issue-card.critical {{ border-left-color: #e74c3c; }}
        .issue-card.high {{ border-left-color: #e67e22; }}
        .issue-card.medium {{ border-left-color: #f39c12; }}
        .issue-card.low {{ border-left-color: #95a5a6; }}
        .issue-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .issue-severity {{ padding: 4px 12px; border-radius: 20px; font-size: 0.85em; font-weight: bold; text-transform: uppercase; }}
        .issue-severity.critical {{ background: #e74c3c; color: white; }}
        .issue-severity.high {{ background: #e67e22; color: white; }}
        .issue-severity.medium {{ background: #f39c12; color: white; }}
        .issue-severity.low {{ background: #95a5a6; color: white; }}
        .issue-file {{ color: #7f8c8d; font-size: 0.9em; }}
        .issue-description {{ color: #2c3e50; margin-top: 8px; }}
        .no-results {{ text-align: center; padding: 40px; color: #7f8c8d; }}
        .hidden {{ display: none; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 {title}</h1>
        <p>Interactive code analysis with filtering and search</p>
    </div>

    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{total_issues}</div>
                <div class="stat-label">Total Issues</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-value">{critical_count}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-card high">
                <div class="stat-value">{high_count}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat-card medium">
                <div class="stat-value">{medium_count}</div>
                <div class="stat-label">Medium</div>
            </div>
            <div class="stat-card low">
                <div class="stat-value">{low_count}</div>
                <div class="stat-label">Low</div>
            </div>
            <div class="stat-card security">
                <div class="stat-value">{security_count}</div>
                <div class="stat-label">Security</div>
            </div>
            <div class="stat-card quality">
                <div class="stat-value">{quality_count}</div>
                <div class="stat-label">Quality</div>
            </div>
        </div>

        <div class="controls">
            <h2>🎛️ Filters & Search</h2>
            <div class="filter-group">
                <button class="filter-btn active" data-filter="all">All Issues</button>
                <button class="filter-btn" data-filter="critical">Critical</button>
                <button class="filter-btn" data-filter="high">High</button>
                <button class="filter-btn" data-filter="medium">Medium</button>
                <button class="filter-btn" data-filter="low">Low</button>
                <button class="filter-btn" data-filter="security">Security</button>
                <button class="filter-btn" data-filter="quality">Quality</button>
            </div>
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search by file name, description, or rule ID...">
        </div>

        <div class="issues-container">
            <div id="issuesList"></div>
            <div id="noResults" class="no-results hidden">
                <h3>No issues found</h3>
                <p>Try adjusting your filters or search query</p>
            </div>
        </div>
    </div>

    <script>
        const allIssues = {issues_json};
        let currentFilter = 'all';
        let currentSearch = '';

        function renderIssues() {{
            const issuesList = document.getElementById('issuesList');
            const noResults = document.getElementById('noResults');

            // Filter issues
            let filtered = allIssues.filter(issue => {{
                // Apply severity/category filter
                if (currentFilter !== 'all') {{
                    if (currentFilter === 'security' && issue.category !== 'security') return false;
                    if (currentFilter === 'quality' && issue.category !== 'quality') return false;
                    if (['critical', 'high', 'medium', 'low'].includes(currentFilter) && issue.severity !== currentFilter) return false;
                }}

                // Apply search filter
                if (currentSearch) {{
                    const searchLower = currentSearch.toLowerCase();
                    return issue.file.toLowerCase().includes(searchLower) ||
                           issue.description.toLowerCase().includes(searchLower) ||
                           issue.id.toLowerCase().includes(searchLower);
                }}

                return true;
            }});

            // Render
            if (filtered.length === 0) {{
                issuesList.innerHTML = '';
                noResults.classList.remove('hidden');
            }} else {{
                noResults.classList.add('hidden');
                issuesList.innerHTML = filtered.map(issue => `
                    <div class="issue-card ${{issue.severity}}">
                        <div class="issue-header">
                            <span class="issue-severity ${{issue.severity}}">${{issue.severity}}</span>
                            <span class="issue-file">${{issue.file}}:${{issue.line}}</span>
                        </div>
                        <div class="issue-description">
                            <strong>${{issue.id}}</strong>: ${{issue.description}}
                        </div>
                    </div>
                `).join('');
            }}
        }}

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                renderIssues();
            }});
        }});

        // Search box
        document.getElementById('searchBox').addEventListener('input', (e) => {{
            currentSearch = e.target.value;
            renderIssues();
        }});

        // Initial render
        renderIssues();
    </script>
</body>
</html>
"""

        return html
