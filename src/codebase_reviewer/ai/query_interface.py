"""Natural language query interface for code analysis."""

from typing import List, Dict, Optional
import re


class QueryInterface:
    """Natural language interface for querying analysis results."""

    def __init__(self):
        """Initialize query interface."""
        self.query_patterns = self._load_query_patterns()

    def _load_query_patterns(self) -> List[dict]:
        """Load natural language query patterns.

        Returns:
            List of query patterns
        """
        return [
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?sql\s+injection",
                "filter": lambda issue: "SQL" in issue.get("rule_id", "").upper()
                or "injection" in issue.get("description", "").lower(),
                "description": "SQL injection vulnerabilities",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?xss",
                "filter": lambda issue: "XSS" in issue.get("rule_id", "").upper()
                or "cross-site" in issue.get("description", "").lower(),
                "description": "XSS vulnerabilities",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?(?:hardcoded\s+)?secrets?",
                "filter": lambda issue: "SECRET" in issue.get("rule_id", "").upper()
                or "hardcoded" in issue.get("description", "").lower(),
                "description": "Hardcoded secrets",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?critical\s+(?:issues|vulnerabilities)",
                "filter": lambda issue: issue.get("severity", "").lower() == "critical",
                "description": "Critical severity issues",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?high\s+(?:priority|severity)",
                "filter": lambda issue: issue.get("severity", "").lower() == "high",
                "description": "High severity issues",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?security\s+(?:issues|vulnerabilities)",
                "filter": lambda issue: "SEC" in issue.get("rule_id", ""),
                "description": "Security issues",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?quality\s+issues",
                "filter": lambda issue: "QUAL" in issue.get("rule_id", ""),
                "description": "Code quality issues",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?(?:issues\s+)?in\s+(.+\.py)",
                "filter": lambda issue, filename: issue.get("file_path", "").endswith(
                    filename
                ),
                "description": "Issues in specific file",
                "extract_param": lambda match: match.group(1),
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?todo",
                "filter": lambda issue: "TODO" in issue.get("rule_id", "").upper()
                or "todo" in issue.get("description", "").lower(),
                "description": "TODO comments",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?(?:missing\s+)?(?:doc|documentation)",
                "filter": lambda issue: "DOC" in issue.get("rule_id", "").upper()
                or "docstring" in issue.get("description", "").lower(),
                "description": "Documentation issues",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?complexity\s+issues",
                "filter": lambda issue: "COMPLEX" in issue.get("rule_id", "").upper()
                or "complexity" in issue.get("description", "").lower(),
                "description": "Complexity issues",
            },
            {
                "pattern": r"(?:show|find|list|get)\s+(?:me\s+)?(?:all\s+)?test\s+issues",
                "filter": lambda issue: "TEST" in issue.get("rule_id", "").upper()
                or "test" in issue.get("description", "").lower(),
                "description": "Testing issues",
            },
            {
                "pattern": r"how\s+many\s+(?:total\s+)?issues",
                "filter": lambda issue: True,
                "description": "Total issue count",
                "count_only": True,
            },
            {
                "pattern": r"what(?:\'s|\s+is)\s+(?:the\s+)?worst\s+file",
                "filter": lambda issue: True,
                "description": "File with most issues",
                "aggregate": "worst_file",
            },
        ]

    def query(self, natural_language: str, issues: List[dict]) -> Dict:
        """Execute natural language query on issues.

        Args:
            natural_language: Natural language query
            issues: List of issues to query

        Returns:
            Query results with matched issues and metadata
        """
        # Normalize query
        query_lower = natural_language.lower().strip()

        # Find matching pattern
        for pattern_info in self.query_patterns:
            match = re.search(pattern_info["pattern"], query_lower, re.IGNORECASE)
            if match:
                return self._execute_query(pattern_info, issues, match)

        # No pattern matched
        return {
            "success": False,
            "message": 'Could not understand query. Try: "Show me all SQL injection vulnerabilities"',
            "issues": [],
            "count": 0,
        }

    def _execute_query(self, pattern_info: dict, issues: List[dict], match) -> Dict:
        """Execute a matched query pattern.

        Args:
            pattern_info: Pattern information
            issues: List of issues
            match: Regex match object

        Returns:
            Query results
        """
        filter_func = pattern_info["filter"]

        # Extract parameter if needed
        param = None
        if "extract_param" in pattern_info:
            param = pattern_info["extract_param"](match)

        # Filter issues
        if param:
            filtered = [issue for issue in issues if filter_func(issue, param)]
        else:
            filtered = [issue for issue in issues if filter_func(issue)]

        # Handle count-only queries
        if pattern_info.get("count_only"):
            return {
                "success": True,
                "message": f"Found {len(filtered)} total issues",
                "issues": [],
                "count": len(filtered),
            }

        # Handle aggregate queries
        if pattern_info.get("aggregate") == "worst_file":
            file_counts = {}
            for issue in filtered:
                file_path = issue.get("file_path", "unknown")
                file_counts[file_path] = file_counts.get(file_path, 0) + 1

            if file_counts:
                worst_file = max(file_counts.items(), key=lambda x: x[1])
                return {
                    "success": True,
                    "message": f"Worst file: {worst_file[0]} with {worst_file[1]} issues",
                    "issues": [
                        i for i in filtered if i.get("file_path") == worst_file[0]
                    ],
                    "count": worst_file[1],
                    "file_path": worst_file[0],
                }
            else:
                return {
                    "success": True,
                    "message": "No issues found",
                    "issues": [],
                    "count": 0,
                }

        # Regular filtered query
        return {
            "success": True,
            "message": f'Found {len(filtered)} {pattern_info["description"]}',
            "issues": filtered,
            "count": len(filtered),
        }

    def get_suggestions(self) -> List[str]:
        """Get example queries.

        Returns:
            List of example queries
        """
        return [
            "Show me all SQL injection vulnerabilities",
            "Find all XSS issues",
            "List all hardcoded secrets",
            "Show me all critical issues",
            "Get all security vulnerabilities",
            "Find all quality issues",
            "Show me all issues in main.py",
            "List all TODO comments",
            "Find all missing documentation",
            "How many total issues?",
            "What's the worst file?",
        ]
