"""Phase 1: Architecture Analysis prompt generation."""

from typing import Any, Dict, List, Optional

from codebase_reviewer.models import Prompt, RepositoryAnalysis
from codebase_reviewer.prompts.template_loader import PromptTemplateLoader


class Phase1Generator:
    """Generates Phase 1 prompts for architecture analysis using templates."""

    def __init__(self):
        """Initialize the generator with template loader."""
        self.loader = PromptTemplateLoader()
        self.phase = 1

    def generate(self, analysis: RepositoryAnalysis) -> List[Prompt]:
        """Generate Phase 1 architecture analysis prompts from templates.

        Args:
            analysis: Repository analysis results

        Returns:
            List of Prompt instances for Phase 1
        """
        if not analysis.code or not analysis.documentation:
            return []

        templates = self.loader.load_phase_templates(self.phase)
        prompts: List[Prompt] = []

        for template in templates:
            if template.conditional and not self._check_conditional(template.conditional, analysis):
                continue

            context = self._build_context(template, analysis)
            if context is None:
                continue

            prompts.append(template.to_prompt(context, self.phase))

        return prompts

    def _check_conditional(self, conditional: str, analysis: RepositoryAnalysis) -> bool:
        """Check if conditional requirement is met."""
        if conditional == "has_dependencies":
            return bool(
                analysis.code and analysis.code.dependencies is not None and len(analysis.code.dependencies) > 0
            )
        return False

    def _build_context(self, template, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context dictionary for a template."""
        if template.id == "1.1":
            return self._build_architecture_validation_context(analysis)
        elif template.id == "1.2":
            return self._build_dependency_context(analysis)
        return {}

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
