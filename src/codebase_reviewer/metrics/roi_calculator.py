"""ROI calculator for code analysis tool."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ROIMetrics:
    """ROI calculation metrics."""

    # Input metrics
    team_size: int
    avg_developer_salary: float
    hours_per_week: float = 40.0

    # Analysis results
    critical_issues_found: int = 0
    high_issues_found: int = 0
    medium_issues_found: int = 0
    low_issues_found: int = 0

    # Time savings
    avg_time_per_critical_fix: float = 8.0  # hours
    avg_time_per_high_fix: float = 4.0  # hours
    avg_time_per_medium_fix: float = 2.0  # hours
    avg_time_per_low_fix: float = 0.5  # hours

    # Cost of bugs in production
    avg_cost_per_production_bug: float = 5000.0  # dollars
    production_bug_prevention_rate: float = 0.7  # 70% of issues would reach production

    # Tool costs
    tool_setup_hours: float = 2.0
    tool_maintenance_hours_per_month: float = 1.0
    tool_license_cost_per_month: float = 0.0  # Free for open source


@dataclass
class ROIReport:
    """ROI calculation report."""

    # Time savings
    total_hours_saved: float
    total_hours_cost: float

    # Bug prevention
    bugs_prevented: int
    bug_prevention_value: float

    # Tool costs
    total_tool_cost: float

    # ROI calculation
    total_value: float
    net_value: float
    roi_percentage: float
    payback_period_days: float

    # Breakdown
    breakdown: Dict[str, float]


class ROICalculator:
    """Calculate ROI for code analysis tool."""

    def calculate_roi(self, metrics: ROIMetrics, months: int = 12) -> ROIReport:
        """Calculate ROI for the tool.

        Args:
            metrics: ROI metrics
            months: Number of months to calculate for

        Returns:
            ROI report
        """
        # Calculate hourly rate
        hourly_rate = metrics.avg_developer_salary / (metrics.hours_per_week * 52)

        # Calculate time saved by fixing issues early
        hours_saved = (
            metrics.critical_issues_found * metrics.avg_time_per_critical_fix
            + metrics.high_issues_found * metrics.avg_time_per_high_fix
            + metrics.medium_issues_found * metrics.avg_time_per_medium_fix
            + metrics.low_issues_found * metrics.avg_time_per_low_fix
        )

        # Calculate value of time saved
        time_value = hours_saved * hourly_rate

        # Calculate bugs prevented
        total_issues = metrics.critical_issues_found + metrics.high_issues_found + metrics.medium_issues_found
        bugs_prevented = int(total_issues * metrics.production_bug_prevention_rate)

        # Calculate value of bug prevention
        bug_prevention_value = bugs_prevented * metrics.avg_cost_per_production_bug

        # Calculate tool costs
        setup_cost = metrics.tool_setup_hours * hourly_rate
        maintenance_cost = metrics.tool_maintenance_hours_per_month * hourly_rate * months
        license_cost = metrics.tool_license_cost_per_month * months
        total_tool_cost = setup_cost + maintenance_cost + license_cost

        # Calculate total value and ROI
        total_value = time_value + bug_prevention_value
        net_value = total_value - total_tool_cost
        roi_percentage = (net_value / total_tool_cost * 100) if total_tool_cost > 0 else 0

        # Calculate payback period
        monthly_value = total_value / months
        payback_period_days = (total_tool_cost / monthly_value * 30) if monthly_value > 0 else 0

        # Create breakdown
        breakdown = {
            "time_savings": time_value,
            "bug_prevention": bug_prevention_value,
            "setup_cost": setup_cost,
            "maintenance_cost": maintenance_cost,
            "license_cost": license_cost,
        }

        return ROIReport(
            total_hours_saved=hours_saved,
            total_hours_cost=time_value,
            bugs_prevented=bugs_prevented,
            bug_prevention_value=bug_prevention_value,
            total_tool_cost=total_tool_cost,
            total_value=total_value,
            net_value=net_value,
            roi_percentage=roi_percentage,
            payback_period_days=payback_period_days,
            breakdown=breakdown,
        )

    def generate_report_text(self, report: ROIReport) -> str:
        """Generate human-readable ROI report.

        Args:
            report: ROI report

        Returns:
            Report text
        """
        lines = [
            "=" * 60,
            "ROI ANALYSIS REPORT",
            "=" * 60,
            "",
            "TIME SAVINGS",
            f"  Total Hours Saved: {report.total_hours_saved:.1f} hours",
            f"  Value of Time Saved: ${report.total_hours_cost:,.2f}",
            "",
            "BUG PREVENTION",
            f"  Bugs Prevented: {report.bugs_prevented}",
            f"  Value of Bug Prevention: ${report.bug_prevention_value:,.2f}",
            "",
            "TOOL COSTS",
            f"  Setup Cost: ${report.breakdown['setup_cost']:,.2f}",
            f"  Maintenance Cost: ${report.breakdown['maintenance_cost']:,.2f}",
            f"  License Cost: ${report.breakdown['license_cost']:,.2f}",
            f"  Total Tool Cost: ${report.total_tool_cost:,.2f}",
            "",
            "ROI SUMMARY",
            f"  Total Value Generated: ${report.total_value:,.2f}",
            f"  Net Value: ${report.net_value:,.2f}",
            f"  ROI: {report.roi_percentage:.1f}%",
            f"  Payback Period: {report.payback_period_days:.0f} days",
            "",
            "=" * 60,
        ]

        if report.roi_percentage > 500:
            lines.append("🎉 EXCELLENT ROI! This tool pays for itself many times over.")
        elif report.roi_percentage > 200:
            lines.append("✅ GREAT ROI! This tool provides significant value.")
        elif report.roi_percentage > 100:
            lines.append("👍 GOOD ROI! This tool is worth the investment.")
        elif report.roi_percentage > 0:
            lines.append("⚠️  POSITIVE ROI, but consider optimizing usage.")
        else:
            lines.append("❌ NEGATIVE ROI - Review tool usage and configuration.")

        lines.append("=" * 60)

        return "\n".join(lines)
