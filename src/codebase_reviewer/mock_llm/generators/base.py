"""Base class and utilities for response generators."""

from typing import Any, List


class BaseGenerator:
    """Base class for all response generators."""

    def _format_claims(self, claims: List[str]) -> str:
        """Format a list of claims as markdown."""
        if not claims:
            return "- No specific claims found"
        return "\n".join(f"- {claim}" for claim in claims)

    def _format_list(self, items: List) -> str:
        """Format a list of items as markdown list."""
        if not items:
            return "- None"
        return "\n".join(f"- {item}" for item in items[:10])

    def _extract_technologies(self, content: str) -> str:
        """Extract technology mentions from content."""
        techs = []
        tech_keywords = {
            "Python": "Python",
            "JavaScript": "JavaScript",
            "TypeScript": "TypeScript",
            "React": "React",
            "Flask": "Flask",
            "Django": "Django",
            "FastAPI": "FastAPI",
            "PostgreSQL": "PostgreSQL",
            "MySQL": "MySQL",
            "Redis": "Redis",
            "Docker": "Docker",
            "Kubernetes": "Kubernetes",
            "Go": "Go",
            "Rust": "Rust",
            "Java": "Java",
        }

        for keyword, tech_name in tech_keywords.items():
            if keyword in content:
                techs.append(tech_name)

        return ", ".join(techs) if techs else "Not explicitly stated"

    def _extract_components(self, content: str) -> str:
        """Extract component mentions from content."""
        components = []
        if "API" in content or "api" in content:
            components.append("API layer")
        if "database" in content.lower() or "db" in content.lower():
            components.append("Database layer")
        if "frontend" in content.lower() or "UI" in content or "web" in content.lower():
            components.append("Frontend/UI")
        if "backend" in content.lower() or "server" in content.lower():
            components.append("Backend/Server")

        return ", ".join(components) if components else "Not explicitly stated"

    def _extract_setup_claims(self, content: str) -> str:
        """Extract setup instruction claims from content."""
        claims = []
        if "install" in content.lower():
            claims.append("- Installation instructions provided")
        if "pip install" in content.lower() or "npm install" in content.lower():
            claims.append("- Package installation commands included")
        if "python" in content.lower() and "run" in content.lower():
            claims.append("- Runtime instructions included")
        if "docker" in content.lower():
            claims.append("- Docker setup mentioned")

        return "\n".join(claims) if claims else "- No explicit setup instructions found"

    def _extract_feature_claims(self, content: str) -> str:
        """Extract feature claims from content."""
        claims = []
        if "test" in content.lower():
            claims.append("- Testing capabilities mentioned")
        if "deploy" in content.lower():
            claims.append("- Deployment process mentioned")
        if "monitor" in content.lower() or "observability" in content.lower():
            claims.append("- Monitoring/observability mentioned")
        if "security" in content.lower():
            claims.append("- Security features mentioned")

        return "\n".join(claims) if claims else "- No explicit feature claims found"

    def _format_context(self, context: Any) -> str:
        """Format context data for display."""
        if isinstance(context, dict):
            items = []
            for key, value in context.items():
                if isinstance(value, (list, dict)):
                    items.append(f"- **{key}**: {len(value)} items")
                else:
                    items.append(f"- **{key}**: {value}")
            return "\n".join(items)
        return str(context)

    def _format_top_issues(self, issues: List) -> str:
        """Format top issues list."""
        if not issues:
            return "- No issues found"

        formatted = []
        for i, issue in enumerate(issues[:10], 1):
            if isinstance(issue, dict):
                severity = issue.get("severity", "UNKNOWN")
                description = issue.get("description", "No description")
                file_path = issue.get("file", "Unknown file")
                formatted.append(f"{i}. **[{severity}]** {description} ({file_path})")
            else:
                formatted.append(f"{i}. {issue}")

        return "\n".join(formatted)

    def _generate_priority_matrix(self, issues: List) -> str:
        """Generate priority matrix for top issues."""
        if not issues:
            return "| No issues | - | - | - | - |"

        rows = []
        for issue in issues[:5]:
            if isinstance(issue, dict):
                name = issue.get("description", "Unknown")[:40]
                severity = issue.get("severity", "MEDIUM")
                impact = "High" if severity in ["HIGH", "CRITICAL"] else "Medium"
                effort = "Low" if "TODO" in name or "comment" in name.lower() else "Medium"
                priority = "P0" if severity == "CRITICAL" else "P1" if severity == "HIGH" else "P2"
                timeline = "This sprint" if priority == "P0" else "Next sprint" if priority == "P1" else "Backlog"
                rows.append(f"| {name} | {impact} | {effort} | {priority} | {timeline} |")

        return "\n".join(rows) if rows else "| No issues | - | - | - | - |"

    def _identify_quick_wins(self, issues: List) -> str:
        """Identify quick win improvements."""
        if not issues:
            return "- No quick wins identified"

        quick_wins = []
        for issue in issues:
            if isinstance(issue, dict):
                desc = issue.get("description", "")
                # Quick wins: TODO comments, simple fixes, low-hanging fruit
                if any(keyword in desc.lower() for keyword in ["todo", "fixme", "comment", "print"]):
                    quick_wins.append(f"- {desc} (Estimated: 1-2 hours)")

        if not quick_wins:
            return "- Review codebase for TODO/FIXME comments\n- Replace print() with logging\n- Add missing docstrings"

        return "\n".join(quick_wins[:5])

    def _identify_major_refactoring(self, issues: List) -> str:
        """Identify major refactoring projects."""
        if not issues:
            return "- No major refactoring needed"

        major_projects = []
        for issue in issues:
            if isinstance(issue, dict):
                desc = issue.get("description", "")
                severity = issue.get("severity", "")
                # Major refactoring: security issues, architecture problems
                if severity in ["HIGH", "CRITICAL"] and not any(
                    keyword in desc.lower() for keyword in ["todo", "comment"]
                ):
                    major_projects.append(f"- {desc} (Estimated: 1-2 weeks)")

        if not major_projects:
            return "- Improve test coverage to 80%+\n- Reduce cyclomatic complexity\n- Break up large modules"

        return "\n".join(major_projects[:5])

    def _generate_setup_recommendations(self, prereqs, setup_files, build_steps, env_vars, undocumented):
        """Generate setup recommendations based on findings."""
        recommendations = []
        if not prereqs:
            recommendations.append("1. ❌ **CRITICAL**: Document prerequisites in README")
        if not setup_files:
            recommendations.append("2. ❌ **CRITICAL**: Add setup.py or requirements.txt")
        if not build_steps:
            recommendations.append("3. ⚠️ **HIGH**: Document build/installation steps")
        if not env_vars:
            recommendations.append("4. ⚠️ **MEDIUM**: Document environment variables")
        if undocumented:
            recommendations.append(f"5. ⚠️ **MEDIUM**: Document {len(undocumented)} undocumented features")

        if not recommendations:
            return "✅ All setup documentation is complete"
        return "\n".join(recommendations)

    def _calculate_setup_score(self, prereqs, setup_files, build_steps):
        """Calculate setup documentation score."""
        score = 0
        if prereqs:
            score += 40
        if setup_files:
            score += 40
        if build_steps:
            score += 20
        return score
