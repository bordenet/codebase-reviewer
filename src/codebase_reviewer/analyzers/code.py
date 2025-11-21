"""Code analyzer - analyzes repository code structure and quality."""

import os
from pathlib import Path

from codebase_reviewer.analyzers.dependency_parser import DependencyParser
from codebase_reviewer.analyzers.language_detector import LanguageDetector
from codebase_reviewer.analyzers.quality_checker import QualityChecker
from codebase_reviewer.models import CodeAnalysis, CodeStructure, DirectoryTree


class CodeAnalyzer:
    """Analyzes repository code structure, patterns, and quality."""

    def __init__(self):
        """Initialize the code analyzer with helper components."""
        self.language_detector = LanguageDetector()
        self.dependency_parser = DependencyParser()
        self.quality_checker = QualityChecker()

    def analyze(self, repo_path: str) -> CodeAnalysis:
        """Analyze code in repository.

        Args:
            repo_path: Path to repository root

        Returns:
            CodeAnalysis with code metrics and findings
        """
        # Analyze structure
        structure = self._analyze_structure(repo_path)

        # Analyze dependencies
        dependencies = self.dependency_parser.analyze_dependencies(repo_path, structure)

        # Basic quality metrics
        quality_issues = self.quality_checker.analyze_quality(repo_path)

        return CodeAnalysis(
            structure=structure,
            dependencies=dependencies,
            complexity_metrics={},
            quality_issues=quality_issues,
        )

    def _analyze_structure(self, repo_path: str) -> CodeStructure:
        """Analyze code structure.

        Args:
            repo_path: Path to repository root

        Returns:
            CodeStructure with languages, frameworks, and entry points
        """
        # Detect languages
        languages = self.language_detector.detect_languages(repo_path)

        # Detect frameworks
        frameworks = self.language_detector.detect_frameworks(repo_path)

        # Find entry points
        entry_points = self.language_detector.find_entry_points(repo_path, languages)

        # Build directory tree
        directory_tree = self._build_directory_tree(repo_path)

        return CodeStructure(
            languages=languages,
            frameworks=frameworks,
            entry_points=entry_points,
            directory_tree=directory_tree,
        )

    def _build_directory_tree(self, repo_path: str) -> DirectoryTree:
        """Build directory structure representation.

        Args:
            repo_path: Path to repository root

        Returns:
            DirectoryTree with file and directory counts
        """
        total_files = 0
        total_dirs = 0

        for root, dirs, files in os.walk(repo_path):
            if any(skip in root for skip in [".git", "node_modules", ".venv", "__pycache__"]):
                continue
            total_dirs += len(dirs)
            total_files += len(files)

        return DirectoryTree(
            root=repo_path,
            total_files=total_files,
            total_dirs=total_dirs,
            structure={},
        )
