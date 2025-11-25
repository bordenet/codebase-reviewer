"""Tests for enterprise module."""

import pytest
from pathlib import Path
from codebase_reviewer.enterprise.multi_repo_analyzer import MultiRepoAnalyzer, RepoAnalysis, AggregateMetrics
from codebase_reviewer.enterprise.dashboard_generator import DashboardGenerator


class TestMultiRepoAnalyzer:
    """Tests for MultiRepoAnalyzer."""
    
    def test_initialization(self):
        """Test multi-repo analyzer initialization."""
        analyzer = MultiRepoAnalyzer(max_workers=2)
        assert analyzer.max_workers == 2
        assert analyzer.repo_analyses == []
    
    def test_get_aggregate_metrics_empty(self):
        """Test aggregate metrics with no analyses."""
        analyzer = MultiRepoAnalyzer()
        metrics = analyzer.get_aggregate_metrics()
        
        assert metrics.total_repos == 0
        assert metrics.total_issues == 0
        assert metrics.avg_issues_per_repo == 0.0
        assert metrics.worst_repo is None
        assert metrics.best_repo is None
    
    def test_get_aggregate_metrics_with_data(self):
        """Test aggregate metrics with sample data."""
        analyzer = MultiRepoAnalyzer()
        
        # Add sample analyses
        analyzer.repo_analyses = [
            RepoAnalysis(
                repo_name='repo1',
                repo_path='/path/to/repo1',
                total_issues=10,
                critical_issues=2,
                high_issues=3,
                medium_issues=3,
                low_issues=2,
                security_issues=5,
                quality_issues=5,
                total_files=50,
                total_lines=5000,
                languages={'python': 80.0, 'javascript': 20.0},
                frameworks=['Django']
            ),
            RepoAnalysis(
                repo_name='repo2',
                repo_path='/path/to/repo2',
                total_issues=20,
                critical_issues=5,
                high_issues=5,
                medium_issues=5,
                low_issues=5,
                security_issues=10,
                quality_issues=10,
                total_files=100,
                total_lines=10000,
                languages={'javascript': 100.0},
                frameworks=['React']
            ),
        ]
        
        metrics = analyzer.get_aggregate_metrics()
        
        assert metrics.total_repos == 2
        assert metrics.total_issues == 30
        assert metrics.total_critical == 7
        assert metrics.total_high == 8
        assert metrics.total_medium == 8
        assert metrics.total_low == 7
        assert metrics.total_security == 15
        assert metrics.total_quality == 15
        assert metrics.avg_issues_per_repo == 15.0
        assert metrics.worst_repo == 'repo2'
        assert metrics.best_repo == 'repo1'
    
    def test_repo_analysis_to_dict(self):
        """Test RepoAnalysis to_dict conversion."""
        analysis = RepoAnalysis(
            repo_name='test-repo',
            repo_path='/path/to/repo',
            total_issues=5,
            critical_issues=1,
            high_issues=1,
            medium_issues=2,
            low_issues=1,
            security_issues=2,
            quality_issues=3,
            total_files=25,
            total_lines=2500,
            languages={'python': 100.0},
            frameworks=['Flask']
        )
        
        data = analysis.to_dict()
        
        assert data['repo_name'] == 'test-repo'
        assert data['total_issues'] == 5
        assert data['critical_issues'] == 1
        assert data['languages'] == {'python': 100.0}
        assert data['frameworks'] == ['Flask']


class TestDashboardGenerator:
    """Tests for DashboardGenerator."""
    
    def test_initialization(self):
        """Test dashboard generator initialization."""
        generator = DashboardGenerator()
        assert generator is not None
    
    def test_generate_multi_repo_dashboard(self, tmp_path):
        """Test generating multi-repo dashboard."""
        generator = DashboardGenerator()
        
        repo_analyses = [
            {
                'repo_name': 'repo1',
                'repo_path': '/path/to/repo1',
                'total_issues': 10,
                'critical_issues': 2,
                'high_issues': 3,
                'medium_issues': 3,
                'low_issues': 2,
                'security_issues': 5,
                'quality_issues': 5,
            },
            {
                'repo_name': 'repo2',
                'repo_path': '/path/to/repo2',
                'total_issues': 5,
                'critical_issues': 1,
                'high_issues': 1,
                'medium_issues': 2,
                'low_issues': 1,
                'security_issues': 2,
                'quality_issues': 3,
            },
        ]
        
        aggregate = {
            'total_repos': 2,
            'total_issues': 15,
            'total_critical': 3,
            'total_high': 4,
            'total_medium': 5,
            'total_low': 3,
            'total_security': 7,
            'total_quality': 8,
            'total_files': 75,
            'total_lines': 7500,
            'avg_issues_per_repo': 7.5,
            'worst_repo': 'repo1',
            'best_repo': 'repo2',
        }
        
        output_path = tmp_path / "dashboard.html"
        generator.generate_multi_repo_dashboard(repo_analyses, aggregate, output_path)
        
        assert output_path.exists()
        
        # Check content
        content = output_path.read_text()
        assert 'Multi-Repository Dashboard' in content
        assert 'repo1' in content
        assert 'repo2' in content
        assert 'Aggregate Metrics' in content
    
    def test_get_severity_class(self):
        """Test severity class determination."""
        generator = DashboardGenerator()
        
        assert generator._get_severity_class(100) == 'high-risk'
        assert generator._get_severity_class(30) == 'medium-risk'
        assert generator._get_severity_class(10) == 'low-risk'

