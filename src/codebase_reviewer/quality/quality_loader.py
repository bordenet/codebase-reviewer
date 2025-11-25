"""Loader for quality rules from YAML files."""

import logging
from pathlib import Path
from typing import List

import yaml

from codebase_reviewer.quality.quality_engine import QualityRule, QualitySeverity

logger = logging.getLogger(__name__)


class QualityRulesLoader:
    """Loads quality rules from YAML configuration files."""

    @staticmethod
    def load_from_file(file_path: Path) -> List[QualityRule]:
        """Load quality rules from a YAML file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            rules = []
            for rule_data in data.get("rules", []):
                try:
                    # Convert severity string to enum
                    severity_str = rule_data.get("severity", "medium")
                    severity = QualitySeverity[severity_str.upper()]

                    rule = QualityRule(
                        id=rule_data["id"],
                        name=rule_data["name"],
                        description=rule_data["description"],
                        severity=severity,
                        pattern=rule_data["pattern"],
                        languages=rule_data["languages"],
                        category=rule_data.get("category", "general"),
                        remediation=rule_data.get("remediation", ""),
                        code_example=rule_data.get("code_example", ""),
                        effort_minutes=rule_data.get("effort_minutes", 15),
                    )
                    rules.append(rule)
                except Exception as e:
                    logger.error(
                        f"Failed to load rule {rule_data.get('id', 'unknown')}: {e}"
                    )
                    continue

            logger.info(f"Loaded {len(rules)} quality rules from {file_path}")
            return rules

        except Exception as e:
            logger.error(f"Failed to load rules from {file_path}: {e}")
            return []

    @staticmethod
    def get_builtin_rules() -> List[QualityRule]:
        """Load built-in quality rules."""
        rules_dir = Path(__file__).parent / "rules"
        all_rules = []

        # Load code quality rules
        quality_file = rules_dir / "code_quality.yaml"
        if quality_file.exists():
            all_rules.extend(QualityRulesLoader.load_from_file(quality_file))

        return all_rules
