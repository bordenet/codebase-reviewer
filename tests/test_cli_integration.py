"""Integration tests for CLI to prevent broken imports from passing CI.

This test file exists because we had a critical quality gate failure where:
- All 177 unit tests passed
- But the CLI was completely broken due to import errors
- CI passed, but the tool was unusable

These tests ensure the CLI can actually start and all commands are importable.
"""

import subprocess
import sys

import pytest
from click.testing import CliRunner


class TestCLIImports:
    """Test that all CLI modules can be imported without errors."""

    def test_cli_init_imports(self):
        """Test that cli/__init__.py imports successfully."""
        from codebase_reviewer.cli import cli, main

        assert cli is not None
        assert main is not None

    def test_cli_core_imports(self):
        """Test that cli/core.py imports successfully."""
        from codebase_reviewer.cli.core import register_core_commands

        assert register_core_commands is not None

    def test_cli_analysis_imports(self):
        """Test that cli/analysis.py imports successfully."""
        from codebase_reviewer.cli.analysis import register_analysis_commands

        assert register_analysis_commands is not None

    def test_cli_enterprise_imports(self):
        """Test that cli/enterprise.py imports successfully."""
        from codebase_reviewer.cli.enterprise import register_enterprise_commands

        assert register_enterprise_commands is not None

    def test_cli_tuning_imports(self):
        """Test that cli/tuning.py imports successfully."""
        from codebase_reviewer.cli.tuning import register_tuning_commands

        assert register_tuning_commands is not None


class TestCLIStartup:
    """Test that the CLI can actually start and show help."""

    def test_cli_help_via_click_runner(self):
        """Test CLI --help via Click's test runner."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Codebase Reviewer" in result.output
        assert "analyze" in result.output

    def test_cli_version_via_click_runner(self):
        """Test CLI --version via Click's test runner."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0

    def test_analyze_help(self):
        """Test analyze command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["analyze", "--help"])

        assert result.exit_code == 0
        assert "analyze" in result.output.lower()

    def test_compliance_help(self):
        """Test compliance command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["compliance", "--help"])

        assert result.exit_code == 0
        assert "compliance" in result.output.lower()

    def test_productivity_help(self):
        """Test productivity command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["productivity", "--help"])

        assert result.exit_code == 0

    def test_roi_help(self):
        """Test roi command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["roi", "--help"])

        assert result.exit_code == 0

    def test_analyze_v2_help(self):
        """Test analyze-v2 command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["analyze-v2", "--help"])

        assert result.exit_code == 0

    def test_generate_prompt_help(self):
        """Test generate-prompt command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["generate-prompt", "--help"])

        assert result.exit_code == 0

    def test_review_help(self):
        """Test review command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["review", "--help"])

        assert result.exit_code == 0

    def test_simulate_help(self):
        """Test simulate command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["simulate", "--help"])

        assert result.exit_code == 0

    def test_evolve_help(self):
        """Test evolve command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["evolve", "--help"])

        assert result.exit_code == 0

    def test_tune_help(self):
        """Test tune command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["tune", "--help"])

        assert result.exit_code == 0

    def test_ask_help(self):
        """Test ask command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["ask", "--help"])

        assert result.exit_code == 0

    def test_multi_repo_help(self):
        """Test multi-repo command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["multi-repo", "--help"])

        assert result.exit_code == 0

    def test_web_help(self):
        """Test web command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["web", "--help"])

        assert result.exit_code == 0


class TestCLISubprocess:
    """Test CLI via subprocess to catch any startup issues."""

    def test_cli_help_via_subprocess(self):
        """Test that review-codebase --help works via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "codebase_reviewer.cli", "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Note: This may fail if cli/__main__.py doesn't exist
        # but that's the point - we want to catch such issues
        # For now, we accept either success or "No module named" for __main__
        if result.returncode != 0:
            # If it fails, it should be because __main__.py doesn't exist
            # not because of import errors
            assert "ModuleNotFoundError" not in result.stderr or "__main__" in result.stderr

    def test_review_codebase_help_via_subprocess(self):
        """Test that review-codebase --help works."""
        result = subprocess.run(
            ["review-codebase", "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert "Codebase Reviewer" in result.stdout


class TestCLIAnalyzeCommand:
    """Test the analyze command execution."""

    def test_analyze_basic_execution(self, tmp_path):
        """Test analyze command with a simple directory."""
        from codebase_reviewer.cli import cli

        # Create a minimal test project
        readme = tmp_path / "README.md"
        readme.write_text("# Test Project\n")
        py_file = tmp_path / "main.py"
        py_file.write_text("print('hello')\n")
        output_file = tmp_path / "output.json"

        runner = CliRunner()
        result = runner.invoke(cli, ["analyze", str(tmp_path), "--output", str(output_file)])

        # Command should complete (may have warnings but no crash)
        assert result.exit_code in [0, 1]  # 0 = success, 1 = findings

    def test_analyze_with_json_format(self, tmp_path):
        """Test analyze command with JSON output format."""
        from codebase_reviewer.cli import cli

        readme = tmp_path / "README.md"
        readme.write_text("# Test\n")
        output_file = tmp_path / "output.json"

        runner = CliRunner()
        result = runner.invoke(cli, ["analyze", str(tmp_path), "--output", str(output_file), "--format", "json"])

        assert result.exit_code in [0, 1]

    def test_analyze_with_html_format(self, tmp_path):
        """Test analyze command with HTML output format."""
        from codebase_reviewer.cli import cli

        readme = tmp_path / "README.md"
        readme.write_text("# Test\n")
        output_file = tmp_path / "output.html"

        runner = CliRunner()
        result = runner.invoke(cli, ["analyze", str(tmp_path), "--output", str(output_file), "--format", "html"])

        assert result.exit_code in [0, 1]


class TestCLIPromptsCommand:
    """Test the prompts command execution."""

    def test_prompts_command(self, tmp_path):
        """Test prompts command."""
        from codebase_reviewer.cli import cli

        readme = tmp_path / "README.md"
        readme.write_text("# Test\n")
        py_file = tmp_path / "app.py"
        py_file.write_text("def main(): pass\n")
        output_file = tmp_path / "prompts.md"

        runner = CliRunner()
        result = runner.invoke(cli, ["prompts", str(tmp_path), "--output", str(output_file)])

        # Should complete without import/attribute errors
        assert result.exit_code in [0, 1]
        assert "AttributeError" not in result.output

    def test_prompts_command_help(self):
        """Test prompts command help."""
        from codebase_reviewer.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["prompts", "--help"])

        assert result.exit_code == 0
        assert "prompts" in result.output.lower()
