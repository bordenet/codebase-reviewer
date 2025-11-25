"""Multi-repository analysis for enterprise teams."""

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class RepoAnalysis:
    """Analysis results for a single repository."""

    repo_name: str
    repo_path: str
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    security_issues: int
    quality_issues: int
    total_files: int
    total_lines: int
    languages: Dict[str, float]
    frameworks: List[str]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "repo_name": self.repo_name,
            "repo_path": self.repo_path,
            "total_issues": self.total_issues,
            "critical_issues": self.critical_issues,
            "high_issues": self.high_issues,
            "medium_issues": self.medium_issues,
            "low_issues": self.low_issues,
            "security_issues": self.security_issues,
            "quality_issues": self.quality_issues,
            "total_files": self.total_files,
            "total_lines": self.total_lines,
            "languages": self.languages,
            "frameworks": self.frameworks,
        }


@dataclass
class AggregateMetrics:
    """Aggregate metrics across all repositories."""

    total_repos: int
    total_issues: int
    total_critical: int
    total_high: int
    total_medium: int
    total_low: int
    total_security: int
    total_quality: int
    total_files: int
    total_lines: int
    avg_issues_per_repo: float
    worst_repo: Optional[str]
    best_repo: Optional[str]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "total_repos": self.total_repos,
            "total_issues": self.total_issues,
            "total_critical": self.total_critical,
            "total_high": self.total_high,
            "total_medium": self.total_medium,
            "total_low": self.total_low,
            "total_security": self.total_security,
            "total_quality": self.total_quality,
            "total_files": self.total_files,
            "total_lines": self.total_lines,
            "avg_issues_per_repo": self.avg_issues_per_repo,
            "worst_repo": self.worst_repo,
            "best_repo": self.best_repo,
        }


class MultiRepoAnalyzer:
    """Analyzes multiple repositories and provides aggregate metrics."""

    def __init__(self, max_workers: int = 4):
        """Initialize multi-repo analyzer.

        Args:
            max_workers: Maximum number of parallel analysis workers
        """
        self.max_workers = max_workers
        self.repo_analyses: List[RepoAnalysis] = []

    def analyze_repos(self, repo_paths: List[Path], progress_callback=None) -> List[RepoAnalysis]:
        """Analyze multiple repositories in parallel.

        Args:
            repo_paths: List of repository paths to analyze
            progress_callback: Optional callback for progress updates

        Returns:
            List of repository analyses
        """
        from codebase_reviewer.analyzers.code import CodeAnalyzer

        self.repo_analyses = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all analysis tasks
            future_to_repo = {}
            for repo_path in repo_paths:
                future = executor.submit(self._analyze_single_repo, repo_path)
                future_to_repo[future] = repo_path

            # Collect results as they complete
            for future in as_completed(future_to_repo):
                repo_path = future_to_repo[future]
                try:
                    analysis = future.result()
                    self.repo_analyses.append(analysis)

                    if progress_callback:
                        progress_callback(f"Completed analysis of {analysis.repo_name}")
                except Exception as e:
                    if progress_callback:
                        progress_callback(f"Failed to analyze {repo_path}: {str(e)}")

        return self.repo_analyses

    def _analyze_single_repo(self, repo_path: Path) -> RepoAnalysis:
        """Analyze a single repository.

        Args:
            repo_path: Path to repository

        Returns:
            Repository analysis
        """
        from codebase_reviewer.analyzers.code import CodeAnalyzer

        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze(str(repo_path))

        # Extract metrics
        issues = analysis.quality_issues or []
        critical = len([i for i in issues if i.severity.value == "critical"])
        high = len([i for i in issues if i.severity.value == "high"])
        medium = len([i for i in issues if i.severity.value == "medium"])
        low = len([i for i in issues if i.severity.value == "low"])

        return RepoAnalysis(
            repo_name=repo_path.name,
            repo_path=str(repo_path),
            total_issues=len(issues),
            critical_issues=critical,
            high_issues=high,
            medium_issues=medium,
            low_issues=low,
            security_issues=len([i for i in issues if "SEC" in i.rule_id]),
            quality_issues=len([i for i in issues if "QUAL" in i.rule_id]),
            total_files=0,  # TODO: Extract from analysis
            total_lines=0,  # TODO: Extract from analysis
            languages={},  # TODO: Extract from analysis
            frameworks=[],  # TODO: Extract from analysis
        )

    def get_aggregate_metrics(self) -> AggregateMetrics:
        """Calculate aggregate metrics across all repositories.

        Returns:
            Aggregate metrics
        """
        if not self.repo_analyses:
            return AggregateMetrics(
                total_repos=0,
                total_issues=0,
                total_critical=0,
                total_high=0,
                total_medium=0,
                total_low=0,
                total_security=0,
                total_quality=0,
                total_files=0,
                total_lines=0,
                avg_issues_per_repo=0.0,
                worst_repo=None,
                best_repo=None,
            )

        total_issues = sum(r.total_issues for r in self.repo_analyses)
        total_critical = sum(r.critical_issues for r in self.repo_analyses)
        total_high = sum(r.high_issues for r in self.repo_analyses)
        total_medium = sum(r.medium_issues for r in self.repo_analyses)
        total_low = sum(r.low_issues for r in self.repo_analyses)

        # Find worst and best repos
        worst = max(self.repo_analyses, key=lambda r: r.total_issues)
        best = min(self.repo_analyses, key=lambda r: r.total_issues)

        return AggregateMetrics(
            total_repos=len(self.repo_analyses),
            total_issues=total_issues,
            total_critical=total_critical,
            total_high=total_high,
            total_medium=total_medium,
            total_low=total_low,
            total_security=sum(r.security_issues for r in self.repo_analyses),
            total_quality=sum(r.quality_issues for r in self.repo_analyses),
            total_files=sum(r.total_files for r in self.repo_analyses),
            total_lines=sum(r.total_lines for r in self.repo_analyses),
            avg_issues_per_repo=total_issues / len(self.repo_analyses),
            worst_repo=worst.repo_name,
            best_repo=best.repo_name,
        )
