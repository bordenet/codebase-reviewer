"""Enterprise features for multi-repo analysis and team dashboards."""

from .dashboard_generator import DashboardGenerator
from .multi_repo_analyzer import MultiRepoAnalyzer

__all__ = ["MultiRepoAnalyzer", "DashboardGenerator"]
