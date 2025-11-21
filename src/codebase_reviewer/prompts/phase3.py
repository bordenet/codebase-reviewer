"""Phase 3: Development Workflow prompt generation."""

from typing import Any, Dict, List

from codebase_reviewer.models import Prompt, RepositoryAnalysis
from codebase_reviewer.prompts.template_loader import PromptTemplateLoader


class Phase3Generator:
    """Generates Phase 3 prompts for development workflow validation using templates."""

    def __init__(self):
        """Initialize the generator with template loader."""
        self.loader = PromptTemplateLoader()
        self.phase = 3

    def generate(self, analysis: RepositoryAnalysis) -> List[Prompt]:
        """Generate Phase 3 development workflow prompts from templates.

        Args:
            analysis: Repository analysis results

        Returns:
            List of Prompt instances for Phase 3
        """
        if not analysis.documentation or not analysis.validation:
            return []

        templates = self.loader.load_phase_templates(self.phase)
        prompts: List[Prompt] = []

        for template in templates:
            context = self._build_context(template, analysis)
            if context is None:
                continue

            prompts.append(template.to_prompt(context, self.phase))

        return prompts

    def _build_context(self, template, analysis: RepositoryAnalysis) -> Dict[str, Any]:
        """Build context dictionary for a template."""
        if template.id == "3.1":
            return self._build_setup_validation_context(analysis)
        elif template.id == "3.2":
            return self._build_testing_context(analysis)
        elif template.id == "3.3":
            return self._build_cicd_context(analysis)
        return {}

    def _build_setup_validation_context(self, analysis: RepositoryAnalysis) -> Dict[str, Any]:
        """Build context for setup validation prompt."""
        docs = analysis.documentation
        validation = analysis.validation

        return {
            "documented_setup": (
                {
                    "prerequisites": docs.setup_instructions.prerequisites,
                    "build_steps": docs.setup_instructions.build_steps,
                    "env_vars": docs.setup_instructions.environment_vars,
                }
                if docs.setup_instructions
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
                if validation.setup_drift
                else []
            ),
            "undocumented_features": validation.undocumented_features,
        }

    def _build_testing_context(self, analysis: RepositoryAnalysis) -> Dict[str, Any]:
        """Build context for testing strategy prompt."""
        return {"repository_path": analysis.repository_path}

    def _build_cicd_context(self, analysis: RepositoryAnalysis) -> Dict[str, Any]:
        """Build context for CI/CD review prompt."""
        return {"repository_path": analysis.repository_path}
