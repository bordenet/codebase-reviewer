"""Trend analysis for tracking metrics over time."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json


@dataclass
class MetricSnapshot:
    """Snapshot of metrics at a point in time."""
    timestamp: datetime
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    total_files: int
    total_lines: int
    security_issues: int
    quality_issues: int
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'total_issues': self.total_issues,
            'critical_issues': self.critical_issues,
            'high_issues': self.high_issues,
            'medium_issues': self.medium_issues,
            'low_issues': self.low_issues,
            'total_files': self.total_files,
            'total_lines': self.total_lines,
            'security_issues': self.security_issues,
            'quality_issues': self.quality_issues,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MetricSnapshot':
        """Create from dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data['timestamp']),
            total_issues=data['total_issues'],
            critical_issues=data['critical_issues'],
            high_issues=data['high_issues'],
            medium_issues=data['medium_issues'],
            low_issues=data['low_issues'],
            total_files=data['total_files'],
            total_lines=data['total_lines'],
            security_issues=data['security_issues'],
            quality_issues=data['quality_issues'],
        )


@dataclass
class Trend:
    """Trend information for a metric."""
    metric_name: str
    current_value: float
    previous_value: float
    change: float
    change_percent: float
    direction: str  # 'improving', 'degrading', 'stable'
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'metric_name': self.metric_name,
            'current_value': self.current_value,
            'previous_value': self.previous_value,
            'change': self.change,
            'change_percent': self.change_percent,
            'direction': self.direction,
        }


class TrendAnalyzer:
    """Analyzes trends in code metrics over time."""
    
    def __init__(self, history_file: Optional[Path] = None):
        """Initialize trend analyzer.
        
        Args:
            history_file: Path to file storing historical metrics
        """
        self.history_file = history_file or Path('.codebase_metrics_history.json')
        self.snapshots: List[MetricSnapshot] = []
        self._load_history()
    
    def _load_history(self) -> None:
        """Load historical metrics from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.snapshots = [MetricSnapshot.from_dict(s) for s in data.get('snapshots', [])]
            except Exception:
                self.snapshots = []
    
    def _save_history(self) -> None:
        """Save historical metrics to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump({
                    'snapshots': [s.to_dict() for s in self.snapshots]
                }, f, indent=2)
        except Exception:
            pass
    
    def record_snapshot(self, snapshot: MetricSnapshot) -> None:
        """Record a new metric snapshot.
        
        Args:
            snapshot: Metric snapshot to record
        """
        self.snapshots.append(snapshot)
        # Keep only last 100 snapshots
        if len(self.snapshots) > 100:
            self.snapshots = self.snapshots[-100:]
        self._save_history()
    
    def get_trends(self) -> List[Trend]:
        """Get trends for all metrics.
        
        Returns:
            List of trends
        """
        if len(self.snapshots) < 2:
            return []
        
        current = self.snapshots[-1]
        previous = self.snapshots[-2]
        
        trends = []
        
        # Total issues trend
        trends.append(self._calculate_trend('total_issues', current.total_issues, previous.total_issues, lower_is_better=True))
        trends.append(self._calculate_trend('critical_issues', current.critical_issues, previous.critical_issues, lower_is_better=True))
        trends.append(self._calculate_trend('security_issues', current.security_issues, previous.security_issues, lower_is_better=True))
        trends.append(self._calculate_trend('quality_issues', current.quality_issues, previous.quality_issues, lower_is_better=True))
        
        return trends
    
    def _calculate_trend(self, name: str, current: float, previous: float, lower_is_better: bool = True) -> Trend:
        """Calculate trend for a metric."""
        change = current - previous
        change_percent = (change / previous * 100) if previous > 0 else 0
        
        # Determine direction
        if abs(change_percent) < 5:
            direction = 'stable'
        elif (change < 0 and lower_is_better) or (change > 0 and not lower_is_better):
            direction = 'improving'
        else:
            direction = 'degrading'
        
        return Trend(
            metric_name=name,
            current_value=current,
            previous_value=previous,
            change=change,
            change_percent=change_percent,
            direction=direction
        )

