"""Phase 2: Implementation Deep-Dive prompt generation."""

from typing import Any, Dict, List, Optional

from codebase_reviewer.models import Prompt, RepositoryAnalysis, Severity
from codebase_reviewer.prompts.template_loader import PromptTemplateLoader


class Phase2Generator:
    """Generates Phase 2 prompts for implementation analysis using templates."""

    def __init__(self):
        """Initialize the generator with template loader."""
        self.loader = PromptTemplateLoader()
        self.phase = 2

    def generate(self, analysis: RepositoryAnalysis) -> List[Prompt]:
        """Generate Phase 2 implementation deep-dive prompts from templates.

        Args:
            analysis: Repository analysis results

        Returns:
            List of Prompt instances for Phase 2
        """
        if not analysis.code:
            return []

        templates = self.loader.load_phase_templates(self.phase)
        prompts: List[Prompt] = []

        for template in templates:
            context = self._build_context(template, analysis)
            if context is None:
                continue

            prompts.append(template.to_prompt(context, self.phase))

        return prompts

    def _build_context(self, template, analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context dictionary for a template."""
        if template.id == "2.1":
            return self._build_quality_context(analysis)
        elif template.id == "2.2":
            return self._build_observability_context(analysis)
        return {}

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
