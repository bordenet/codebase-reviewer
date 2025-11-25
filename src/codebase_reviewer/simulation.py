"""LLM simulation system for testing and tuning prompts."""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from codebase_reviewer.models import Prompt, RepositoryAnalysis
from codebase_reviewer.orchestrator import AnalysisOrchestrator
from codebase_reviewer.prompt_generator import PromptGenerator
from codebase_reviewer.mock_llm import MockLLM


@dataclass
class SimulatedResponse:
    """A simulated LLM response to a prompt."""

    prompt_id: str
    prompt_text: str
    response: str
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class SimulationResult:
    """Results from a simulation run."""

    repository_path: str
    workflow: str
    prompts_tested: int
    responses: List[SimulatedResponse]
    timestamp: datetime
    duration_seconds: float


class LLMSimulator:
    """Simulates LLM responses for prompt testing and tuning."""

    def __init__(self, output_dir: Optional[str] = None, use_mock_llm: bool = True):
        """Initialize the simulator.

        Args:
            output_dir: Directory to save simulation results (default: ./simulation_results)
            use_mock_llm: Whether to use context-aware mock LLM (default: True)
        """
        self.output_dir = Path(output_dir or "./simulation_results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.use_mock_llm = use_mock_llm
        self.mock_llm = MockLLM() if use_mock_llm else None

    def simulate_prompt(
        self, prompt: Prompt, analysis: RepositoryAnalysis
    ) -> SimulatedResponse:
        """Simulate an LLM response to a single prompt.

        This is where YOU (Claude) will act as the LLM and provide responses.
        For now, this generates a structured placeholder that shows what the LLM would receive.

        Args:
            prompt: The prompt to simulate
            analysis: The repository analysis context

        Returns:
            SimulatedResponse with the simulated LLM output
        """
        # Generate the full prompt text
        prompt_text = self._format_prompt(prompt, analysis)

        # For now, generate a structured analysis response
        # In interactive mode, this would be replaced with actual Claude responses
        response = self._generate_analysis_response(prompt, analysis)

        return SimulatedResponse(
            prompt_id=prompt.prompt_id,
            prompt_text=prompt_text,
            response=response,
            timestamp=datetime.now(),
            metadata={
                "prompt_name": prompt.title,
                "prompt_phase": prompt.phase,
                "repository": analysis.repository_path,
            },
        )

    def _format_prompt(self, prompt: Prompt, analysis: RepositoryAnalysis) -> str:
        """Format a prompt with context for the LLM."""
        # Get languages from code analysis
        languages = []
        if analysis.code and analysis.code.structure:
            languages = [lang.name for lang in analysis.code.structure.languages]

        sections = [
            f"# {prompt.title}",
            "",
            f"**Objective:** {prompt.objective}",
            "",
            "**Tasks:**",
        ]

        for task in prompt.tasks:
            sections.append(f"- {task}")

        sections.extend(
            [
                "",
                f"**Deliverable:** {prompt.deliverable}",
                "",
                "---",
                "",
                "**Repository Context:**",
                f"- Path: {analysis.repository_path}",
                f"- Languages: {', '.join(languages) if languages else 'Unknown'}",
                "",
                "**Context Data:**",
                "",
                str(prompt.context),
            ]
        )

        return "\n".join(sections)

    def _generate_analysis_response(
        self, prompt: Prompt, analysis: RepositoryAnalysis
    ) -> str:
        """Generate a simulated analysis response.

        This creates a structured response showing what information the LLM would analyze.
        If use_mock_llm is True, uses context-aware mock LLM for realistic responses.
        """
        # Use mock LLM if enabled
        if self.use_mock_llm and self.mock_llm:
            prompt_text = self._format_prompt(prompt, analysis)
            return self.mock_llm.generate_response(
                prompt.prompt_id, prompt_text, prompt.context, analysis.repository_path
            )

        # Fallback to generic placeholder
        languages = []
        if analysis.code and analysis.code.structure:
            languages = [lang.name for lang in analysis.code.structure.languages]

        response_parts = [
            f"# Analysis Response: {prompt.title}",
            "",
            "## Summary",
            f"This is a simulated response for prompt '{prompt.prompt_id}'.",
            f"The prompt asks the LLM to analyze: {prompt.objective}",
            "",
            "## Key Findings",
            "- [Simulated finding 1]",
            "- [Simulated finding 2]",
            "- [Simulated finding 3]",
            "",
            "## Recommendations",
            "- [Simulated recommendation 1]",
            "- [Simulated recommendation 2]",
            "",
            "## Context Analyzed",
            f"- Repository: {analysis.repository_path}",
            f"- Languages: {', '.join(languages) if languages else 'Unknown'}",
            "",
            "---",
            "*This is a simulated response. In interactive mode, Claude would provide actual analysis.*",
        ]

        return "\n".join(response_parts)

    def run_simulation(
        self, repo_path: str, workflow: str = "default"
    ) -> SimulationResult:
        """Run a full simulation on a repository.

        Args:
            repo_path: Path to the repository to analyze
            workflow: Workflow to use for the simulation

        Returns:
            SimulationResult with all simulated responses
        """
        start_time = datetime.now()

        # Run analysis
        orchestrator = AnalysisOrchestrator()
        analysis = orchestrator.run_full_analysis(repo_path)

        # Generate prompts
        generator = PromptGenerator()
        prompt_collection = generator.generate_all_phases(analysis, workflow=workflow)
        prompts = prompt_collection.all_prompts()

        # Simulate responses for each prompt
        responses = []
        for prompt in prompts:
            response = self.simulate_prompt(prompt, analysis)
            responses.append(response)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        result = SimulationResult(
            repository_path=repo_path,
            workflow=workflow,
            prompts_tested=len(prompts),
            responses=responses,
            timestamp=start_time,
            duration_seconds=duration,
        )

        # Save results
        self._save_results(result)

        return result

    def _save_results(self, result: SimulationResult) -> None:
        """Save simulation results to disk."""
        timestamp_str = result.timestamp.strftime("%Y%m%d_%H%M%S")
        workflow_name = result.workflow.replace("/", "_")
        output_file = (
            self.output_dir / f"simulation_{workflow_name}_{timestamp_str}.json"
        )

        # Convert to JSON-serializable format
        data = {
            "repository_path": result.repository_path,
            "workflow": result.workflow,
            "prompts_tested": result.prompts_tested,
            "timestamp": result.timestamp.isoformat(),
            "duration_seconds": result.duration_seconds,
            "responses": [
                {
                    "prompt_id": r.prompt_id,
                    "prompt_text": r.prompt_text,
                    "response": r.response,
                    "timestamp": r.timestamp.isoformat(),
                    "metadata": r.metadata,
                }
                for r in result.responses
            ],
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"\n✅ Simulation results saved to: {output_file}")

        # Also save a human-readable markdown report
        self._save_markdown_report(result, timestamp_str, workflow_name)

    def _save_markdown_report(
        self, result: SimulationResult, timestamp_str: str, workflow_name: str
    ) -> None:
        """Save a human-readable markdown report."""
        report_file = self.output_dir / f"simulation_{workflow_name}_{timestamp_str}.md"

        lines = [
            f"# Simulation Report: {result.workflow}",
            "",
            f"**Repository:** {result.repository_path}",
            f"**Timestamp:** {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Duration:** {result.duration_seconds:.2f} seconds",
            f"**Prompts Tested:** {result.prompts_tested}",
            "",
            "---",
            "",
        ]

        for i, response in enumerate(result.responses, 1):
            lines.extend(
                [
                    f"## {i}. {response.metadata.get('prompt_name', 'Unknown')}",
                    "",
                    f"**Prompt ID:** `{response.prompt_id}`",
                    f"**Phase:** {response.metadata.get('prompt_phase', 'N/A')}",
                    "",
                    "### Prompt Text",
                    "",
                    "```",
                    response.prompt_text,
                    "```",
                    "",
                    "### Simulated Response",
                    "",
                    response.response,
                    "",
                    "---",
                    "",
                ]
            )

        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"📄 Markdown report saved to: {report_file}")

    def print_summary(self, result: SimulationResult) -> None:
        """Print a summary of the simulation results."""
        print("\n" + "=" * 80)
        print(f"🎯 SIMULATION SUMMARY: {result.workflow}")
        print("=" * 80)
        print(f"Repository: {result.repository_path}")
        print(f"Prompts Tested: {result.prompts_tested}")
        print(f"Duration: {result.duration_seconds:.2f} seconds")
        print(f"Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nPrompts:")
        for i, response in enumerate(result.responses, 1):
            print(
                f"  {i}. {response.metadata.get('prompt_name', 'Unknown')} ({response.prompt_id})"
            )
        print("=" * 80 + "\n")
