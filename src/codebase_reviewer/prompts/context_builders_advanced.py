"""Advanced context builders for prompt generation.

This module contains complex context builders that perform deeper analysis
such as file scanning, git analysis, and code structure inspection.
"""

import ast
import glob
import os
from collections import Counter
from typing import Any, Dict, Optional

from codebase_reviewer.models import RepositoryAnalysis


class AdvancedContextBuilders:
    """Collection of advanced context builder methods requiring deeper analysis."""

    @staticmethod
    def build_observability_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for observability review prompt."""
        import re

        repo_path = analysis.repository_path
        exclude_dirs = {
            ".venv",
            "venv",
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "node_modules",
        }

        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)

        # Scan for logging patterns
        logging_imports = []
        logging_calls = []
        print_statements = []
        exception_handlers = []

        for py_file in python_files[:30]:  # Limit to first 30 files
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    rel_path = os.path.relpath(py_file, repo_path)

                    # Check for logging imports
                    if re.search(r"import logging|from logging", content):
                        logging_imports.append(rel_path)

                    # Count logging calls
                    log_calls = len(
                        re.findall(
                            r"logging\.(debug|info|warning|error|critical|exception)",
                            content,
                        )
                    )
                    if log_calls > 0:
                        logging_calls.append({"file": rel_path, "count": log_calls})

                    # Count print statements
                    print_count = len(re.findall(r"\bprint\(", content))
                    if print_count > 0:
                        print_statements.append({"file": rel_path, "count": print_count})

                    # Count exception handlers
                    except_count = len(re.findall(r"\bexcept\s+", content))
                    if except_count > 0:
                        exception_handlers.append({"file": rel_path, "count": except_count})

            except (IOError, UnicodeDecodeError):
                pass

        return {
            "repository_path": repo_path,
            "files_analyzed": len(python_files[:30]),
            "logging_imports_count": len(logging_imports),
            "files_with_logging": logging_calls[:10],
            "files_with_print": print_statements[:10],
            "files_with_exception_handling": exception_handlers[:10],
            "has_structured_logging": len(logging_imports) > 0,
            "print_vs_logging_ratio": (
                len(print_statements) / max(len(logging_calls), 1) if logging_calls else "N/A (no logging)"
            ),
        }

    @staticmethod
    def build_setup_validation_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for setup validation prompt."""
        docs = analysis.documentation
        validation = analysis.validation
        repo_path = analysis.repository_path

        # Check for setup/build files
        setup_files = []
        for filename in [
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "Pipfile",
            "environment.yml",
            "Dockerfile",
        ]:
            filepath = os.path.join(repo_path, filename)
            if os.path.exists(filepath):
                setup_files.append(filename)

        # Extract setup claims from documentation
        setup_claims = []
        if docs and docs.setup_instructions:
            # Combine all setup text for analysis
            setup_text = " ".join(
                docs.setup_instructions.prerequisites
                + docs.setup_instructions.build_steps
                + docs.setup_instructions.environment_vars
            ).lower()
            if "pip install" in setup_text:
                setup_claims.append("Uses pip for installation")
            if "docker" in setup_text:
                setup_claims.append("Supports Docker deployment")
            if "npm install" in setup_text or "yarn install" in setup_text:
                setup_claims.append("Requires Node.js dependencies")

        # Extract validation drift
        setup_drift = []
        if validation and validation.setup_drift:
            setup_drift = [
                {
                    "claim": d.claim.description if d.claim else "Unknown",
                    "status": d.validation_status.value,
                    "severity": d.severity.value,
                }
                for d in validation.setup_drift[:10]
            ]

        return {
            "setup_files_found": setup_files,
            "setup_claims": setup_claims,
            "setup_drift": setup_drift,
            "has_setup_docs": bool(docs and docs.setup_instructions),
            "setup_completeness": docs.completeness_score if docs else 0,
        }

    @staticmethod
    def build_testing_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for testing strategy prompt."""
        repo_path = analysis.repository_path

        # Find test files
        test_patterns = ["**/test_*.py", "**/*_test.py", "**/tests/**/*.py"]
        test_files = []
        for pattern in test_patterns:
            test_files.extend(glob.glob(os.path.join(repo_path, pattern), recursive=True))

        # Deduplicate and get relative paths
        test_files = list(set([os.path.relpath(f, repo_path) for f in test_files]))

        # Detect test framework
        test_frameworks = []
        dependencies = analysis.code.dependencies if analysis.code else []
        if any("pytest" in dep.name.lower() for dep in dependencies):
            test_frameworks.append("pytest")
        if any("unittest" in dep.name.lower() for dep in dependencies):
            test_frameworks.append("unittest")

        # Organize tests by directory
        test_dirs: Dict[str, Any] = {}
        for test_file in test_files:
            test_dir = os.path.dirname(test_file) or "root"
            if test_dir not in test_dirs:
                test_dirs[test_dir] = []
            test_dirs[test_dir].append(os.path.basename(test_file))

        return {
            "repository_path": repo_path,
            "test_files": test_files[:20],  # Limit to first 20 for brevity
            "test_file_count": len(test_files),
            "test_frameworks": test_frameworks,
            "test_organization": test_dirs,
            "has_tests": len(test_files) > 0,
        }

    @staticmethod
    def build_call_graph_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for call graph and dependency tracing."""
        repo_path = analysis.repository_path
        exclude_dirs = {
            ".venv",
            "venv",
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "node_modules",
        }

        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    python_files.append(os.path.relpath(file_path, repo_path))

        # Analyze imports in each file
        internal_imports: Dict[str, Any] = {}
        external_imports: Dict[str, Any] = {}

        for py_file in python_files[:30]:  # Limit to first 30 files for performance
            try:
                file_path = os.path.join(repo_path, py_file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse imports using AST
                try:
                    tree = ast.parse(content)
                    imports = []
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports.append(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imports.append(node.module)

                    # Separate internal vs external imports
                    internal = [imp for imp in imports if imp.startswith("codebase_reviewer") or imp.startswith("src.")]
                    external = [
                        imp for imp in imports if not imp.startswith("codebase_reviewer") and not imp.startswith("src.")
                    ]

                    if internal:
                        internal_imports[py_file] = internal
                    if external:
                        external_imports[py_file] = external[:10]  # Limit external imports

                except SyntaxError:
                    # Skip files with syntax errors
                    pass

            except (IOError, UnicodeDecodeError):
                # Skip files that can't be read
                pass

        # Count most common internal imports
        all_internal = []
        for imports in internal_imports.values():
            all_internal.extend(imports)

        internal_counts = Counter(all_internal).most_common(10)

        return {
            "total_python_files": len(python_files),
            "files_analyzed": min(30, len(python_files)),
            "internal_dependencies": dict(list(internal_imports.items())[:10]),  # Show first 10 files
            "most_imported_internal": [{"module": mod, "count": count} for mod, count in internal_counts],
            "external_dependencies_sample": dict(list(external_imports.items())[:5]),  # Show 5 examples
        }

    @staticmethod
    def build_git_hotspots_context(analysis: RepositoryAnalysis) -> Optional[Dict[str, Any]]:
        """Build context for git hotspots analysis."""
        try:
            import git

            repo_path = analysis.repository_path

            try:
                repo = git.Repo(repo_path)
            except git.InvalidGitRepositoryError:
                return {"error": "Not a git repository", "repository_path": repo_path}

            # Analyze commits (last 100 commits)
            commits = list(repo.iter_commits("HEAD", max_count=100))

            # Track file changes
            file_changes: Counter = Counter()
            commit_messages = []

            for commit in commits:
                # Get files changed in this commit
                if commit.parents:
                    diffs = commit.parents[0].diff(commit)
                    for diff in diffs:
                        if diff.a_path and diff.a_path.endswith(".py"):
                            file_changes[diff.a_path] += 1
                        if diff.b_path and diff.b_path.endswith(".py"):
                            file_changes[diff.b_path] += 1

                # Collect commit messages for pattern analysis
                msg = (
                    commit.message
                    if isinstance(commit.message, str)
                    else commit.message.decode("utf-8", errors="ignore")
                )
                commit_messages.append(msg.split("\n")[0][:100])  # First line, max 100 chars

            # Get most frequently changed files
            hotspots = file_changes.most_common(15)

            # Analyze commit message patterns
            bug_fix_commits = [
                msg for msg in commit_messages if any(word in msg.lower() for word in ["fix", "bug", "error", "issue"])
            ]
            refactor_commits = [
                msg
                for msg in commit_messages
                if any(word in msg.lower() for word in ["refactor", "cleanup", "improve"])
            ]

            return {
                "total_commits_analyzed": len(commits),
                "hotspot_files": [{"file": file, "change_count": count} for file, count in hotspots],
                "bug_fix_commit_count": len(bug_fix_commits),
                "refactor_commit_count": len(refactor_commits),
                "recent_commit_messages": commit_messages[:10],
            }

        except ImportError:
            return {
                "error": "GitPython not available",
                "repository_path": analysis.repository_path,
            }
        except Exception as e:
            return {
                "error": f"Git analysis failed: {str(e)}",
                "repository_path": analysis.repository_path,
            }
