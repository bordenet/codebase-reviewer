"""Unified prompt generator using template-based configuration."""

from typing import Any, Callable, Dict, List, Optional

from codebase_reviewer.models import Prompt, RepositoryAnalysis, Severity
from codebase_reviewer.prompts.template_loader import PromptTemplateLoader


class PhaseGenerator:
    """Generates prompts for any phase using templates and context builders."""

    def __init__(self):
        """Initialize the generator with template loader and context builders."""
        self.loader = PromptTemplateLoader()
        self._context_builders: Dict[str, Callable] = {}
        self._conditional_checkers: Dict[str, Callable] = {}
        self._register_context_builders()
        self._register_conditional_checkers()

    def generate(self, phase: int, analysis: RepositoryAnalysis) -> List[Prompt]:
        """Generate prompts for a specific phase.

        Args:
            phase: Phase number (0-4)
            analysis: Repository analysis results

        Returns:
            List of Prompt instances for the phase
        """
        # Phase-specific prerequisites
        if not self._check_phase_prerequisites(phase, analysis):
            return []

        templates = self.loader.load_phase_templates(phase)
        prompts: List[Prompt] = []

        for template in templates:
            # Check conditional requirements
            if template.conditional and not self._check_conditional(template.conditional, analysis):
                continue

            # Build context for this template
            context = self._build_context(template.id, analysis)
            if context is None:
                continue

            prompts.append(template.to_prompt(context, phase))

        return prompts

    def _check_phase_prerequisites(self, phase: int, analysis: RepositoryAnalysis) -> bool:
        """Check if phase prerequisites are met."""
        prerequisites = {
            0: lambda a: a.documentation is not None,
            1: lambda a: a.code is not None and a.documentation is not None,
            2: lambda a: a.code is not None,
            3: lambda a: a.documentation is not None and a.validation is not None,
            4: lambda a: True,  # Phase 4 has no prerequisites
        }
        return prerequisites.get(phase, lambda a: True)(analysis)

    def _check_conditional(self, conditional: str, analysis: RepositoryAnalysis) -> bool:
        """Check if conditional requirement is met."""
        checker = self._conditional_checkers.get(conditional)
        if checker:
            return checker(analysis)
        return False

    def _build_context(self, template_id: str, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context dictionary for a template."""
        builder = self._context_builders.get(template_id)
        if builder:
            return builder(analysis)
        return {}

    def _register_conditional_checkers(self):
        """Register conditional checker functions."""
        self._conditional_checkers = {
            "has_architecture_docs": lambda a: (
                a.documentation and any(d.doc_type == "architecture" for d in a.documentation.discovered_docs)
            ),
            "has_setup_docs": lambda a: (a.documentation and a.documentation.setup_instructions is not None),
            "has_dependencies": lambda a: (a.code and a.code.dependencies is not None and len(a.code.dependencies) > 0),
        }

    def _register_context_builders(self):
        """Register context builder functions for each template."""
        self._context_builders = {
            # Phase 0: Documentation Review
            "0.1": self._build_readme_context,
            "0.2": self._build_architecture_docs_context,
            "0.3": self._build_setup_docs_context,
            # Phase 1: Architecture Analysis
            "1.1": self._build_architecture_validation_context,
            "1.2": self._build_dependency_context,
            # Phase 2: Implementation Deep-Dive
            "2.1": self._build_quality_context,
            "2.2": self._build_observability_context,
            # Phase 3: Development Workflow
            "3.1": self._build_setup_validation_context,
            "3.2": self._build_testing_context,
            "3.3": self._build_cicd_context,
            # Phase 4: Interactive Remediation
            "4.1": self._build_remediation_context,
            # Security templates
            "security.1": self._build_security_context,
            "security.2": self._build_error_handling_context,
            "security.3": self._build_dependency_security_context,
            # Architecture insights templates
            "arch.1": self._build_call_graph_context,
            "arch.2": self._build_git_hotspots_context,
            "arch.3": self._build_duplication_context,
            "arch.4": self._build_cohesion_coupling_context,
            # Strategy templates
            "strategy.1": self._build_documentation_strategy_context,
            "strategy.2": self._build_observability_strategy_context,
            "strategy.3": self._build_testing_strategy_context,
            "strategy.4": self._build_tech_debt_context,
            "strategy.5": self._build_mentorship_context,
        }

    # ========== Phase 0 Context Builders ==========

    def _build_readme_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
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

    def _build_architecture_docs_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for architecture documentation prompt."""
        docs = analysis.documentation
        if not docs:
            return None

        arch_docs = [d for d in docs.discovered_docs if d.doc_type == "architecture"]
        if not arch_docs:
            return None

        arch_content = "\n\n---\n\n".join(f"## {d.path}\n{d.content[:3000]}" for d in arch_docs[:3])

        return {
            "architecture_docs": arch_content,
            "doc_count": len(arch_docs),
            "claimed_pattern": (docs.claimed_architecture.pattern if docs.claimed_architecture else None),
        }

    def _build_setup_docs_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for setup documentation prompt."""
        docs = analysis.documentation
        if not docs or not docs.setup_instructions:
            return None

        setup = docs.setup_instructions
        return {
            "prerequisites": setup.prerequisites,
            "build_steps": setup.build_steps,
            "environment_vars": setup.environment_vars,
            "documented_in": setup.documented_in,
        }

    # ========== Phase 1 Context Builders ==========

    def _build_architecture_validation_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for architecture validation prompt."""
        code = analysis.code
        docs = analysis.documentation
        validation = analysis.validation

        return {
            "claimed_architecture": (
                {
                    "pattern": docs.claimed_architecture.pattern if docs else None,
                    "layers": docs.claimed_architecture.layers if docs else [],
                    "components": docs.claimed_architecture.components if docs else [],
                }
                if docs and docs.claimed_architecture
                else None
            ),
            "actual_structure": {
                "languages": [
                    {"name": l.name, "percentage": l.percentage}
                    for l in (code.structure.languages if code and code.structure else [])
                ],
                "frameworks": [f.name for f in (code.structure.frameworks if code and code.structure else [])],
                "entry_points": [ep.path for ep in (code.structure.entry_points if code and code.structure else [])],
            },
            "validation_results": (
                [
                    {
                        "status": r.validation_status.value,
                        "evidence": r.evidence,
                        "recommendation": r.recommendation,
                    }
                    for r in validation.architecture_drift
                ]
                if validation
                else []
            ),
        }

    def _build_dependency_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for dependency analysis prompt."""
        code = analysis.code
        docs = analysis.documentation

        if not code or not code.dependencies:
            return None

        return {
            "dependencies": [
                {
                    "name": d.name,
                    "version": d.version,
                    "type": d.dependency_type,
                    "source": d.source_file,
                }
                for d in code.dependencies[:50]
            ],
            "total_count": len(code.dependencies),
            "documented_prerequisites": (
                docs.setup_instructions.prerequisites if docs and docs.setup_instructions else []
            ),
        }

    # ========== Phase 2 Context Builders ==========

    def _build_quality_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
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

    def _build_observability_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for observability review prompt."""
        return {"repository_path": analysis.repository_path}

    # ========== Phase 3 Context Builders ==========

    def _build_setup_validation_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for setup validation prompt."""
        docs = analysis.documentation
        validation = analysis.validation

        return {
            "documented_setup": (
                {
                    "prerequisites": (
                        docs.setup_instructions.prerequisites if docs and docs.setup_instructions else []
                    ),
                    "build_steps": (docs.setup_instructions.build_steps if docs and docs.setup_instructions else []),
                    "env_vars": (docs.setup_instructions.environment_vars if docs and docs.setup_instructions else []),
                }
                if docs and docs.setup_instructions
                else None
            ),
            "validation_results": (
                [
                    {
                        "status": r.validation_status.value,
                        "evidence": r.evidence,
                        "recommendation": r.recommendation,
                    }
                    for r in validation.setup_drift
                ]
                if validation and validation.setup_drift
                else []
            ),
            "undocumented_features": validation.undocumented_features if validation else [],
        }

    def _build_testing_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for testing strategy prompt."""
        return {"repository_path": analysis.repository_path}

    def _build_cicd_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for CI/CD review prompt."""
        return {"repository_path": analysis.repository_path}

    # ========== Phase 4 Context Builders ==========

    def _build_remediation_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
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

    def _build_security_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for security vulnerability assessment."""
        return self._build_quality_context(analysis)  # Reuse quality context for now

    def _build_error_handling_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for error handling verification."""
        return self._build_quality_context(analysis)  # Reuse quality context for now

    def _build_dependency_security_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for dependency security audit."""
        return self._build_dependency_context(analysis)  # Reuse dependency context for now

    # ========== Architecture Insights Context Builders ==========

    def _build_call_graph_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for call graph and dependency tracing."""
        return self._build_dependency_context(analysis)  # Reuse dependency context for now

    def _build_git_hotspots_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for git hotspots analysis."""
        return self._build_quality_context(analysis)  # Reuse quality context for now

    def _build_duplication_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for code duplication analysis."""
        return self._build_quality_context(analysis)  # Reuse quality context for now

    def _build_cohesion_coupling_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for cohesion and coupling analysis."""
        return self._build_architecture_validation_context(analysis)  # Reuse architecture context for now

    # ========== Strategy Context Builders ==========

    def _build_documentation_strategy_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for living documentation strategy."""
        return self._build_architecture_docs_context(analysis)  # Reuse docs context for now

    def _build_observability_strategy_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for observability and instrumentation strategy."""
        return self._build_observability_context(analysis)  # Reuse observability context for now

    def _build_testing_strategy_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for test coverage and quality strategy."""
        return self._build_testing_context(analysis)  # Reuse testing context for now

    def _build_tech_debt_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for technical debt and refactoring roadmap."""
        return self._build_remediation_context(analysis)  # Reuse remediation context for now

    def _build_mentorship_context(self, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for team mentorship and best practices guide."""
        return self._build_quality_context(analysis)  # Reuse quality context for now
