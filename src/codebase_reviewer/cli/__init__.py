"""Command-line interface for codebase-reviewer."""

import click

from codebase_reviewer.cli.analysis import register_analysis_commands
from codebase_reviewer.cli.core import register_core_commands
from codebase_reviewer.cli.enterprise import register_enterprise_commands
from codebase_reviewer.cli.tuning import register_tuning_commands


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Codebase Reviewer - AI-powered codebase analysis and onboarding tool."""


# Register all command groups
register_core_commands(cli)
register_tuning_commands(cli)
register_analysis_commands(cli)
register_enterprise_commands(cli)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
