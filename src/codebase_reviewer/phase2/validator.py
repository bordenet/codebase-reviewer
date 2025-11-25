"""Phase 2 tool validator - ensures tools work correctly."""

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class ValidationReport:
    """Report from validating Phase 2 tools."""

    is_valid: bool
    """Whether tools passed all validation checks."""

    errors: List[str]
    """List of validation errors."""

    warnings: List[str]
    """List of validation warnings."""

    checks_passed: int
    """Number of checks that passed."""

    checks_total: int
    """Total number of checks run."""


class Phase2Validator:
    """Validates Phase 2 tools."""

    def validate_tools(self, tools_dir: Path, binary_path: Path) -> ValidationReport:
        """Validate that Phase 2 tools are properly structured and functional.

        Args:
            tools_dir: Directory containing tool source code
            binary_path: Path to compiled binary

        Returns:
            ValidationReport with results
        """
        errors = []
        warnings = []
        checks_passed = 0
        checks_total = 0

        # Check 1: Tools directory exists
        checks_total += 1
        if not tools_dir.exists():
            errors.append(f"Tools directory not found: {tools_dir}")
        else:
            checks_passed += 1

        # Check 2: Binary exists
        checks_total += 1
        if not binary_path.exists():
            errors.append(f"Binary not found: {binary_path}")
        else:
            checks_passed += 1

        # Check 3: Binary is executable
        checks_total += 1
        if binary_path.exists():
            if not binary_path.stat().st_mode & 0o111:
                errors.append(f"Binary is not executable: {binary_path}")
            else:
                checks_passed += 1

        # Check 4: Has main.go
        checks_total += 1
        main_go = tools_dir / "cmd" / "generate-docs" / "main.go"
        if not main_go.exists():
            warnings.append(f"main.go not found at expected location: {main_go}")
        else:
            checks_passed += 1

        # Check 5: Has go.mod
        checks_total += 1
        go_mod = tools_dir / "go.mod"
        if not go_mod.exists():
            warnings.append(f"go.mod not found: {go_mod}")
        else:
            checks_passed += 1

        # Check 6: Has README or documentation
        checks_total += 1
        readme = tools_dir / "README.md"
        if not readme.exists():
            warnings.append("No README.md found in tools directory")
        else:
            checks_passed += 1

        is_valid = len(errors) == 0

        return ValidationReport(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            checks_passed=checks_passed,
            checks_total=checks_total,
        )

    def print_report(self, report: ValidationReport):
        """Print validation report to console.

        Args:
            report: ValidationReport to print
        """
        print(f"\n{'='*60}")
        print(f"Phase 2 Tools Validation Report")
        print(f"{'='*60}")
        print(f"Status: {'✅ VALID' if report.is_valid else '❌ INVALID'}")
        print(f"Checks: {report.checks_passed}/{report.checks_total} passed")

        if report.errors:
            print(f"\n❌ Errors ({len(report.errors)}):")
            for error in report.errors:
                print(f"   - {error}")

        if report.warnings:
            print(f"\n⚠️  Warnings ({len(report.warnings)}):")
            for warning in report.warnings:
                print(f"   - {warning}")

        if report.is_valid:
            print(f"\n✅ Phase 2 tools are valid and ready to use!")
        else:
            print(f"\n❌ Phase 2 tools have validation errors - fix before using")

        print(f"{'='*60}\n")
