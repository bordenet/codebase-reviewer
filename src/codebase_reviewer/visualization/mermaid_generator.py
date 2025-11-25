"""Mermaid diagram generator for architecture visualization."""

from pathlib import Path
from typing import Dict, List, Optional

from ..models import CodeAnalysis, CodeStructure, DependencyInfo


class MermaidGenerator:
    """Generate Mermaid diagrams from code analysis."""

    def generate_architecture_diagram(self, analysis: CodeAnalysis) -> str:
        """Generate architecture diagram showing main components.

        Args:
            analysis: Code analysis results

        Returns:
            Mermaid diagram as string
        """
        lines = ["```mermaid", "graph TD"]

        if not analysis.structure:
            lines.extend(["    A[No Structure Data]", "```"])
            return "\n".join(lines)

        # Get top-level directories as components
        structure = analysis.structure
        components = self._extract_components(structure)

        # Add nodes
        for i, comp in enumerate(components[:10]):  # Limit to 10 components
            node_id = f"C{i}"
            lines.append(f"    {node_id}[{comp}]")

        # Add relationships based on dependencies
        if analysis.dependencies:
            for i, dep in enumerate(analysis.dependencies[:15]):  # Limit to 15 edges
                # Use dependency name and source_file for relationships
                source_idx = self._find_component_index(dep.source_file, components)
                target_idx = self._find_component_index(dep.name, components)
                if source_idx is not None and target_idx is not None and source_idx != target_idx:
                    lines.append(f"    C{source_idx} --> C{target_idx}")

        lines.append("```")
        return "\n".join(lines)

    def generate_dependency_graph(self, dependencies: List[DependencyInfo]) -> str:
        """Generate dependency graph.

        Args:
            dependencies: List of dependencies

        Returns:
            Mermaid diagram as string
        """
        lines = ["```mermaid", "graph LR"]

        if not dependencies:
            lines.extend(["    A[No Dependencies]", "```"])
            return "\n".join(lines)

        # Create nodes for each dependency
        node_ids = {}
        node_counter = 0

        for dep in dependencies[:20]:  # Limit to 20 dependencies
            dep_name = self._simplify_name(dep.name)
            if dep_name not in node_ids:
                node_ids[dep_name] = f"N{node_counter}"
                node_counter += 1
                # Color code by type
                if dep.dependency_type == "development":
                    lines.append(f"    {node_ids[dep_name]}[{dep_name}]:::dev")
                else:
                    lines.append(f"    {node_ids[dep_name]}[{dep_name}]")

        # Add style classes
        lines.extend(["    classDef dev fill:#f9f,stroke:#333,stroke-width:2px", "```"])
        return "\n".join(lines)

    def generate_data_flow_diagram(self, analysis: CodeAnalysis) -> str:
        """Generate data flow diagram.

        Args:
            analysis: Code analysis results

        Returns:
            Mermaid diagram as string
        """
        lines = ["```mermaid", "flowchart TD"]

        # Simple data flow based on structure
        lines.extend(
            [
                "    A[User Input] --> B[Input Validation]",
                "    B --> C[Business Logic]",
                "    C --> D[Data Access]",
                "    D --> E[Database]",
                "    C --> F[Output Formatting]",
                "    F --> G[User Output]",
            ]
        )

        lines.append("```")
        return "\n".join(lines)

    def generate_sequence_diagram(self, workflow_name: str = "Main Workflow") -> str:
        """Generate sequence diagram for a workflow.

        Args:
            workflow_name: Name of the workflow

        Returns:
            Mermaid diagram as string
        """
        lines = ["```mermaid", "sequenceDiagram"]

        lines.extend(
            [
                "    participant U as User",
                "    participant C as CLI",
                "    participant A as Analyzer",
                "    participant G as Generator",
                "",
                "    U->>C: Run analysis",
                "    C->>A: Analyze codebase",
                "    A->>A: Scan files",
                "    A->>A: Extract structure",
                "    A-->>C: Return analysis",
                "    C->>G: Generate docs",
                "    G-->>C: Return documentation",
                "    C-->>U: Display results",
            ]
        )

        lines.append("```")
        return "\n".join(lines)

    def _extract_components(self, structure: CodeStructure) -> List[str]:
        """Extract component names from structure."""
        components = []

        # Use language names as components
        if structure.languages:
            for lang in structure.languages[:5]:  # Top 5 languages
                components.append(lang.name)

        # Add framework names
        if structure.frameworks:
            for fw in structure.frameworks[:3]:  # Top 3 frameworks
                components.append(fw.name)

        return components if components else ["Main"]

    def _find_component_index(self, name: str, components: List[str]) -> Optional[int]:
        """Find component index by name."""
        for i, comp in enumerate(components):
            if comp.lower() in name.lower() or name.lower() in comp.lower():
                return i
        return None

    def _simplify_name(self, name: str) -> str:
        """Simplify a module/file name for display."""
        # Remove file extensions
        name = Path(name).stem
        # Take last part of path
        parts = name.split("/")
        return parts[-1] if parts else name
