"""Extract code blocks from LLM responses."""

import re
from typing import Dict, List, Tuple
from pathlib import Path


class CodeExtractor:
    """Extracts code blocks from markdown-formatted LLM responses."""

    @staticmethod
    def extract_code_blocks(content: str) -> Dict[str, List[Tuple[str, str]]]:
        """Extract all code blocks from markdown content.

        Args:
            content: Markdown content with code blocks

        Returns:
            Dict mapping language -> list of (code, metadata) tuples

        Example:
            ```python
            # File: main.py
            print("hello")
            ```

            Returns: {"python": [("print(\"hello\")", "File: main.py")]}
        """
        # Pattern: ```language\n# File: path\ncode\n```
        pattern = r"```(\w+)\n(.*?)\n```"
        blocks: Dict[str, List[Tuple[str, str]]] = {}

        for match in re.finditer(pattern, content, re.DOTALL):
            language = match.group(1)
            code_content = match.group(2)

            # Extract file path if present
            file_match = re.match(r"#\s*File:\s*(.+?)\n", code_content)
            metadata = ""

            if file_match:
                metadata = file_match.group(1).strip()
                # Remove the file comment from code
                code_content = code_content[file_match.end() :]

            if language not in blocks:
                blocks[language] = []

            blocks[language].append((code_content.strip(), metadata))

        return blocks

    @staticmethod
    def extract_go_files(content: str) -> Dict[str, str]:
        """Extract Go source files from LLM response.

        Args:
            content: LLM response containing Go code blocks

        Returns:
            Dict mapping file path -> file content

        Example:
            ```go
            // File: cmd/generate-docs/main.go
            package main
            func main() {}
            ```

            Returns: {"cmd/generate-docs/main.go": "package main\nfunc main() {}"}
        """
        blocks = CodeExtractor.extract_code_blocks(content)
        go_files = {}

        for code, metadata in blocks.get("go", []):
            if metadata:
                # metadata is the file path
                go_files[metadata] = code
            else:
                # No file path specified, try to infer from package
                package_match = re.match(r"package\s+(\w+)", code)
                if package_match:
                    pkg_name = package_match.group(1)
                    if pkg_name == "main":
                        go_files["cmd/generate-docs/main.go"] = code
                    else:
                        go_files[f"pkg/{pkg_name}/{pkg_name}.go"] = code

        return go_files

    @staticmethod
    def extract_project_structure(content: str) -> Dict[str, str]:
        """Extract complete project structure from LLM response.

        Looks for all code blocks and organizes them by file path.

        Args:
            content: LLM response with code blocks

        Returns:
            Dict mapping file path -> file content
        """
        all_blocks = CodeExtractor.extract_code_blocks(content)
        project_files = {}

        # Map language extensions
        lang_extensions = {
            "go": ".go",
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "yaml": ".yaml",
            "json": ".json",
            "markdown": ".md",
            "bash": ".sh",
            "shell": ".sh",
        }

        for language, blocks in all_blocks.items():
            extension = lang_extensions.get(language.lower(), f".{language}")

            for code, metadata in blocks:
                if metadata:
                    # Use specified file path
                    file_path = metadata
                else:
                    # Generate a default path
                    file_path = f"generated/{language}/file{extension}"

                project_files[file_path] = code

        return project_files

    @staticmethod
    def validate_go_project(files: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Validate that extracted Go files form a valid project.

        Args:
            files: Dict of file path -> content

        Returns:
            (is_valid, list of validation errors)
        """
        errors = []

        # Check for main package
        has_main = any("package main" in content for content in files.values())

        if not has_main:
            errors.append("No main package found")

        # Check for go.mod
        has_go_mod = any(path.endswith("go.mod") for path in files.keys())

        if not has_go_mod:
            errors.append("No go.mod file found (will need to generate)")

        # Check that all .go files have package declarations
        for path, content in files.items():
            if path.endswith(".go"):
                if not re.search(r"^\s*package\s+\w+", content, re.MULTILINE):
                    errors.append(f"File {path} missing package declaration")

        return len(errors) == 0, errors
