"""Phase 0: Documentation Review prompt generation."""

from typing import Dict, List, Any

from codebase_reviewer.models import Prompt, RepositoryAnalysis
from codebase_reviewer.prompts.template_loader import PromptTemplateLoader


class Phase0Generator:
    """Generates Phase 0 prompts for documentation review using templates."""

    def __init__(self):
        """Initialize the generator with template loader."""
        self.loader = PromptTemplateLoader()
        self.phase = 0

    def generate(self, analysis: RepositoryAnalysis) -> List[Prompt]:
        """Generate Phase 0 documentation review prompts from templates.

        Args:
            analysis: Repository analysis results

        Returns:
            List of Prompt instances for Phase 0
        """
        if not analysis.documentation:
            return []

        templates = self.loader.load_phase_templates(self.phase)
        prompts: List[Prompt] = []

        for template in templates:
            # Check conditional requirements
            if template.conditional and not self._check_conditional(template.conditional, analysis):
                continue

            # Build context for this template
            context = self._build_context(template, analysis)
            if context is None:
                continue

            prompts.append(template.to_prompt(context, self.phase))

        return prompts

    def _check_conditional(self, conditional: str, analysis: RepositoryAnalysis) -> bool:
        """Check if conditional requirement is met.

        Args:
            conditional: Conditional expression (e.g., "has_architecture_docs")
            analysis: Repository analysis results

        Returns:
            True if condition is met, False otherwise
        """
        docs = analysis.documentation
        if not docs:
            return False

        if conditional == "has_architecture_docs":
            return any(d.doc_type == "architecture" for d in docs.discovered_docs)
        elif conditional == "has_setup_instructions":
            return docs.setup_instructions is not None

        return False

    def _build_context(self, template, analysis: RepositoryAnalysis) -> Dict[str, Any]:
        """Build context dictionary for a template.

        Args:
            template: PromptTemplate instance
            analysis: Repository analysis results

        Returns:
            Context dictionary or None if context cannot be built
        """
        docs = analysis.documentation
        if not docs:
            return None

        # Build context based on template ID
        if template.id == "0.1":
            return self._build_readme_context(docs)
        elif template.id == "0.2":
            return self._build_architecture_context(docs)
        elif template.id == "0.3":
            return self._build_setup_context(docs)

        return {}

    def _build_readme_context(self, docs) -> Dict[str, Any]:
        """Build context for README analysis prompt."""
        readme_docs = [d for d in docs.discovered_docs if d.doc_type == "primary"]
        readme_content = readme_docs[0].content if readme_docs else "No README found"

        return {
            "readme_content": readme_content[:5000],
            "readme_path": readme_docs[0].path if readme_docs else "N/A",
            "total_docs_found": len(docs.discovered_docs),
        }

    def _build_architecture_context(self, docs) -> Dict[str, Any]:
        """Build context for architecture documentation prompt."""
        arch_docs = [d for d in docs.discovered_docs if d.doc_type == "architecture"]
        if not arch_docs:
            return None

        arch_content = "\n\n---\n\n".join(f"## {d.path}\n{d.content[:3000]}" for d in arch_docs[:3])

        return {
            "architecture_docs": arch_content,
            "doc_count": len(arch_docs),
            "claimed_pattern": docs.claimed_architecture.pattern if docs.claimed_architecture else None,
        }

    def _build_setup_context(self, docs) -> Dict[str, Any]:
        """Build context for setup documentation prompt."""
        if not docs.setup_instructions:
            return None

        setup = docs.setup_instructions
        return {
            "prerequisites": setup.prerequisites,
            "build_steps": setup.build_steps,
            "environment_vars": setup.environment_vars,
            "documented_in": setup.documented_in,
        }
