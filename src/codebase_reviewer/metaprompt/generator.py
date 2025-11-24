"""Generate meta-prompts for Phase 2 tool creation."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class MetaPromptGenerator:
    """Generates meta-prompts from Phase 1 analysis and user dialogue."""
    
    def __init__(self, template_path: Optional[Path] = None):
        """Initialize generator.
        
        Args:
            template_path: Path to meta-prompt template (default: built-in template)
        """
        if template_path is None:
            # Use built-in template
            template_path = Path(__file__).parent.parent.parent.parent / \
                "prompts" / "templates" / "meta-prompt-template.md"
        
        self.template_path = template_path
        self.template = template_path.read_text()
    
    def generate(
        self,
        phase1_prompt_path: Path,
        codebase_name: str,
        generation: int = 1,
        user_requirements: Optional[Dict[str, Any]] = None,
        learnings: Optional[str] = None
    ) -> str:
        """Generate meta-prompt from Phase 1 analysis.
        
        Args:
            phase1_prompt_path: Path to Phase 1 prompt
            codebase_name: Name of codebase
            generation: Generation number (1, 2, 3, ...)
            user_requirements: User requirements from dialogue
            learnings: Learnings from previous generations
            
        Returns:
            Complete meta-prompt ready for AI assistant
        """
        # Load Phase 1 prompt
        phase1_content = phase1_prompt_path.read_text()
        
        # Extract codebase analysis from Phase 1 prompt
        analysis = self._extract_analysis(phase1_content)
        
        # Get user requirements (or use defaults)
        reqs = user_requirements or self._default_requirements()
        
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
            
            # Thresholds
            "files_changed_threshold": reqs.get("files_changed_threshold", 20),
            "coverage_threshold": reqs.get("coverage_threshold", 90),
            "staleness_threshold": reqs.get("staleness_threshold", 30),
            "error_threshold": reqs.get("error_threshold", 5),
            
            # Learnings
            "learnings": learnings or "**Generation 1**: No previous learnings",
            "improvements": self._generate_improvements(generation, learnings),
            
            # Success criteria
            "fidelity_target": reqs.get("fidelity_target", 95),
            "coverage_target": reqs.get("coverage_target", 90),
            "performance_target": reqs.get("performance_target", "60"),
            
            # Full meta-prompt (for embedding)
            "full_meta_prompt": "{{SELF_REFERENCE}}",  # Will be replaced
        }
        
        # Generate meta-prompt
        meta_prompt = self._render_template(context)
        
        # Replace self-reference with actual content
        meta_prompt = meta_prompt.replace("{{SELF_REFERENCE}}", meta_prompt)
        
        return meta_prompt
    
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
                chunk = phase1_content[start:start+2000]
                analysis["repositories"] = chunk
        
        # Extract structure info
        if "Repository Structure" in phase1_content:
            analysis["structure"] = "Multi-repository structure (see Phase 1 prompt)"
        
        return analysis
    
    def _default_requirements(self) -> Dict[str, Any]:
        """Get default user requirements.
        
        Returns:
            Default requirements dictionary
        """
        return {
            "documentation_needs": "Comprehensive documentation including architecture, APIs, and setup guides",
            "quality_standards": "95% coverage, <5% error rate, clear and actionable",
            "update_frequency": "As needed when codebase changes significantly",
            "files_changed_threshold": 20,
            "coverage_threshold": 90,
            "staleness_threshold": 30,
            "error_threshold": 5,
            "fidelity_target": 95,
            "coverage_target": 90,
            "performance_target": "60",
        }
    
    def _generate_improvements(self, generation: int, learnings: Optional[str]) -> str:
        """Generate improvement recommendations.
        
        Args:
            generation: Generation number
            learnings: Learnings from previous generations
            
        Returns:
            Improvement recommendations
        """
        if generation == 1:
            return """
**Generation 1 Focus**:
- Establish baseline functionality
- Implement core analysis and documentation generation
- Set up metrics tracking and obsolescence detection
- Ensure meta-prompt embedding works correctly
"""
        else:
            return f"""
**Generation {generation} Focus**:
- Incorporate learnings from Gen {generation-1}
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

