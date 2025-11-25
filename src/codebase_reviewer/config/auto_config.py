"""Automatic configuration detection for zero-configuration setup."""

from pathlib import Path
from typing import Dict, List, Optional
import json


class AutoConfig:
    """Automatically detect project configuration for zero-configuration setup."""

    def __init__(self, repo_path: Path):
        """Initialize auto-config.

        Args:
            repo_path: Path to repository
        """
        self.repo_path = Path(repo_path)
        self.config = self._detect_config()

    def _detect_config(self) -> Dict:
        """Detect project configuration automatically.

        Returns:
            Configuration dictionary
        """
        config = {
            "project_type": self._detect_project_type(),
            "languages": self._detect_languages(),
            "frameworks": self._detect_frameworks(),
            "test_framework": self._detect_test_framework(),
            "build_tool": self._detect_build_tool(),
            "ci_cd": self._detect_ci_cd(),
            "ignore_patterns": self._get_default_ignore_patterns(),
        }

        return config

    def _detect_project_type(self) -> str:
        """Detect project type.

        Returns:
            Project type (web, cli, library, etc.)
        """
        # Check for common indicators
        if (self.repo_path / "setup.py").exists() or (
            self.repo_path / "pyproject.toml"
        ).exists():
            return "python-package"
        elif (self.repo_path / "package.json").exists():
            package_json = json.loads((self.repo_path / "package.json").read_text())
            if "dependencies" in package_json and "react" in package_json.get(
                "dependencies", {}
            ):
                return "react-app"
            elif "dependencies" in package_json and "express" in package_json.get(
                "dependencies", {}
            ):
                return "node-server"
            return "node-package"
        elif (self.repo_path / "Cargo.toml").exists():
            return "rust-package"
        elif (self.repo_path / "go.mod").exists():
            return "go-module"
        else:
            return "unknown"

    def _detect_languages(self) -> List[str]:
        """Detect programming languages used.

        Returns:
            List of detected languages
        """
        languages = []

        # Check for common file extensions
        extensions = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "javascript",
            ".tsx": "typescript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".c": "c",
            ".cpp": "cpp",
            ".cs": "csharp",
        }

        for ext, lang in extensions.items():
            if list(self.repo_path.rglob(f"*{ext}")):
                if lang not in languages:
                    languages.append(lang)

        return languages

    def _detect_frameworks(self) -> List[str]:
        """Detect frameworks used.

        Returns:
            List of detected frameworks
        """
        frameworks = []

        # Python frameworks
        if (self.repo_path / "requirements.txt").exists():
            requirements = (self.repo_path / "requirements.txt").read_text().lower()
            if "django" in requirements:
                frameworks.append("Django")
            if "flask" in requirements:
                frameworks.append("Flask")
            if "fastapi" in requirements:
                frameworks.append("FastAPI")

        # JavaScript frameworks
        if (self.repo_path / "package.json").exists():
            try:
                package_json = json.loads((self.repo_path / "package.json").read_text())
                deps = {
                    **package_json.get("dependencies", {}),
                    **package_json.get("devDependencies", {}),
                }
                if "react" in deps:
                    frameworks.append("React")
                if "vue" in deps:
                    frameworks.append("Vue")
                if "angular" in deps or "@angular/core" in deps:
                    frameworks.append("Angular")
                if "express" in deps:
                    frameworks.append("Express")
                if "next" in deps:
                    frameworks.append("Next.js")
            except:
                pass

        return frameworks

    def _detect_test_framework(self) -> Optional[str]:
        """Detect test framework.

        Returns:
            Test framework name or None
        """
        # Python
        if (self.repo_path / "pytest.ini").exists() or list(
            self.repo_path.rglob("test_*.py")
        ):
            return "pytest"

        # JavaScript
        if (self.repo_path / "jest.config.js").exists():
            return "jest"

        return None

    def _detect_build_tool(self) -> Optional[str]:
        """Detect build tool.

        Returns:
            Build tool name or None
        """
        if (self.repo_path / "Makefile").exists():
            return "make"
        elif (self.repo_path / "build.gradle").exists():
            return "gradle"
        elif (self.repo_path / "pom.xml").exists():
            return "maven"
        elif (self.repo_path / "Cargo.toml").exists():
            return "cargo"

        return None

    def _detect_ci_cd(self) -> List[str]:
        """Detect CI/CD systems.

        Returns:
            List of detected CI/CD systems
        """
        ci_systems = []

        if (self.repo_path / ".github" / "workflows").exists():
            ci_systems.append("GitHub Actions")
        if (self.repo_path / ".gitlab-ci.yml").exists():
            ci_systems.append("GitLab CI")
        if (self.repo_path / ".travis.yml").exists():
            ci_systems.append("Travis CI")
        if (self.repo_path / "Jenkinsfile").exists():
            ci_systems.append("Jenkins")

        return ci_systems

    def _get_default_ignore_patterns(self) -> List[str]:
        """Get default ignore patterns.

        Returns:
            List of ignore patterns
        """
        return [
            "__pycache__",
            "*.pyc",
            "node_modules",
            ".git",
            ".venv",
            "venv",
            "dist",
            "build",
            "*.egg-info",
            ".pytest_cache",
            "coverage",
            ".coverage",
        ]

    def get_config(self) -> Dict:
        """Get detected configuration.

        Returns:
            Configuration dictionary
        """
        return self.config
