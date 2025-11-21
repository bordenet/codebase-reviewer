"""Phase 4: Interactive Remediation prompt generation."""

from typing import Any, Dict, List

from codebase_reviewer.models import Prompt, RepositoryAnalysis
from codebase_reviewer.prompts.template_loader import PromptTemplateLoader


class Phase4Generator:
    """Generates Phase 4 prompts for interactive remediation using templates."""

    def __init__(self):
        """Initialize the generator with template loader."""
        self.loader = PromptTemplateLoader()
        self.phase = 4

    def generate(self, analysis: RepositoryAnalysis) -> List[Prompt]:
        """Generate Phase 4 interactive remediation prompts from templates.

        Args:
            analysis: Repository analysis results

        Returns:
            List of Prompt instances for Phase 4
        """
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
        if template.id == "4.1":
            return self._build_prioritization_context(analysis)
        return {}

    def _build_prioritization_context(self, analysis: RepositoryAnalysis) -> Dict[str, Any]:
        """Build context for issue prioritization prompt."""
        all_issues: List[Dict[str, Any]] = []

        # Collect validation issues
        if analysis.validation:
            for drift in (
                analysis.validation.architecture_drift + analysis.validation.setup_drift + analysis.validation.api_drift
            ):
                all_issues.append(
                    {
                        "category": "Documentation Drift",
                        "severity": drift.severity.value,
                        "description": drift.evidence,
                        "recommendation": drift.recommendation,
                    }
                )

        # Collect code quality issues
        if analysis.code and analysis.code.quality_issues:
            for issue in analysis.code.quality_issues[:20]:
                all_issues.append(
                    {
                        "category": "Code Quality",
                        "severity": issue.severity.value,
                        "description": issue.title,
                        "source": issue.source,
                    }
                )

        return {
            "total_issues": len(all_issues),
            "issues_by_severity": {
                "critical": len([i for i in all_issues if i.get("severity") == "critical"]),
                "high": len([i for i in all_issues if i.get("severity") == "high"]),
                "medium": len([i for i in all_issues if i.get("severity") == "medium"]),
                "low": len([i for i in all_issues if i.get("severity") == "low"]),
            },
            "top_issues": all_issues[:15],
        }
