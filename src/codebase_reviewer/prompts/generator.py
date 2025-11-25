"""Unified prompt generator using template-based configuration."""

from typing import Any, Callable, Dict, List, Optional

from codebase_reviewer.models import Prompt, RepositoryAnalysis
from codebase_reviewer.prompts.context_builders import ContextBuilders
from codebase_reviewer.prompts.template_loader import PromptTemplateLoader


class PhaseGenerator:
    """Generates prompts for any phase using templates and context builders."""

    def __init__(self):
        """Initialize the generator with template loader and context builders."""
        self.loader = PromptTemplateLoader()
        self.builders = ContextBuilders()
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
            "0.1": ContextBuilders.build_readme_context,
            "0.2": ContextBuilders.build_architecture_docs_context,
            "0.3": ContextBuilders.build_setup_docs_context,
            # Phase 1: Architecture Analysis
            "1.1": ContextBuilders.build_architecture_validation_context,
            "1.2": ContextBuilders.build_dependency_context,
            # Phase 2: Implementation Deep-Dive
            "2.1": ContextBuilders.build_quality_context,
            "2.2": ContextBuilders.build_observability_context,
            # Phase 3: Development Workflow
            "3.1": ContextBuilders.build_setup_validation_context,
            "3.2": ContextBuilders.build_testing_context,
            "3.3": ContextBuilders.build_cicd_context,
            # Phase 4: Interactive Remediation
            "4.1": ContextBuilders.build_remediation_context,
            # Security templates
            "security.1": ContextBuilders.build_security_context,
            "security.2": ContextBuilders.build_error_handling_context,
            "security.3": ContextBuilders.build_dependency_security_context,
            # Architecture insights templates
            "arch.1": ContextBuilders.build_call_graph_context,
            "arch.2": ContextBuilders.build_git_hotspots_context,
            "arch.3": ContextBuilders.build_duplication_context,
            "arch.4": ContextBuilders.build_cohesion_coupling_context,
            # Strategy templates
            "strategy.1": ContextBuilders.build_documentation_strategy_context,
            "strategy.2": ContextBuilders.build_observability_strategy_context,
            "strategy.3": ContextBuilders.build_testing_strategy_context,
            "strategy.4": ContextBuilders.build_tech_debt_context,
            "strategy.5": ContextBuilders.build_mentorship_context,
        }
