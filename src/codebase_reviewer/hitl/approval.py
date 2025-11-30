"""Approval gate system for tool regeneration."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

import click


class ApprovalDecision(Enum):
    """Approval decision types."""

    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"


@dataclass
class ApprovalRequest:
    """Request for approval to regenerate tools."""

    current_version: int
    """Current tool version."""

    proposed_version: int
    """Proposed new version."""

    reason: str
    """Reason for regeneration (e.g., 'obsolescence detected')."""

    changes_summary: str
    """Summary of changes that triggered regeneration."""

    metrics_comparison: Optional[Dict] = None
    """Comparison of metrics between versions."""

    risk_level: str = "medium"
    """Risk level: low, medium, high."""

    auto_approve: bool = False
    """Whether this can be auto-approved."""


@dataclass
class ApprovalResult:
    """Result of an approval decision."""

    decision: ApprovalDecision
    """Approval decision."""

    notes: Optional[str] = None
    """Optional notes from reviewer."""

    modifications: Optional[Dict] = None
    """Optional modifications to apply."""


class ApprovalGate:
    """Manages approval workflow for tool regeneration."""

    def __init__(self, auto_approve_low_risk: bool = False):
        """Initialize approval gate.

        Args:
            auto_approve_low_risk: Whether to auto-approve low-risk changes
        """
        self.auto_approve_low_risk = auto_approve_low_risk

    def request_approval(self, request: ApprovalRequest, interactive: bool = True) -> ApprovalResult:
        """Request approval for tool regeneration.

        Args:
            request: Approval request
            interactive: Whether to prompt user for approval

        Returns:
            Approval result
        """
        # Auto-approve if configured and low risk
        if self.auto_approve_low_risk and request.risk_level == "low" and request.auto_approve:
            return ApprovalResult(
                decision=ApprovalDecision.APPROVED,
                notes="Auto-approved (low risk)",
            )

        if not interactive:
            # Non-interactive mode: require manual approval later
            return ApprovalResult(
                decision=ApprovalDecision.NEEDS_REVIEW,
                notes="Manual review required (non-interactive mode)",
            )

        # Interactive approval
        return self._interactive_approval(request)

    def _interactive_approval(self, request: ApprovalRequest) -> ApprovalResult:
        """Interactive approval workflow.

        Args:
            request: Approval request

        Returns:
            Approval result
        """
        click.echo("\n" + "=" * 70)
        click.echo(click.style("🔍 APPROVAL REQUIRED: Tool Regeneration", fg="yellow", bold=True))
        click.echo("=" * 70)

        click.echo(f"\n📊 Current Version: {request.current_version}")
        click.echo(f"📊 Proposed Version: {request.proposed_version}")
        click.echo(f"\n⚠️  Risk Level: {request.risk_level.upper()}")
        click.echo(f"\n📝 Reason: {request.reason}")

        click.echo(f"\n📋 Changes Summary:")
        for line in request.changes_summary.split("\n"):
            click.echo(f"   {line}")

        if request.metrics_comparison:
            click.echo(f"\n📈 Metrics Comparison:")
            for key, value in request.metrics_comparison.items():
                click.echo(f"   {key}: {value}")

        click.echo("\n" + "=" * 70)
        click.echo("\nOptions:")
        click.echo("  [a] Approve - Proceed with regeneration")
        click.echo("  [r] Reject - Cancel regeneration")
        click.echo("  [v] View details - Show more information")
        click.echo("  [m] Modify - Provide custom parameters")

        while True:
            choice = click.prompt("\nYour decision", type=str, default="a").lower().strip()

            if choice in ["a", "approve"]:
                notes = click.prompt("Optional approval notes", default="", show_default=False)
                return ApprovalResult(
                    decision=ApprovalDecision.APPROVED,
                    notes=notes if notes else None,
                )

            elif choice in ["r", "reject"]:
                notes = click.prompt("Rejection reason", default="User declined", show_default=False)
                return ApprovalResult(
                    decision=ApprovalDecision.REJECTED,
                    notes=notes,
                )

            elif choice in ["v", "view"]:
                self._show_detailed_view(request)
                continue

            elif choice in ["m", "modify"]:
                modifications = self._get_modifications()
                notes = click.prompt("Optional notes", default="", show_default=False)
                return ApprovalResult(
                    decision=ApprovalDecision.APPROVED,
                    notes=notes if notes else None,
                    modifications=modifications,
                )

            else:
                click.echo(click.style("Invalid choice. Please enter a, r, v, or m.", fg="red"))

    def _show_detailed_view(self, request: ApprovalRequest):
        """Show detailed view of approval request."""
        click.echo("\n" + "=" * 70)
        click.echo(click.style("📊 DETAILED VIEW", fg="cyan", bold=True))
        click.echo("=" * 70)

        click.echo(f"\nAuto-approve eligible: {request.auto_approve}")

        if request.metrics_comparison:
            click.echo("\nFull Metrics Comparison:")
            for key, value in request.metrics_comparison.items():
                click.echo(f"  {key}:")
                if isinstance(value, dict):
                    for k, v in value.items():
                        click.echo(f"    {k}: {v}")
                else:
                    click.echo(f"    {value}")

        click.echo("\n" + "=" * 70)

    def _get_modifications(self) -> Dict:
        """Get custom modifications from user."""
        click.echo("\n" + "=" * 70)
        click.echo(click.style("🔧 CUSTOM MODIFICATIONS", fg="cyan", bold=True))
        click.echo("=" * 70)

        modifications = {}

        # Scan mode
        scan_mode = click.prompt(
            "\nScan mode (review/deep_scan/scorch)",
            type=click.Choice(["review", "deep_scan", "scorch"]),
            default="review",
        )
        modifications["scan_mode"] = scan_mode

        # Temperature
        if click.confirm("\nCustomize LLM temperature?", default=False):
            temperature = click.prompt("Temperature (0.0-1.0)", type=float, default=0.3)
            modifications["temperature"] = temperature

        # Max tokens
        if click.confirm("\nCustomize max tokens?", default=False):
            max_tokens = click.prompt("Max tokens", type=int, default=16000)
            modifications["max_tokens"] = max_tokens

        click.echo("\n✅ Modifications configured")
        return modifications

    def format_approval_summary(self, request: ApprovalRequest, result: ApprovalResult) -> str:
        """Format approval summary for logging.

        Args:
            request: Approval request
            result: Approval result

        Returns:
            Formatted summary
        """
        lines = [
            "=" * 70,
            f"APPROVAL SUMMARY: {request.current_version} → {request.proposed_version}",
            "=" * 70,
            f"Decision: {result.decision.value.upper()}",
            f"Reason: {request.reason}",
            f"Risk Level: {request.risk_level}",
        ]

        if result.notes:
            lines.append(f"Notes: {result.notes}")

        if result.modifications:
            lines.append("\nModifications:")
            for key, value in result.modifications.items():
                lines.append(f"  {key}: {value}")

        lines.append("=" * 70)
        return "\n".join(lines)
