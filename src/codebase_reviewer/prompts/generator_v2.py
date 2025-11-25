"""Phase 1 prompt generator for v2.0 architecture."""

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from codebase_reviewer.prompts.v2_loader import Phase1TemplateV2, PromptTemplateV2Loader


@dataclass
class ScanParameters:
    """Parameters for codebase scanning."""

    target_path: str
    scan_mode: str = "review"  # review, deep_scan, or scorch
    output_path: str = "/tmp/codebase-reviewer"
    exclude_patterns: Optional[List[str]] = None
    include_patterns: Optional[List[str]] = None
    max_file_size_kb: int = 500
    languages: Optional[List[str]] = None


class Phase1PromptGeneratorV2:
    """Generates Phase 1 prompts using v2.0 template architecture."""

    def __init__(self, template_path: Optional[str] = None):
        """Initialize the generator.

        Args:
            template_path: Optional path to phase1-prompt-template.yaml
        """
        self.loader = PromptTemplateV2Loader(template_path)
        self.template: Optional[Phase1TemplateV2] = None

    def load_template(self) -> Phase1TemplateV2:
        """Load the Phase 1 template."""
        if self.template is None:
            self.template = self.loader.load_phase1_template()
        return self.template

    def generate_prompt(self, params: ScanParameters) -> str:
        """Generate a complete Phase 1 prompt for codebase analysis.

        Args:
            params: Scan parameters including target path, mode, etc.

        Returns:
            Complete prompt string ready to send to LLM
        """
        template = self.load_template()

        # Build the prompt sections
        sections = []

        # Header
        sections.append(f"# Codebase Analysis Request - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sections.append("")

        # Role and context
        sections.append(f"## Your Role")
        sections.append(template.role)
        sections.append("")
        sections.append(f"## Context")
        sections.append(template.context)
        sections.append("")

        # Scan parameters
        sections.append(f"## Scan Parameters")
        sections.append(f"- **Target Path**: `{params.target_path}`")
        sections.append(f"- **Scan Mode**: `{params.scan_mode}`")
        sections.append(f"- **Output Path**: `{params.output_path}`")
        if params.exclude_patterns:
            sections.append(f"- **Exclude Patterns**: {', '.join(params.exclude_patterns)}")
        if params.include_patterns:
            sections.append(f"- **Include Patterns**: {', '.join(params.include_patterns)}")
        if params.languages:
            sections.append(f"- **Languages**: {', '.join(params.languages)}")
        sections.append(f"- **Max File Size**: {params.max_file_size_kb} KB")
        sections.append("")

        # Scan mode definition
        if params.scan_mode in template.scan_mode_definitions:
            mode_def = template.scan_mode_definitions[params.scan_mode]
            sections.append(f"## Scan Mode: {params.scan_mode}")
            sections.append(f"**Description**: {mode_def['description']}")
            sections.append(f"**Depth**: {mode_def['depth']}")
            sections.append(f"**Focus**: {mode_def['focus']}")
            sections.append("")

        # Tasks
        sections.append(f"## Tasks")
        sections.append("")
        for i, task in enumerate(template.tasks, 1):
            sections.append(f"### Task {i}: {task.name}")
            sections.append(f"**ID**: {task.task_id}")
            sections.append("")
            sections.append(task.description)
            sections.append("")
            sections.append(f"**Output Format**: {task.output_format}")
            sections.append("")
            if task.output_schema:
                sections.append(f"**Output Schema**:")
                sections.append(f"```")
                sections.append(task.output_schema)
                sections.append(f"```")
                sections.append("")

        # Output requirements
        sections.append(f"## Output Requirements")
        for key, value in template.output_requirements.items():
            sections.append(f"- **{key}**: {value}")
        sections.append("")

        # Guidance
        sections.append(f"## Guidance")
        for category, items in template.guidance_spec.items():
            sections.append(f"### {category.replace('_', ' ').title()}")
            for item in items:
                sections.append(f"- {item}")
            sections.append("")

        # Success criteria
        sections.append(f"## Success Criteria")
        for criterion in template.success_criteria:
            sections.append(f"- {criterion}")
        sections.append("")

        # Security and execution notes
        sections.append(f"## Security Notes")
        sections.append(template.security_notes)
        sections.append("")
        sections.append(f"## Execution Notes")
        sections.append(template.execution_notes)
        sections.append("")

        return "\n".join(sections)

    def save_prompt(self, prompt: str, output_path: str) -> str:
        """Save generated prompt to file.

        Args:
            prompt: Generated prompt string
            output_path: Directory to save prompt

        Returns:
            Path to saved prompt file
        """
        os.makedirs(output_path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phase1_prompt_{timestamp}.md"
        filepath = os.path.join(output_path, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(prompt)

        return filepath
