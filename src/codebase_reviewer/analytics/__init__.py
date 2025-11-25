"""Analytics module for trend analysis and predictive analytics."""

from .hotspot_detector import HotspotDetector
from .risk_scorer import RiskScorer
from .trend_analyzer import TrendAnalyzer

__all__ = ["TrendAnalyzer", "HotspotDetector", "RiskScorer"]
