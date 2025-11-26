"""Rules loader for loading security rules from YAML files."""

import logging
from pathlib import Path
from typing import List

import yaml

from .rule_engine import SecurityRule, Severity

logger = logging.getLogger(__name__)


class RulesLoader:
    """Loader for security rules from YAML files."""

    @staticmethod
    def load_from_yaml(yaml_path: Path) -> List[SecurityRule]:
        """
        Load security rules from a YAML file.

        Args:
            yaml_path: Path to the YAML file containing rules

        Returns:
            List of SecurityRule objects
        """
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            rules = []
            for rule_data in data.get("rules", []):
                try:
                    rule = RulesLoader._parse_rule(rule_data)
                    rules.append(rule)
                except Exception as e:
                    logger.error(f"Failed to parse rule {rule_data.get('id', 'unknown')}: {e}")

            logger.info(f"Loaded {len(rules)} rules from {yaml_path}")
            return rules

        except Exception as e:
            logger.error(f"Failed to load rules from {yaml_path}: {e}")
            return []

    @staticmethod
    def load_from_directory(directory: Path) -> List[SecurityRule]:
        """
        Load all security rules from YAML files in a directory.

        Args:
            directory: Path to directory containing YAML rule files

        Returns:
            List of SecurityRule objects
        """
        all_rules: List[SecurityRule] = []

        if not directory.exists():
            logger.warning(f"Rules directory does not exist: {directory}")
            return all_rules

        for yaml_file in directory.glob("*.yaml"):
            rules = RulesLoader.load_from_yaml(yaml_file)
            all_rules.extend(rules)

        for yaml_file in directory.glob("*.yml"):
            rules = RulesLoader.load_from_yaml(yaml_file)
            all_rules.extend(rules)

        logger.info(f"Loaded {len(all_rules)} total rules from {directory}")
        return all_rules

    @staticmethod
    def _parse_rule(rule_data: dict) -> SecurityRule:
        """
        Parse a single rule from dictionary data.

        Args:
            rule_data: Dictionary containing rule data

        Returns:
            SecurityRule object
        """
        # Parse severity
        severity_str = rule_data.get("severity", "medium").lower()
        severity = Severity[severity_str.upper()]

        # Create rule
        rule = SecurityRule(
            id=rule_data["id"],
            name=rule_data["name"],
            description=rule_data["description"],
            severity=severity,
            pattern=rule_data["pattern"],
            languages=rule_data.get("languages", []),
            owasp_category=rule_data.get("owasp_category", "Unknown"),
            cwe_id=rule_data.get("cwe_id"),
            remediation=rule_data.get("remediation", ""),
            code_example=rule_data.get("code_example", ""),
            effort_minutes=rule_data.get("effort_minutes", 30),
        )

        return rule

    @staticmethod
    def get_builtin_rules() -> List[SecurityRule]:
        """
        Get built-in security rules.

        Returns:
            List of built-in SecurityRule objects
        """
        # Load from the built-in rules directory
        builtin_dir = Path(__file__).parent / "rules"
        if builtin_dir.exists():
            return RulesLoader.load_from_directory(builtin_dir)

        # Fallback to hardcoded rules if directory doesn't exist
        logger.warning("Built-in rules directory not found, using hardcoded rules")
        return RulesLoader._get_hardcoded_rules()

    @staticmethod
    def _get_hardcoded_rules() -> List[SecurityRule]:
        """
        Get hardcoded security rules as fallback.

        Returns:
            List of hardcoded SecurityRule objects
        """
        # This will be populated with actual rules
        # For now, return empty list - rules will be in YAML files
        return []
