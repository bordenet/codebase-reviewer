"""Base prompt generator functionality."""

from codebase_reviewer.models import Prompt, PromptCollection, RepositoryAnalysis
from codebase_reviewer.prompts.export import PromptExporter
from codebase_reviewer.prompts.generator import PhaseGenerator
from codebase_reviewer.prompts.workflow_loader import WorkflowLoader


class PromptGenerator:
    """Generates structured prompts for AI code review and onboarding."""

    def __init__(self):
        """Initialize with unified phase generator."""
        self.generator = PhaseGenerator()
        self.exporter = PromptExporter()
        self.workflow_loader = WorkflowLoader()

    def generate_all_phases(self, repo_analysis: RepositoryAnalysis, workflow: str = "default") -> PromptCollection:
        """Generate complete prompt set for all phases.

        Args:
            repo_analysis: Complete repository analysis
            workflow: Workflow name to use (default, principal_engineer, etc.)

        Returns:
            PromptCollection with prompts for all phases
        """
        if workflow == "default":
            # Use original 5-phase generation
            return PromptCollection(
                phase0=self.generator.generate(0, repo_analysis),
                phase1=self.generator.generate(1, repo_analysis),
                phase2=self.generator.generate(2, repo_analysis),
                phase3=self.generator.generate(3, repo_analysis),
                phase4=self.generator.generate(4, repo_analysis),
            )

        # Load workflow and generate prompts
        workflow_def = self.workflow_loader.load(workflow)
        return self._generate_from_workflow(workflow_def, repo_analysis)

    def _generate_from_workflow(self, workflow_def, repo_analysis: RepositoryAnalysis) -> PromptCollection:
        """Generate prompts from a workflow definition.

        Args:
            workflow_def: WorkflowDefinition object
            repo_analysis: Complete repository analysis

        Returns:
            PromptCollection with prompts organized by workflow sections
        """
        # For now, map workflow sections to phases
        # This is a simplified implementation for Phase 1
        all_prompts = []

        for section in workflow_def.sections:
            for prompt_ref in section.prompts:
                if prompt_ref.template:
                    # Resolve template reference
                    template_file, prompt_id = self.workflow_loader.resolve_template_reference(prompt_ref.template)
                    phase_num = int(template_file.replace("phase", "").replace(".yml", ""))
                    prompts = self.generator.generate(phase_num, repo_analysis)
                    # Find the specific prompt by ID if specified
                    if prompt_id:
                        matching = [p for p in prompts if p.prompt_id == prompt_id]
                        all_prompts.extend(matching)
                    else:
                        all_prompts.extend(prompts)
                elif prompt_ref.custom:
                    # Generate custom prompt
                    custom = prompt_ref.custom
                    all_prompts.append(
                        Prompt(
                            prompt_id=custom.id,
                            phase=0,  # Will be organized later
                            title=custom.title,
                            objective=custom.objective or "",
                            tasks=custom.tasks or [],
                            context=custom.prompt,
                            deliverable=custom.deliverable or "",
                        )
                    )

        # Organize into phases (simplified - put all in phase0 for now)
        return PromptCollection(
            phase0=all_prompts,
            phase1=[],
            phase2=[],
            phase3=[],
            phase4=[],
        )

    def export_prompts_markdown(self, prompts: PromptCollection) -> str:
        """Export prompts to markdown format."""
        return self.exporter.to_markdown(prompts)

    def export_prompts_json(self, prompts: PromptCollection) -> str:
        """Export prompts to JSON format."""
        return self.exporter.to_json(prompts)
