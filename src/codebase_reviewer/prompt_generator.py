"""Base prompt generator functionality."""

from codebase_reviewer.models import PromptCollection, RepositoryAnalysis
from codebase_reviewer.prompts.export import PromptExporter
from codebase_reviewer.prompts.generator import PhaseGenerator


class PromptGenerator:
    """Generates structured prompts for AI code review and onboarding."""

    def __init__(self):
        """Initialize with unified phase generator."""
        self.generator = PhaseGenerator()
        self.exporter = PromptExporter()

    def generate_all_phases(self, repo_analysis: RepositoryAnalysis) -> PromptCollection:
        """Generate complete prompt set for all phases.

        Args:
            repo_analysis: Complete repository analysis

        Returns:
            PromptCollection with prompts for all phases
        """
        return PromptCollection(
            phase0=self.generator.generate(0, repo_analysis),
            phase1=self.generator.generate(1, repo_analysis),
            phase2=self.generator.generate(2, repo_analysis),
            phase3=self.generator.generate(3, repo_analysis),
            phase4=self.generator.generate(4, repo_analysis),
        )

    def export_prompts_markdown(self, prompts: PromptCollection) -> str:
        """Export prompts to markdown format."""
        return self.exporter.to_markdown(prompts)

    def export_prompts_json(self, prompts: PromptCollection) -> str:
        """Export prompts to JSON format."""
        return self.exporter.to_json(prompts)
