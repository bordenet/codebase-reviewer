"""Dashboard generation for team metrics and visualization."""

from typing import List, Dict
from pathlib import Path


class DashboardGenerator:
    """Generates HTML dashboards for team metrics."""
    
    def __init__(self):
        """Initialize dashboard generator."""
        pass
    
    def generate_multi_repo_dashboard(self, repo_analyses: List[dict], aggregate: dict, output_path: Path) -> None:
        """Generate multi-repository dashboard.
        
        Args:
            repo_analyses: List of repository analyses
            aggregate: Aggregate metrics
            output_path: Path to save dashboard HTML
        """
        html = self._generate_html(repo_analyses, aggregate)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def _generate_html(self, repo_analyses: List[dict], aggregate: dict) -> str:
        """Generate HTML for dashboard.
        
        Args:
            repo_analyses: List of repository analyses
            aggregate: Aggregate metrics
            
        Returns:
            HTML string
        """
        # Generate repository cards
        repo_cards = []
        for repo in sorted(repo_analyses, key=lambda r: r['total_issues'], reverse=True):
            severity_class = self._get_severity_class(repo['total_issues'])
            
            card = f"""
            <div class="repo-card {severity_class}">
                <h3>{repo['repo_name']}</h3>
                <div class="metrics">
                    <div class="metric">
                        <span class="label">Total Issues</span>
                        <span class="value">{repo['total_issues']}</span>
                    </div>
                    <div class="metric">
                        <span class="label">Critical</span>
                        <span class="value critical">{repo['critical_issues']}</span>
                    </div>
                    <div class="metric">
                        <span class="label">High</span>
                        <span class="value high">{repo['high_issues']}</span>
                    </div>
                    <div class="metric">
                        <span class="label">Medium</span>
                        <span class="value medium">{repo['medium_issues']}</span>
                    </div>
                    <div class="metric">
                        <span class="label">Low</span>
                        <span class="value low">{repo['low_issues']}</span>
                    </div>
                </div>
                <div class="breakdown">
                    <span>🔒 Security: {repo['security_issues']}</span>
                    <span>📊 Quality: {repo['quality_issues']}</span>
                </div>
            </div>
            """
            repo_cards.append(card)
        
        # Generate aggregate summary
        summary = f"""
        <div class="summary">
            <h2>Aggregate Metrics</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <span class="summary-label">Total Repositories</span>
                    <span class="summary-value">{aggregate['total_repos']}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Total Issues</span>
                    <span class="summary-value">{aggregate['total_issues']}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Critical Issues</span>
                    <span class="summary-value critical">{aggregate['total_critical']}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Avg Issues/Repo</span>
                    <span class="summary-value">{aggregate['avg_issues_per_repo']:.1f}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Worst Repository</span>
                    <span class="summary-value">{aggregate['worst_repo']}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Best Repository</span>
                    <span class="summary-value">{aggregate['best_repo']}</span>
                </div>
            </div>
        </div>
        """
        
        # Complete HTML
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Repository Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #2c3e50; margin-bottom: 30px; font-size: 2.5em; }}
        .summary {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 30px; }}
        .summary h2 {{ color: #34495e; margin-bottom: 20px; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
        .summary-item {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        .summary-label {{ display: block; color: #7f8c8d; font-size: 0.9em; margin-bottom: 8px; }}
        .summary-value {{ display: block; font-size: 1.8em; font-weight: bold; color: #2c3e50; }}
        .summary-value.critical {{ color: #e74c3c; }}
        .repos-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }}
        .repo-card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #3498db; }}
        .repo-card.high-risk {{ border-left-color: #e74c3c; }}
        .repo-card.medium-risk {{ border-left-color: #f39c12; }}
        .repo-card.low-risk {{ border-left-color: #27ae60; }}
        .repo-card h3 {{ color: #2c3e50; margin-bottom: 15px; font-size: 1.3em; }}
        .metrics {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 15px; }}
        .metric {{ display: flex; justify-content: space-between; padding: 8px; background: #f8f9fa; border-radius: 6px; }}
        .metric .label {{ color: #7f8c8d; font-size: 0.9em; }}
        .metric .value {{ font-weight: bold; color: #2c3e50; }}
        .metric .value.critical {{ color: #e74c3c; }}
        .metric .value.high {{ color: #e67e22; }}
        .metric .value.medium {{ color: #f39c12; }}
        .metric .value.low {{ color: #95a5a6; }}
        .breakdown {{ display: flex; justify-content: space-around; padding-top: 15px; border-top: 1px solid #ecf0f1; color: #7f8c8d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 Multi-Repository Dashboard</h1>
        {summary}
        <h2 style="color: #2c3e50; margin-bottom: 20px;">Repository Details</h2>
        <div class="repos-grid">
            {''.join(repo_cards)}
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def _get_severity_class(self, total_issues: int) -> str:
        """Get CSS class based on issue count.
        
        Args:
            total_issues: Total number of issues
            
        Returns:
            CSS class name
        """
        if total_issues >= 50:
            return 'high-risk'
        elif total_issues >= 20:
            return 'medium-risk'
        else:
            return 'low-risk'

