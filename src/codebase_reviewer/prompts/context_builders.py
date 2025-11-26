"""Context builders for prompt generation.

This module contains basic context builder functions that extract and format
data from RepositoryAnalysis for use in prompt templates.

For advanced context builders (observability, git analysis, etc.), see context_builders_advanced.py.
"""

import glob
import os
from typing import Any, Dict, Optional

from codebase_reviewer.models import RepositoryAnalysis, Severity
from codebase_reviewer.prompts.context_builders_advanced import AdvancedContextBuilders


class ContextBuilders:
    """Collection of basic context builder methods for prompt generation."""

    # ========== Phase 0: Documentation Review ==========

    @staticmethod
    def build_readme_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for README analysis prompt."""
        docs = analysis.documentation
        if not docs:
            return None

        readme_docs = [d for d in docs.discovered_docs if d.doc_type == "primary"]
        readme_content = readme_docs[0].content if readme_docs else "No README found"

        return {
            "readme_content": readme_content[:5000],
            "readme_path": readme_docs[0].path if readme_docs else "N/A",
            "total_docs_found": len(docs.discovered_docs),
        }

    @staticmethod
    def build_architecture_docs_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for architecture documentation prompt."""
        docs = analysis.documentation
        if not docs:
            return None

        arch_docs = [d for d in docs.discovered_docs if d.doc_type == "architecture"]
        if not arch_docs:
            return None

        return {
            "architecture_docs": [
                {"path": d.path, "content": d.content[:2000], "size_bytes": d.size_bytes} for d in arch_docs
            ],
            "claimed_architecture": (
                {
                    "pattern": docs.claimed_architecture.pattern,
                    "components": docs.claimed_architecture.components,
                }
                if docs.claimed_architecture
                else None
            ),
        }

    @staticmethod
    def build_setup_docs_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for setup documentation prompt."""
        docs = analysis.documentation
        if not docs or not docs.setup_instructions:
            return None

        setup = docs.setup_instructions
        # SetupGuide is a dataclass with list attributes
        setup_summary = {
            "prerequisites": setup.prerequisites[:10] if setup.prerequisites else [],
            "build_steps": setup.build_steps[:10] if setup.build_steps else [],
            "environment_vars": setup.environment_vars[:10] if setup.environment_vars else [],
        }

        return {
            "setup_instructions": setup_summary,
            "setup_completeness": docs.completeness_score,
            "has_prerequisites": bool(setup.prerequisites),
        }

    # ========== Phase 1: Architecture Analysis ==========

    @staticmethod
    def build_architecture_validation_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for architecture validation prompt."""
        docs = analysis.documentation
        code = analysis.code
        validation = analysis.validation

        if not docs or not code:
            return None

        # Extract claimed architecture
        claimed_arch = None
        if docs.claimed_architecture:
            claimed_arch = {
                "pattern": docs.claimed_architecture.pattern,
                "layers": docs.claimed_architecture.layers,
                "components": docs.claimed_architecture.components,
            }

        # Extract actual code structure
        actual_structure = None
        if code.structure:
            actual_structure = {
                "languages": [{"name": lang.name, "percentage": lang.percentage} for lang in code.structure.languages],
                "frameworks": [fw.name for fw in code.structure.frameworks],
                "entry_points": [ep.path for ep in code.structure.entry_points],
            }

        # Extract validation results
        validation_results = None
        if validation:
            validation_results = {
                "drift_severity": validation.drift_severity.value,
                "architecture_drift": [
                    {
                        "claim": d.claim.description if d.claim else "Unknown",
                        "status": d.validation_status.value,
                        "severity": d.severity.value,
                    }
                    for d in validation.architecture_drift[:10]
                ],
                "missing_components": [
                    d.claim.description for d in validation.architecture_drift if d.validation_status.value == "invalid"
                ],
            }

        return {
            "claimed_architecture": claimed_arch,
            "actual_structure": actual_structure,
            "validation_results": validation_results,
            "repository_path": analysis.repository_path,
        }

    @staticmethod
    def build_dependency_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for dependency analysis prompt."""
        code = analysis.code
        if not code or not code.dependencies:
            return None

        # DependencyInfo is a dataclass, extract relevant fields
        deps_summary = [
            {"name": dep.name, "version": dep.version, "type": dep.dependency_type} for dep in code.dependencies[:50]
        ]

        return {
            "dependencies": deps_summary,
            "dependency_count": len(code.dependencies),
            "has_lock_file": any("lock" in dep.source_file.lower() for dep in code.dependencies if dep.source_file),
        }

    # ========== Phase 2: Implementation Deep-Dive ==========

    @staticmethod
    def build_quality_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for code quality assessment prompt."""
        code = analysis.code
        if not code:
            return None

        quality_issues = code.quality_issues

        todos = [i for i in quality_issues if "TODO" in i.title or "FIXME" in i.title]
        security_issues = [i for i in quality_issues if i.severity == Severity.HIGH]

        return {
            "todo_count": len(todos),
            "sample_todos": [{"title": t.title, "description": t.description} for t in todos[:10]],
            "security_issues_count": len(security_issues),
            "sample_security_issues": [{"title": s.title, "description": s.description} for s in security_issues[:5]],
        }

    @staticmethod
    def build_observability_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for observability review prompt."""
        return AdvancedContextBuilders.build_observability_context(analysis)

    # ========== Phase 3: Development Workflow ==========

    @staticmethod
    def build_setup_validation_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for setup validation prompt."""
        return AdvancedContextBuilders.build_setup_validation_context(analysis)

    @staticmethod
    def build_testing_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for testing strategy prompt."""
        return AdvancedContextBuilders.build_testing_context(analysis)

    @staticmethod
    def build_cicd_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for CI/CD review prompt."""
        return {"repository_path": analysis.repository_path}

    # ========== Phase 4: Interactive Remediation ==========

    @staticmethod
    def build_remediation_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for interactive remediation prompt."""
        validation = analysis.validation
        code = analysis.code

        if not validation and not code:
            return None

        # Collect all issues
        all_issues = []

        if validation:
            all_issues.extend(
                [
                    {
                        "type": "architecture_drift",
                        "severity": r.validation_status.value,
                        "description": r.evidence,
                        "recommendation": r.recommendation,
                    }
                    for r in validation.architecture_drift
                ]
            )
            all_issues.extend(
                [
                    {
                        "type": "setup_drift",
                        "severity": r.validation_status.value,
                        "description": r.evidence,
                        "recommendation": r.recommendation,
                    }
                    for r in validation.setup_drift
                ]
            )

        if code:
            all_issues.extend(
                [
                    {
                        "type": "code_quality",
                        "severity": i.severity.value,
                        "description": i.description,
                        "source": i.source,
                    }
                    for i in code.quality_issues
                ]
            )

        return {
            "total_issues": len(all_issues),
            "issues_by_severity": {
                "high": len([i for i in all_issues if i.get("severity") == "high"]),
                "medium": len([i for i in all_issues if i.get("severity") == "medium"]),
                "low": len([i for i in all_issues if i.get("severity") == "low"]),
            },
            "top_issues": all_issues[:15],
        }

    # ========== Security Context Builders ==========

    @staticmethod
    def build_security_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for security vulnerability assessment."""
        return ContextBuilders.build_quality_context(analysis)

    @staticmethod
    def build_error_handling_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for error handling verification."""
        return ContextBuilders.build_quality_context(analysis)

    @staticmethod
    def build_dependency_security_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for dependency security audit."""
        return ContextBuilders.build_dependency_context(analysis)

    # ========== Architecture Insights Context Builders ==========

    @staticmethod
    def build_call_graph_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for call graph and dependency tracing."""
        return AdvancedContextBuilders.build_call_graph_context(analysis)

    @staticmethod
    def build_git_hotspots_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for git hotspots analysis."""
        return AdvancedContextBuilders.build_git_hotspots_context(analysis)

    @staticmethod
    def build_duplication_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for code duplication analysis."""
        return ContextBuilders.build_quality_context(analysis)

    @staticmethod
    def build_cohesion_coupling_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for cohesion and coupling analysis."""
        return ContextBuilders.build_architecture_validation_context(analysis)

    # ========== Strategy Context Builders ==========

    @staticmethod
    def build_documentation_strategy_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for living documentation strategy."""
        return ContextBuilders.build_architecture_docs_context(analysis)

    @staticmethod
    def build_observability_strategy_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for observability and instrumentation strategy."""
        return ContextBuilders.build_observability_context(analysis)

    @staticmethod
    def build_testing_strategy_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for test coverage and quality strategy."""
        return ContextBuilders.build_testing_context(analysis)

    @staticmethod
    def build_tech_debt_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for technical debt and refactoring roadmap."""
        return ContextBuilders.build_remediation_context(analysis)

    @staticmethod
    def build_mentorship_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for team mentorship and best practices guide."""
        return ContextBuilders.build_quality_context(analysis)
