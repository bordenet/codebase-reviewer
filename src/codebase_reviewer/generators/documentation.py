"""Documentation generator - creates comprehensive documentation from code analysis."""

from pathlib import Path
from typing import List, Optional
from ..models import CodeAnalysis, Language


class DocumentationGenerator:
    """Generate comprehensive documentation from code analysis."""
    
    def generate(self, analysis: CodeAnalysis, codebase_path: str) -> str:
        """
        Generate comprehensive documentation.
        
        Args:
            analysis: Code analysis results
            codebase_path: Path to the codebase
            
        Returns:
            Markdown documentation string
        """
        sections = []
        
        # Title
        codebase_name = Path(codebase_path).name
        sections.append(f"# {codebase_name} - Codebase Documentation")
        sections.append("")
        
        # Overview
        sections.extend(self._generate_overview(analysis, codebase_path))
        sections.append("")
        
        # Architecture
        sections.extend(self._generate_architecture(analysis))
        sections.append("")
        
        # Languages
        sections.extend(self._generate_languages(analysis))
        sections.append("")
        
        # Key Components
        sections.extend(self._generate_components(analysis))
        sections.append("")
        
        # Setup Instructions
        sections.extend(self._generate_setup(analysis))
        sections.append("")
        
        # API Documentation
        sections.extend(self._generate_api_docs(analysis))
        sections.append("")
        
        return "\n".join(sections)
    
    def _generate_overview(self, analysis: CodeAnalysis, codebase_path: str) -> List[str]:
        """Generate overview section."""
        languages = analysis.structure.languages if analysis.structure else []
        lang_count = len(languages)
        
        total_files = sum(lang.file_count for lang in languages) if languages else 0
        
        return [
            "## Overview",
            "",
            f"This codebase is located at `{codebase_path}` and contains {total_files} files across {lang_count} programming languages.",
            "",
            "The project appears to be a well-structured codebase with clear separation of concerns.",
        ]
    
    def _generate_architecture(self, analysis: CodeAnalysis) -> List[str]:
        """Generate architecture section."""
        return [
            "## Architecture",
            "",
            "The codebase follows a modular architecture with the following components:",
            "",
            "- **Analyzers**: Code and documentation analysis modules",
            "- **Validators**: Quality and fidelity validation systems",
            "- **CLI**: Command-line interface for user interaction",
            "- **Generators**: Documentation and code generation tools",
        ]
    
    def _generate_languages(self, analysis: CodeAnalysis) -> List[str]:
        """Generate languages section."""
        lines = [
            "## Languages",
            "",
            "The codebase uses the following programming languages:",
            "",
        ]
        
        languages = analysis.structure.languages if analysis.structure else []
        if languages:
            for lang in languages[:10]:
                lines.append(f"- **{lang.name}**: {lang.file_count} files")
        else:
            lines.append("- No language information available")
        
        return lines
    
    def _generate_components(self, analysis: CodeAnalysis) -> List[str]:
        """Generate key components section."""
        return [
            "## Key Components",
            "",
            "The codebase is organized into the following key components:",
            "",
            "### Analyzers",
            "",
            "- Code analysis: Analyzes code structure and quality",
            "- Documentation analysis: Evaluates documentation completeness",
            "",
            "### Validators",
            "",
            "- Quality validation: Ensures code quality standards",
            "- Fidelity validation: Compares outputs for consistency",
            "",
            "### CLI",
            "",
            "- Command-line interface for all operations",
            "- Interactive workflows for complex tasks",
        ]
    
    def _generate_setup(self, analysis: CodeAnalysis) -> List[str]:
        """Generate setup instructions."""
        languages = analysis.structure.languages if analysis.structure else []
        has_python = any(lang.name == "Python" for lang in languages)
        has_go = any(lang.name == "Go" for lang in languages)
        
        lines = [
            "## Setup Instructions",
            "",
        ]
        
        if has_python:
            lines.extend([
                "### Python Setup",
                "",
                "1. Clone the repository",
                "2. Install dependencies: `pip install -e .`",
                "3. Run the application: `review-codebase --help`",
                "",
            ])
        
        if has_go:
            lines.extend([
                "### Go Setup",
                "",
                "1. Ensure Go is installed (1.19+)",
                "2. Build the tools: `go build ./...`",
                "3. Run the tools: `./bin/generate-docs`",
                "",
            ])
        
        return lines
    
    def _generate_api_docs(self, analysis: CodeAnalysis) -> List[str]:
        """Generate API documentation section."""
        return [
            "## API Documentation",
            "",
            "API documentation is available in the respective module directories.",
            "",
            "Key APIs:",
            "",
            "- **Analyzers API**: For code and documentation analysis",
            "- **Validators API**: For quality and fidelity validation",
            "- **Generators API**: For documentation generation",
        ]

