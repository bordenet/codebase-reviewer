"""Tests for auto-configuration."""

import pytest
from pathlib import Path
from codebase_reviewer.config.auto_config import AutoConfig


class TestAutoConfig:
    """Tests for AutoConfig."""

    def test_initialization(self, tmp_path):
        """Test auto-config initialization."""
        config = AutoConfig(tmp_path)
        assert config.repo_path == tmp_path
        assert config.config is not None

    def test_detect_python_package(self, tmp_path):
        """Test detecting Python package."""
        # Create setup.py
        (tmp_path / "setup.py").write_text("from setuptools import setup")

        config = AutoConfig(tmp_path)

        assert config.config["project_type"] == "python-package"

    def test_detect_node_package(self, tmp_path):
        """Test detecting Node.js package."""
        # Create package.json
        (tmp_path / "package.json").write_text('{"name": "test"}')

        config = AutoConfig(tmp_path)

        assert config.config["project_type"] == "node-package"

    def test_detect_react_app(self, tmp_path):
        """Test detecting React app."""
        # Create package.json with React
        (tmp_path / "package.json").write_text('{"dependencies": {"react": "^18.0.0"}}')

        config = AutoConfig(tmp_path)

        assert config.config["project_type"] == "react-app"

    def test_detect_languages(self, tmp_path):
        """Test detecting languages."""
        # Create Python files
        (tmp_path / "main.py").write_text('print("hello")')
        (tmp_path / "test.py").write_text("import pytest")

        # Create JavaScript files
        (tmp_path / "app.js").write_text('console.log("hello")')

        config = AutoConfig(tmp_path)

        assert "python" in config.config["languages"]
        assert "javascript" in config.config["languages"]

    def test_detect_django_framework(self, tmp_path):
        """Test detecting Django framework."""
        # Create requirements.txt with Django
        (tmp_path / "requirements.txt").write_text("Django==4.0.0\npsycopg2==2.9.0")

        config = AutoConfig(tmp_path)

        assert "Django" in config.config["frameworks"]

    def test_detect_react_framework(self, tmp_path):
        """Test detecting React framework."""
        # Create package.json with React
        (tmp_path / "package.json").write_text('{"dependencies": {"react": "^18.0.0"}}')

        config = AutoConfig(tmp_path)

        assert "React" in config.config["frameworks"]

    def test_detect_pytest(self, tmp_path):
        """Test detecting pytest."""
        # Create pytest.ini
        (tmp_path / "pytest.ini").write_text("[pytest]")

        config = AutoConfig(tmp_path)

        assert config.config["test_framework"] == "pytest"

    def test_detect_github_actions(self, tmp_path):
        """Test detecting GitHub Actions."""
        # Create GitHub Actions workflow
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        (workflows_dir / "ci.yml").write_text("name: CI")

        config = AutoConfig(tmp_path)

        assert "GitHub Actions" in config.config["ci_cd"]

    def test_detect_gitlab_ci(self, tmp_path):
        """Test detecting GitLab CI."""
        # Create .gitlab-ci.yml
        (tmp_path / ".gitlab-ci.yml").write_text("stages:\n  - test")

        config = AutoConfig(tmp_path)

        assert "GitLab CI" in config.config["ci_cd"]

    def test_get_config(self, tmp_path):
        """Test getting configuration."""
        config = AutoConfig(tmp_path)

        result = config.get_config()

        assert "project_type" in result
        assert "languages" in result
        assert "frameworks" in result
        assert "test_framework" in result
        assert "build_tool" in result
        assert "ci_cd" in result
        assert "ignore_patterns" in result

    def test_default_ignore_patterns(self, tmp_path):
        """Test default ignore patterns."""
        config = AutoConfig(tmp_path)

        patterns = config.config["ignore_patterns"]

        assert "__pycache__" in patterns
        assert "node_modules" in patterns
        assert ".git" in patterns
        assert "venv" in patterns
