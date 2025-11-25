"""Tests for quality_checker module."""

import os
import tempfile
from pathlib import Path

import pytest

from codebase_reviewer.analyzers.quality_checker import QualityChecker
from codebase_reviewer.models import Severity


@pytest.fixture
def temp_repo():
    """Create a temporary repository for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def quality_checker():
    """Create a QualityChecker instance."""
    return QualityChecker()


def test_analyze_quality_empty_repo(quality_checker, temp_repo):
    """Test analyzing an empty repository."""
    issues = quality_checker.analyze_quality(temp_repo)
    assert issues == []


def test_check_for_todos_python(quality_checker, temp_repo):
    """Test TODO detection in Python files."""
    test_file = Path(temp_repo) / "test.py"
    test_file.write_text(
        "# TODO: Fix this\n"
        "# FIXME: Broken code\n"
        "# HACK: Temporary workaround\n"
        "# XXX: Review this\n"
        "def foo():\n"
        "    pass\n"
    )

    issues = quality_checker._check_for_todos(temp_repo)
    assert len(issues) == 4
    assert all(issue.severity == Severity.LOW for issue in issues)
    assert any("TODO" in issue.title for issue in issues)
    assert any("FIXME" in issue.title for issue in issues)
    assert any("HACK" in issue.title for issue in issues)
    assert any("XXX" in issue.title for issue in issues)


def test_check_for_todos_typescript(quality_checker, temp_repo):
    """Test TODO detection in TypeScript files."""
    test_file = Path(temp_repo) / "test.ts"
    test_file.write_text("# TODO: Implement feature\nfunction test() {}\n")

    issues = quality_checker._check_for_todos(temp_repo)
    assert len(issues) == 1
    assert "TODO" in issues[0].title
    assert "test.ts" in issues[0].source


def test_check_for_todos_case_insensitive(quality_checker, temp_repo):
    """Test that TODO detection is case-insensitive."""
    test_file = Path(temp_repo) / "test.py"
    test_file.write_text("# todo: lowercase todo\n# ToDo: Mixed case\n")

    issues = quality_checker._check_for_todos(temp_repo)
    assert len(issues) == 2


def test_check_for_todos_skips_directories(quality_checker, temp_repo):
    """Test that certain directories are skipped."""
    # Create files in directories that should be skipped
    for skip_dir in [".git", "node_modules", ".venv", "__pycache__"]:
        dir_path = Path(temp_repo) / skip_dir
        dir_path.mkdir()
        (dir_path / "test.py").write_text("# TODO: Should be skipped\n")

    issues = quality_checker._check_for_todos(temp_repo)
    assert len(issues) == 0


def test_check_for_security_issues_hardcoded_password(quality_checker, temp_repo):
    """Test detection of hardcoded passwords."""
    test_file = Path(temp_repo) / "config.py"
    test_file.write_text('password = "secret123"\n')

    issues = quality_checker._check_for_security_issues(temp_repo)
    assert len(issues) == 1
    assert issues[0].severity == Severity.HIGH
    assert "password" in issues[0].description.lower()


def test_check_for_security_issues_api_key(quality_checker, temp_repo):
    """Test detection of hardcoded API keys."""
    test_file = Path(temp_repo) / "config.py"
    test_file.write_text('api_key = "abc123xyz"\napi-key = "def456"\n')

    issues = quality_checker._check_for_security_issues(temp_repo)
    assert len(issues) >= 1
    assert any("API key" in issue.description for issue in issues)


def test_check_for_security_issues_secret(quality_checker, temp_repo):
    """Test detection of hardcoded secrets."""
    test_file = Path(temp_repo) / "config.py"
    test_file.write_text('secret = "my_secret_value"\n')

    issues = quality_checker._check_for_security_issues(temp_repo)
    assert len(issues) == 1
    assert "secret" in issues[0].description.lower()


def test_check_for_security_issues_eval(quality_checker, temp_repo):
    """Test detection of eval() usage."""
    test_file = Path(temp_repo) / "dangerous.py"
    test_file.write_text('result = eval("1 + 1")\n')

    issues = quality_checker._check_for_security_issues(temp_repo)
    assert len(issues) == 1
    assert "eval()" in issues[0].description


def test_check_for_security_issues_exec(quality_checker, temp_repo):
    """Test detection of exec() usage."""
    test_file = Path(temp_repo) / "dangerous.py"
    test_file.write_text("exec(\"print('hello')\")\n")

    issues = quality_checker._check_for_security_issues(temp_repo)
    assert len(issues) == 1
    assert "exec()" in issues[0].description


def test_check_for_security_issues_skips_test_directories(quality_checker, temp_repo):
    """Test that test directories are skipped for security checks."""
    for test_dir in ["tests", "test"]:
        dir_path = Path(temp_repo) / test_dir
        dir_path.mkdir()
        (dir_path / "test.py").write_text('password = "test123"\n')

    issues = quality_checker._check_for_security_issues(temp_repo)
    assert len(issues) == 0


def test_analyze_quality_combined(quality_checker, temp_repo):
    """Test that analyze_quality combines TODO and security checks."""
    test_file = Path(temp_repo) / "code.py"
    test_file.write_text("# TODO: Fix security\n" 'password = "secret"\n')

    issues = quality_checker.analyze_quality(temp_repo)
    # Now we get 3 issues: TODO + legacy password check + OWASP password check
    assert len(issues) >= 2  # At least TODO and password
    assert any(issue.severity == Severity.LOW for issue in issues)  # TODO
    assert any(issue.severity in [Severity.HIGH, Severity.CRITICAL] for issue in issues)  # password


def test_check_for_todos_handles_read_errors(quality_checker, temp_repo):
    """Test that TODO check handles file read errors gracefully."""
    # Create a file with invalid encoding
    test_file = Path(temp_repo) / "bad.py"
    test_file.write_bytes(b"# TODO: \xff\xfe Invalid UTF-8\n")

    # Should not raise an exception
    issues = quality_checker._check_for_todos(temp_repo)
    # May or may not find the TODO depending on error handling
    assert isinstance(issues, list)


def test_check_for_security_issues_handles_read_errors(quality_checker, temp_repo):
    """Test that security check handles file read errors gracefully."""
    # Create a file with invalid encoding
    test_file = Path(temp_repo) / "bad.py"
    test_file.write_bytes(b'password = "\xff\xfe"\n')

    # Should not raise an exception
    issues = quality_checker._check_for_security_issues(temp_repo)
    assert isinstance(issues, list)
