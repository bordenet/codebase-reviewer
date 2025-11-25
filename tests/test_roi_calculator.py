"""Tests for ROI calculator."""

import pytest

from codebase_reviewer.metrics.roi_calculator import ROICalculator, ROIMetrics


class TestROICalculator:
    """Tests for ROICalculator."""

    def test_initialization(self):
        """Test ROI calculator initialization."""
        calculator = ROICalculator()
        assert calculator is not None

    def test_calculate_roi_basic(self):
        """Test basic ROI calculation."""
        calculator = ROICalculator()

        metrics = ROIMetrics(
            team_size=5,
            avg_developer_salary=100000,
            critical_issues_found=10,
            high_issues_found=20,
            medium_issues_found=30,
            low_issues_found=40,
        )

        report = calculator.calculate_roi(metrics, months=12)

        assert report.total_hours_saved > 0
        assert report.total_hours_cost > 0
        assert report.bugs_prevented > 0
        assert report.bug_prevention_value > 0
        assert report.total_value > 0
        assert report.roi_percentage > 0

    def test_calculate_roi_high_value(self):
        """Test ROI calculation with high value."""
        calculator = ROICalculator()

        metrics = ROIMetrics(
            team_size=10,
            avg_developer_salary=120000,
            critical_issues_found=50,
            high_issues_found=100,
            medium_issues_found=200,
            low_issues_found=300,
        )

        report = calculator.calculate_roi(metrics, months=12)

        # With many issues found, ROI should be very high
        assert report.roi_percentage > 500
        assert report.net_value > 0
        assert report.payback_period_days < 30

    def test_calculate_roi_low_value(self):
        """Test ROI calculation with low value."""
        calculator = ROICalculator()

        metrics = ROIMetrics(
            team_size=1,
            avg_developer_salary=50000,
            critical_issues_found=1,
            high_issues_found=2,
            medium_issues_found=3,
            low_issues_found=5,
        )

        report = calculator.calculate_roi(metrics, months=12)

        # With few issues, ROI should be lower but still positive
        assert report.total_value > 0
        assert report.roi_percentage > 0

    def test_time_savings_calculation(self):
        """Test time savings calculation."""
        calculator = ROICalculator()

        metrics = ROIMetrics(
            team_size=5,
            avg_developer_salary=100000,
            critical_issues_found=10,
            high_issues_found=0,
            medium_issues_found=0,
            low_issues_found=0,
            avg_time_per_critical_fix=8.0,
        )

        report = calculator.calculate_roi(metrics, months=12)

        # 10 critical issues * 8 hours = 80 hours saved
        assert report.total_hours_saved == 80.0

    def test_bug_prevention_calculation(self):
        """Test bug prevention calculation."""
        calculator = ROICalculator()

        metrics = ROIMetrics(
            team_size=5,
            avg_developer_salary=100000,
            critical_issues_found=10,
            high_issues_found=10,
            medium_issues_found=10,
            production_bug_prevention_rate=0.7,
            avg_cost_per_production_bug=5000.0,
        )

        report = calculator.calculate_roi(metrics, months=12)

        # 30 total issues * 0.7 = 21 bugs prevented
        assert report.bugs_prevented == 21
        assert report.bug_prevention_value == 21 * 5000.0

    def test_tool_cost_calculation(self):
        """Test tool cost calculation."""
        calculator = ROICalculator()

        metrics = ROIMetrics(
            team_size=5,
            avg_developer_salary=100000,
            critical_issues_found=10,
            tool_setup_hours=2.0,
            tool_maintenance_hours_per_month=1.0,
            tool_license_cost_per_month=100.0,
        )

        report = calculator.calculate_roi(metrics, months=12)

        # Setup + (maintenance * 12) + (license * 12)
        hourly_rate = 100000 / (40 * 52)
        expected_setup = 2.0 * hourly_rate
        expected_maintenance = 1.0 * hourly_rate * 12
        expected_license = 100.0 * 12
        expected_total = expected_setup + expected_maintenance + expected_license

        assert abs(report.total_tool_cost - expected_total) < 1.0

    def test_generate_report_text(self):
        """Test generating report text."""
        calculator = ROICalculator()

        metrics = ROIMetrics(
            team_size=5,
            avg_developer_salary=100000,
            critical_issues_found=20,
            high_issues_found=40,
            medium_issues_found=60,
        )

        report = calculator.calculate_roi(metrics, months=12)
        text = calculator.generate_report_text(report)

        assert "ROI ANALYSIS REPORT" in text
        assert "TIME SAVINGS" in text
        assert "BUG PREVENTION" in text
        assert "TOOL COSTS" in text
        assert "ROI SUMMARY" in text
        assert f"{report.roi_percentage:.1f}%" in text

    def test_report_text_excellent_roi(self):
        """Test report text with excellent ROI."""
        calculator = ROICalculator()

        metrics = ROIMetrics(
            team_size=10,
            avg_developer_salary=120000,
            critical_issues_found=100,
            high_issues_found=200,
            medium_issues_found=300,
        )

        report = calculator.calculate_roi(metrics, months=12)
        text = calculator.generate_report_text(report)

        # Should have excellent ROI message
        assert "EXCELLENT ROI" in text or "GREAT ROI" in text
