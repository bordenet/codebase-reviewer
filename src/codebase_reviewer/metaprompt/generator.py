"""Generate meta-prompts for Phase 2 tool creation."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from codebase_reviewer.config.loader import ConfigLoader, Phase2ThresholdsConfig, PromptsConfig
from codebase_reviewer.obsolescence.detector import ObsolescenceResult, ObsolescenceTrigger


class MetaPromptGenerator:
    """Generates meta-prompts from Phase 1 analysis and user dialogue.

    This generator uses externalized configuration from:
    - config/phase2_thresholds.yml: Threshold values and recommendations
    - config/prompts.yml: Prompt templates and settings
    """

    def __init__(self, template_path: Optional[Path] = None):
        """Initialize generator.

        Args:
            template_path: Path to meta-prompt template (default: built-in template)
        """
        if template_path is None:
            # Use built-in template
            template_path = (
                Path(__file__).parent.parent.parent.parent / "prompts" / "templates" / "meta-prompt-template.yaml"
            )

        self.template_path = template_path
        self.template = template_path.read_text()

        # Load configuration
        self._config_loader = ConfigLoader()
        self._thresholds_config: Optional[Phase2ThresholdsConfig] = None
        self._prompts_config: Optional[PromptsConfig] = None

    @property
    def thresholds_config(self) -> Phase2ThresholdsConfig:
        """Get thresholds configuration (lazy loaded)."""
        if self._thresholds_config is None:
            self._thresholds_config = self._config_loader.load_thresholds()
        return self._thresholds_config

    @property
    def prompts_config(self) -> PromptsConfig:
        """Get prompts configuration (lazy loaded)."""
        if self._prompts_config is None:
            self._prompts_config = self._config_loader.load_prompts()
        return self._prompts_config

    def generate(
        self,
        phase1_prompt_path: Path,
        codebase_name: str,
        generation: int = 1,
        user_requirements: Optional[Dict[str, Any]] = None,
        learnings: Optional[str] = None,
        obsolescence_result: Optional[ObsolescenceResult] = None,
    ) -> str:
        """Generate meta-prompt from Phase 1 analysis.

        Args:
            phase1_prompt_path: Path to Phase 1 prompt
            codebase_name: Name of codebase
            generation: Generation number (1, 2, 3, ...)
            user_requirements: User requirements from dialogue
            learnings: Learnings from previous generations
            obsolescence_result: Result from obsolescence detection (for regeneration)

        Returns:
            Complete meta-prompt ready for AI assistant
        """
        # Load Phase 1 prompt
        phase1_content = phase1_prompt_path.read_text()

        # Extract codebase analysis from Phase 1 prompt
        analysis = self._extract_analysis(phase1_content)

        # Get user requirements (or use defaults from config)
        reqs = user_requirements or self._default_requirements()

        # Get threshold values from config
        thresholds = self.thresholds_config

        # Build context
        context = {
            "generation": generation,
            "codebase_name": codebase_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            # Codebase analysis
            "codebase_structure": analysis.get("structure", "See Phase 1 prompt"),
            "languages": analysis.get("languages", "See Phase 1 prompt"),
            "repositories": analysis.get("repositories", "See Phase 1 prompt"),
            "patterns": analysis.get("patterns", "See Phase 1 prompt"),
            # User requirements
            "documentation_needs": reqs.get("documentation_needs", "Comprehensive documentation"),
            "quality_standards": reqs.get("quality_standards", "95% coverage, <5% errors"),
            "update_frequency": reqs.get("update_frequency", "As needed"),
            # Thresholds from config (not hardcoded)
            "files_changed_threshold": thresholds.files_changed_percent,
            "coverage_threshold": thresholds.coverage_min_percent,
            "staleness_threshold": thresholds.staleness_max_days,
            "error_threshold": thresholds.error_rate_max_percent,
            "false_positive_multiplier": thresholds.false_positive_spike_multiplier,
            "cooldown_days": thresholds.fallback.cooldown_days,
            # Learnings
            "learnings": learnings or "**Generation 1**: No previous learnings",
            "improvements": self._generate_improvements(generation, learnings),
            # Success criteria from config
            "fidelity_target": reqs.get("fidelity_target", self.prompts_config.defaults.get("fidelity_target", 95)),
            "coverage_target": reqs.get("coverage_target", self.prompts_config.defaults.get("coverage_target", 90)),
            "performance_target": reqs.get(
                "performance_target", self.prompts_config.defaults.get("performance_target_seconds", 60)
            ),
            # Full meta-prompt (for embedding)
            "full_meta_prompt": "{{SELF_REFERENCE}}",  # Will be replaced
            # Threshold config YAML for embedding
            "threshold_config_yaml": self._config_loader.get_threshold_as_yaml(),
        }

        # Add obsolescence context if this is a regeneration
        if obsolescence_result and obsolescence_result.is_obsolete:
            context.update(self._build_obsolescence_context(obsolescence_result))

        # Generate meta-prompt
        meta_prompt = self._render_template(context)

        # Replace self-reference with actual content
        meta_prompt = meta_prompt.replace("{{SELF_REFERENCE}}", meta_prompt)

        return meta_prompt

    def _build_obsolescence_context(self, result: ObsolescenceResult) -> Dict[str, Any]:
        """Build context from obsolescence detection result.

        Args:
            result: ObsolescenceResult from detector

        Returns:
            Context dictionary for template rendering
        """
        # Format trigger reasons
        trigger_reasons = "\n".join(f"- {r}" for r in result.reasons)

        # Format recommendations from triggers
        recommendations = []
        for trigger in result.triggers:
            if trigger.recommendation:
                recommendations.append(
                    f"### {trigger.trigger_type.replace('_', ' ').title()}\n{trigger.recommendation}"
                )

        # Build improvement list based on triggers
        improvement_list = self._build_improvement_list(result.triggers)

        return {
            "is_regeneration": True,
            "trigger_reasons": trigger_reasons,
            "trigger_types": ", ".join(result.get_trigger_types()),
            "recommendations": "\n\n".join(recommendations) if recommendations else "No specific recommendations.",
            "improvement_list": improvement_list,
            "obsolescence_threshold_config": result.threshold_config_yaml,
        }

    def _build_improvement_list(self, triggers: List[ObsolescenceTrigger]) -> str:
        """Build improvement list from triggers.

        Args:
            triggers: List of obsolescence triggers

        Returns:
            Formatted improvement list
        """
        improvements = []

        for trigger in triggers:
            if trigger.trigger_type == "files_changed":
                improvements.append("- Update file discovery and traversal patterns")
                improvements.append("- Revise directory structure assumptions")
            elif trigger.trigger_type == "new_languages":
                improvements.append(f"- Add support for new languages: {trigger.current_value}")
                improvements.append("- Implement language-specific analysis patterns")
            elif trigger.trigger_type == "coverage_drop":
                improvements.append("- Expand file pattern matching")
                improvements.append("- Review exclude patterns for over-filtering")
            elif trigger.trigger_type == "staleness":
                improvements.append("- Consider implementing incremental analysis")
                improvements.append("- Add CI/CD integration for automatic updates")
            elif trigger.trigger_type == "error_spike":
                improvements.append("- Improve error handling and edge case detection")
                improvements.append("- Add more robust input validation")
            elif trigger.trigger_type == "false_positive_spike":
                improvements.append("- Refine detection patterns to reduce false positives")
                improvements.append("- Implement context-aware filtering")

        return "\n".join(improvements) if improvements else "- General improvements based on usage patterns"

    def _extract_analysis(self, phase1_content: str) -> Dict[str, str]:
        """Extract codebase analysis from Phase 1 prompt.

        Args:
            phase1_content: Phase 1 prompt content

        Returns:
            Dictionary of analysis sections
        """
        # Simple extraction - look for JSON blocks
        analysis = {}

        # Try to find nested_repos JSON
        if "nested_repos" in phase1_content:
            start = phase1_content.find("nested_repos")
            if start != -1:
                # Extract a reasonable chunk
                chunk = phase1_content[start : start + 2000]
                analysis["repositories"] = chunk

        # Extract structure info
        if "Repository Structure" in phase1_content:
            analysis["structure"] = "Multi-repository structure (see Phase 1 prompt)"

        return analysis

    def _default_requirements(self) -> Dict[str, Any]:
        """Get default user requirements from config.

        Returns:
            Default requirements dictionary from config/prompts.yml
        """
        defaults = self.prompts_config.defaults
        thresholds = self.thresholds_config

        return {
            "documentation_needs": defaults.get(
                "documentation_needs", "Comprehensive documentation including architecture, APIs, and setup guides"
            ),
            "quality_standards": defaults.get(
                "quality_standards", "95% coverage, <5% error rate, clear and actionable"
            ),
            "update_frequency": defaults.get("update_frequency", "As needed when codebase changes significantly"),
            # Thresholds from config
            "files_changed_threshold": thresholds.files_changed_percent,
            "coverage_threshold": thresholds.coverage_min_percent,
            "staleness_threshold": thresholds.staleness_max_days,
            "error_threshold": thresholds.error_rate_max_percent,
            # Targets from config
            "fidelity_target": defaults.get("fidelity_target", 95),
            "coverage_target": defaults.get("coverage_target", 90),
            "performance_target": defaults.get("performance_target_seconds", 60),
        }

    def _generate_improvements(self, generation: int, learnings: Optional[str]) -> str:
        """Generate improvement recommendations from config.

        Args:
            generation: Generation number
            learnings: Learnings from previous generations

        Returns:
            Improvement recommendations from config/prompts.yml
        """
        if generation == 1:
            # Use template from config if available
            template = self.prompts_config.generation_1_focus
            if template:
                return template
            return """
**Generation 1 Focus**:
- Establish baseline functionality
- Implement core analysis and documentation generation
- Set up metrics tracking and obsolescence detection
- Ensure meta-prompt embedding works correctly
"""
        else:
            # Use template from config if available
            template = self.prompts_config.generation_n_focus
            if template:
                # Simple template substitution
                return template.replace("{{generation}}", str(generation)).replace(
                    "{{prev_generation}}", str(generation - 1)
                )
            return f"""
**Generation {generation} Focus**:
- Incorporate learnings from Gen {generation - 1}
- Improve coverage and accuracy
- Optimize performance
- Enhance error handling
- Add new patterns detected in codebase

See learnings section for specific improvements.
"""

    def _render_template(self, context: Dict[str, Any]) -> str:
        """Render template with context.

        Args:
            context: Template context

        Returns:
            Rendered template
        """
        result = self.template

        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))

        return result
