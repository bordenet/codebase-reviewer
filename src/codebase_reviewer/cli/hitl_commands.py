"""Human-in-the-Loop CLI commands."""

import sys
from pathlib import Path

import click

from codebase_reviewer.hitl.approval import ApprovalDecision, ApprovalGate, ApprovalRequest
from codebase_reviewer.hitl.rollback import RollbackManager
from codebase_reviewer.hitl.version_manager import ToolVersionManager


def register_hitl_commands(cli):
    """Register HITL commands with the CLI group."""

    @cli.command("versions")
    @click.argument("codebase_path", type=click.Path(exists=True))
    @click.option(
        "--output-dir",
        "-o",
        type=click.Path(),
        default="/tmp/codebase-reviewer",
        help="Base output directory",
    )
    def list_versions(codebase_path, output_dir):
        """List all tool versions for a codebase.

        Shows version history with status, timestamps, and validation results.

        Example:
            review-codebase versions /path/to/codebase
        """
        try:
            codebase_path = Path(codebase_path).resolve()
            output_dir = Path(output_dir)

            version_manager = ToolVersionManager(codebase_path, output_dir)
            versions = version_manager.list_versions()

            if not versions:
                click.echo(click.style("No versions found.", fg="yellow"))
                return

            click.echo(click.style(f"\n📦 Tool Versions for {codebase_path.name}", fg="cyan", bold=True))
            click.echo("=" * 70)

            active_version = version_manager.get_active_version()

            for v in sorted(versions, key=lambda x: x.version, reverse=True):
                # Version header
                status_color = "green" if v.status == "active" else "white"
                active_marker = " ★" if active_version and v.version == active_version.version else ""
                click.echo(f"\n{click.style(f'Version {v.version}{active_marker}', fg=status_color, bold=True)}")

                # Details
                click.echo(f"  Status: {v.status}")
                click.echo(f"  Created: {v.timestamp}")
                click.echo(f"  Validation: {'✓ Passed' if v.validation_passed else '✗ Failed'}")

                if v.llm_model:
                    click.echo(f"  LLM Model: {v.llm_model}")
                if v.llm_cost:
                    click.echo(f"  Cost: ${v.llm_cost:.4f}")
                if v.notes:
                    click.echo(f"  Notes: {v.notes}")

                click.echo(f"  Tools: {v.tools_dir}")
                if v.binary_path:
                    click.echo(f"  Binary: {v.binary_path}")

            click.echo("\n" + "=" * 70)
            click.echo(f"Total versions: {len(versions)}")
            if active_version:
                click.echo(f"Active version: {active_version.version}")

        except Exception as e:
            click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
            sys.exit(1)

    @cli.command("activate")
    @click.argument("codebase_path", type=click.Path(exists=True))
    @click.argument("version", type=int)
    @click.option(
        "--output-dir",
        "-o",
        type=click.Path(),
        default="/tmp/codebase-reviewer",
        help="Base output directory",
    )
    def activate_version(codebase_path, version, output_dir):
        """Activate a specific tool version.

        Makes the specified version the active version for the codebase.

        Example:
            review-codebase activate /path/to/codebase 2
        """
        try:
            codebase_path = Path(codebase_path).resolve()
            output_dir = Path(output_dir)

            version_manager = ToolVersionManager(codebase_path, output_dir)
            activated = version_manager.set_active_version(version)

            click.echo(click.style(f"\n✅ Activated version {version}", fg="green", bold=True))
            click.echo(f"   Created: {activated.timestamp}")
            click.echo(f"   Tools: {activated.tools_dir}")
            if activated.binary_path:
                click.echo(f"   Binary: {activated.binary_path}")

        except Exception as e:
            click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
            sys.exit(1)

    @cli.command("rollback")
    @click.argument("codebase_path", type=click.Path(exists=True))
    @click.option(
        "--to-version",
        "-v",
        type=int,
        help="Version to rollback to (default: previous version)",
    )
    @click.option(
        "--output-dir",
        "-o",
        type=click.Path(),
        default="/tmp/codebase-reviewer",
        help="Base output directory",
    )
    @click.option(
        "--no-restore",
        is_flag=True,
        help="Don't restore files to workspace (only change active version)",
    )
    @click.option(
        "--list",
        "list_targets",
        is_flag=True,
        help="List available rollback targets",
    )
    def rollback(codebase_path, to_version, output_dir, no_restore, list_targets):
        """Rollback to a previous tool version.

        Reverts to a previous working version of the Phase 2 tools.

        Examples:
            review-codebase rollback /path/to/codebase --list
            review-codebase rollback /path/to/codebase  # rollback to previous
            review-codebase rollback /path/to/codebase --to-version 2
        """
        try:
            codebase_path = Path(codebase_path).resolve()
            output_dir = Path(output_dir)

            version_manager = ToolVersionManager(codebase_path, output_dir)
            rollback_manager = RollbackManager(version_manager)

            # List targets
            if list_targets:
                targets = rollback_manager.list_rollback_targets()
                if not targets:
                    click.echo(click.style("No rollback targets available.", fg="yellow"))
                    return

                click.echo(click.style(f"\n📋 Rollback Targets for {codebase_path.name}", fg="cyan", bold=True))
                click.echo("=" * 70)

                for target in targets:
                    status_marker = "★" if target.status == "active" else " "
                    click.echo(f"\n{status_marker} Version {target.version}")
                    click.echo(f"  Created: {target.timestamp}")
                    click.echo(f"  Status: {target.status}")
                    click.echo(f"  Validation: {'✓ Passed' if target.validation_passed else '✗ Failed'}")
                    if target.notes:
                        click.echo(f"  Notes: {target.notes}")

                click.echo("\n" + "=" * 70)
                return

            # Perform rollback
            if not rollback_manager.can_rollback():
                click.echo(click.style("No versions available for rollback.", fg="yellow"))
                return

            # Confirm rollback
            current = version_manager.get_active_version()
            if current:
                click.echo(f"\nCurrent version: {current.version}")

            target_desc = f"version {to_version}" if to_version else "previous version"
            if not click.confirm(f"\n⚠️  Rollback to {target_desc}?", default=True):
                click.echo("Rollback cancelled.")
                return

            # Execute rollback
            restore = not no_restore
            if to_version:
                activated = rollback_manager.rollback_to_version(to_version, restore_to_workspace=restore)
            else:
                activated = rollback_manager.rollback_to_previous(restore_to_workspace=restore)

            click.echo(click.style(f"\n✅ Rolled back to version {activated.version}", fg="green", bold=True))
            if restore:
                click.echo("   Files restored to workspace")

        except Exception as e:
            click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
            sys.exit(1)

    @cli.command("approve")
    @click.argument("codebase_path", type=click.Path(exists=True))
    @click.option(
        "--reason",
        "-r",
        required=True,
        help="Reason for regeneration",
    )
    @click.option(
        "--risk-level",
        type=click.Choice(["low", "medium", "high"]),
        default="medium",
        help="Risk level of the change",
    )
    @click.option(
        "--auto",
        is_flag=True,
        help="Auto-approve without interactive prompt",
    )
    @click.option(
        "--output-dir",
        "-o",
        type=click.Path(),
        default="/tmp/codebase-reviewer",
        help="Base output directory",
    )
    def request_approval(codebase_path, reason, risk_level, auto, output_dir):
        """Request approval for tool regeneration.

        Creates an approval gate for regenerating Phase 2 tools.

        Example:
            review-codebase approve /path/to/codebase --reason "Obsolescence detected"
        """
        try:
            codebase_path = Path(codebase_path).resolve()
            output_dir = Path(output_dir)

            version_manager = ToolVersionManager(codebase_path, output_dir)
            current = version_manager.get_active_version()
            next_version = version_manager.get_next_version()

            # Create approval request
            request = ApprovalRequest(
                current_version=current.version if current else 0,
                proposed_version=next_version,
                reason=reason,
                changes_summary=f"Regenerating tools to version {next_version}",
                risk_level=risk_level,
                auto_approve=auto,
            )

            # Process approval
            approval_gate = ApprovalGate(auto_approve_low_risk=auto)
            result = approval_gate.request_approval(request, interactive=not auto)

            # Display result
            if result.decision == ApprovalDecision.APPROVED:
                click.echo(click.style("\n✅ Regeneration APPROVED", fg="green", bold=True))
                if result.notes:
                    click.echo(f"   Notes: {result.notes}")
                if result.modifications:
                    click.echo("\n   Modifications:")
                    for key, value in result.modifications.items():
                        click.echo(f"     {key}: {value}")

            elif result.decision == ApprovalDecision.REJECTED:
                click.echo(click.style("\n❌ Regeneration REJECTED", fg="red", bold=True))
                if result.notes:
                    click.echo(f"   Reason: {result.notes}")

            else:
                click.echo(click.style("\n⏸️  Review pending", fg="yellow", bold=True))

        except Exception as e:
            click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
            sys.exit(1)

    @cli.command("history")
    @click.argument("codebase_path", type=click.Path(exists=True))
    @click.option(
        "--output-dir",
        "-o",
        type=click.Path(),
        default="/tmp/codebase-reviewer",
        help="Base output directory",
    )
    def show_history(codebase_path, output_dir):
        """Show version history with changes.

        Displays the complete history of tool versions and their changes.

        Example:
            review-codebase history /path/to/codebase
        """
        try:
            codebase_path = Path(codebase_path).resolve()
            output_dir = Path(output_dir)

            version_manager = ToolVersionManager(codebase_path, output_dir)
            rollback_manager = RollbackManager(version_manager)

            history = rollback_manager.get_rollback_history()

            if not history:
                click.echo(click.style("No version history available.", fg="yellow"))
                return

            click.echo(click.style(f"\n📜 Version History for {codebase_path.name}", fg="cyan", bold=True))
            click.echo("=" * 70)

            for version_info, change_desc in history:
                status_color = "green" if version_info.status == "active" else "white"
                marker = "★" if version_info.status == "active" else "○"

                click.echo(f"\n{marker} {click.style(f'Version {version_info.version}', fg=status_color, bold=True)}")
                click.echo(f"  Created: {version_info.timestamp}")
                click.echo(f"  Change: {change_desc}")
                click.echo(f"  Validation: {'✓ Passed' if version_info.validation_passed else '✗ Failed'}")

            click.echo("\n" + "=" * 70)

        except Exception as e:
            click.echo(click.style(f"\n✗ Error: {str(e)}", fg="red"), err=True)
            sys.exit(1)
