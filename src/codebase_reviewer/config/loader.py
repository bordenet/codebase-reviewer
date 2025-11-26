"""Configuration loader for Phase 2 thresholds and prompts."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class ThresholdConfig:
    """Individual threshold configuration."""

    value: float
    description: str = ""
    rationale: str = ""


@dataclass
class FallbackConfig:
    """Fallback strategy configuration."""

    cooldown_days: int = 7
    suppress_on_failure: bool = True
    alert_on_chained_failures: bool = True
    chained_failure_count: int = 3


@dataclass
class HeuristicsConfig:
    """Advanced heuristics configuration."""

    checksum_critical_dirs: bool = True
    critical_directories: List[str] = field(default_factory=lambda: ["src/", "lib/", "internal/", "pkg/"])
    semantic_api_changes: bool = True
    api_patterns: List[str] = field(default_factory=lambda: ["*.proto", "**/api/**", "*.graphql"])
    git_analysis: bool = True
    commit_lookback: int = 100
    hotspot_threshold: int = 5


@dataclass
class PromptIntegrationConfig:
    """Configuration for how thresholds are embedded in prompts."""

    embed_thresholds: bool = True
    embed_trigger_reasons: bool = True
    embed_metrics_history: bool = True
    history_lookback_runs: int = 5
    include_recommendations: bool = True
    recommendations: Dict[str, str] = field(default_factory=dict)


@dataclass
class Phase2ThresholdsConfig:
    """Complete Phase 2 thresholds configuration."""

    # Core thresholds
    files_changed_percent: float = 30.0
    new_languages_enabled: bool = True
    coverage_min_percent: float = 85.0
    staleness_max_days: int = 30
    error_rate_max_percent: float = 5.0
    false_positive_spike_multiplier: float = 1.5

    # Fallback strategies
    fallback: FallbackConfig = field(default_factory=FallbackConfig)

    # Advanced heuristics
    heuristics: HeuristicsConfig = field(default_factory=HeuristicsConfig)

    # Prompt integration
    prompt_integration: PromptIntegrationConfig = field(default_factory=PromptIntegrationConfig)

    def get_recommendation(self, trigger_type: str) -> str:
        """Get recommendation template for a trigger type."""
        return self.prompt_integration.recommendations.get(trigger_type, "")


@dataclass
class RoleConfig:
    """Role configuration for prompts."""

    name: str
    description: str


@dataclass
class PromptsConfig:
    """Complete prompts configuration."""

    # Settings
    default_temperature: float = 0.3
    default_max_tokens: int = 16000
    require_complete_response: bool = True
    warn_on_high_cost: bool = True
    high_cost_threshold_usd: float = 1.00

    # Roles
    roles: Dict[str, RoleConfig] = field(default_factory=dict)

    # Templates
    metaprompt_header: str = ""
    phase1_context: str = ""
    regeneration_preamble: str = ""
    regeneration_improvement_focus: str = ""

    # Improvement templates
    generation_1_focus: str = ""
    generation_n_focus: str = ""

    # Defaults
    defaults: Dict[str, Any] = field(default_factory=dict)


class ConfigLoader:
    """Loads and caches configuration files."""

    _instance: Optional["ConfigLoader"] = None
    _thresholds_cache: Optional[Phase2ThresholdsConfig] = None
    _prompts_cache: Optional[PromptsConfig] = None

    def __new__(cls) -> "ConfigLoader":
        """Singleton pattern for config loader."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the config loader."""
        self.config_dir = Path(__file__).parent
        self.thresholds_path = self.config_dir / "phase2_thresholds.yml"
        self.prompts_path = self.config_dir / "prompts.yml"

    def load_thresholds(self, force_reload: bool = False) -> Phase2ThresholdsConfig:
        """Load Phase 2 thresholds configuration."""
        if self._thresholds_cache is not None and not force_reload:
            return self._thresholds_cache

        if not self.thresholds_path.exists():
            self._thresholds_cache = Phase2ThresholdsConfig()
            return self._thresholds_cache

        with open(self.thresholds_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        config = self._parse_thresholds(data)
        self._thresholds_cache = config
        return config

    def _parse_thresholds(self, data: Dict[str, Any]) -> Phase2ThresholdsConfig:
        """Parse thresholds from YAML data."""
        thresholds = data.get("thresholds", {})
        fallback_data = data.get("fallback", {})
        heuristics_data = data.get("heuristics", {})
        prompt_int_data = data.get("prompt_integration", {})

        # Parse fallback config
        fallback = FallbackConfig(
            cooldown_days=fallback_data.get("cooldown", {}).get("days", 7),
            suppress_on_failure=fallback_data.get("suppress_on_failure", True),
            alert_on_chained_failures=fallback_data.get("alert_on_chained_failures", True),
            chained_failure_count=fallback_data.get("chained_failure_count", 3),
        )

        # Parse heuristics config
        checksum_cfg = heuristics_data.get("checksum_critical_dirs", {})
        semantic_cfg = heuristics_data.get("semantic_api_changes", {})
        git_cfg = heuristics_data.get("git_analysis", {})

        heuristics = HeuristicsConfig(
            checksum_critical_dirs=checksum_cfg.get("enabled", True),
            critical_directories=checksum_cfg.get("directories", ["src/", "lib/", "internal/", "pkg/"]),
            semantic_api_changes=semantic_cfg.get("enabled", True),
            api_patterns=semantic_cfg.get("patterns", ["*.proto", "**/api/**", "*.graphql"]),
            git_analysis=git_cfg.get("enabled", True),
            commit_lookback=git_cfg.get("commit_lookback", 100),
            hotspot_threshold=git_cfg.get("hotspot_threshold", 5),
        )

        # Parse prompt integration config
        recommendations = prompt_int_data.get("recommendations", {})
        prompt_integration = PromptIntegrationConfig(
            embed_thresholds=prompt_int_data.get("embed_thresholds", True),
            embed_trigger_reasons=prompt_int_data.get("embed_trigger_reasons", True),
            embed_metrics_history=prompt_int_data.get("embed_metrics_history", True),
            history_lookback_runs=prompt_int_data.get("history_lookback_runs", 5),
            include_recommendations=prompt_int_data.get("include_recommendations", True),
            recommendations=recommendations,
        )

        return Phase2ThresholdsConfig(
            files_changed_percent=thresholds.get("files_changed", {}).get("percent", 30.0),
            new_languages_enabled=thresholds.get("new_languages", {}).get("enabled", True),
            coverage_min_percent=thresholds.get("coverage", {}).get("min_percent", 85.0),
            staleness_max_days=thresholds.get("staleness", {}).get("max_days", 30),
            error_rate_max_percent=thresholds.get("error_rate", {}).get("max_percent", 5.0),
            false_positive_spike_multiplier=thresholds.get("false_positives", {}).get("spike_multiplier", 1.5),
            fallback=fallback,
            heuristics=heuristics,
            prompt_integration=prompt_integration,
        )

    def load_prompts(self, force_reload: bool = False) -> PromptsConfig:
        """Load prompts configuration."""
        if self._prompts_cache is not None and not force_reload:
            return self._prompts_cache

        if not self.prompts_path.exists():
            self._prompts_cache = PromptsConfig()
            return self._prompts_cache

        with open(self.prompts_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        config = self._parse_prompts(data)
        self._prompts_cache = config
        return config

    def _parse_prompts(self, data: Dict[str, Any]) -> PromptsConfig:
        """Parse prompts from YAML data."""
        settings = data.get("settings", {})
        roles_data = data.get("roles", {})
        metaprompt = data.get("metaprompt", {})
        improvements = data.get("improvements", {})
        defaults = data.get("defaults", {})

        # Parse roles
        roles = {}
        for role_key, role_data in roles_data.items():
            roles[role_key] = RoleConfig(
                name=role_data.get("name", role_key),
                description=role_data.get("description", ""),
            )

        return PromptsConfig(
            default_temperature=settings.get("default_temperature", 0.3),
            default_max_tokens=settings.get("default_max_tokens", 16000),
            require_complete_response=settings.get("require_complete_response", True),
            warn_on_high_cost=settings.get("warn_on_high_cost", True),
            high_cost_threshold_usd=settings.get("high_cost_threshold_usd", 1.00),
            roles=roles,
            metaprompt_header=metaprompt.get("header", ""),
            phase1_context=metaprompt.get("phase1_analysis", {}).get("context", ""),
            regeneration_preamble=metaprompt.get("regeneration", {}).get("preamble", ""),
            regeneration_improvement_focus=metaprompt.get("regeneration", {}).get("improvement_focus", ""),
            generation_1_focus=improvements.get("generation_1", {}).get("focus", ""),
            generation_n_focus=improvements.get("generation_n", {}).get("focus", ""),
            defaults=defaults,
        )

    def clear_cache(self) -> None:
        """Clear all cached configurations."""
        self._thresholds_cache = None
        self._prompts_cache = None

    def get_threshold_as_yaml(self) -> str:
        """Get current thresholds as YAML string for embedding in prompts."""
        config = self.load_thresholds()
        threshold_dict = {
            "files_changed_percent": config.files_changed_percent,
            "new_languages_detection": config.new_languages_enabled,
            "coverage_min_percent": config.coverage_min_percent,
            "staleness_max_days": config.staleness_max_days,
            "error_rate_max_percent": config.error_rate_max_percent,
            "false_positive_spike_multiplier": config.false_positive_spike_multiplier,
            "regeneration_cooldown_days": config.fallback.cooldown_days,
        }
        return yaml.dump(threshold_dict, default_flow_style=False)
