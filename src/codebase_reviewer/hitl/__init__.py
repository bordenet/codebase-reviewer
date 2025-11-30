"""Human-in-the-Loop (HITL) workflow support.

This module provides:
1. Approval gates for tool regeneration
2. Rollback support to previous versions
3. Version management and tracking
4. Change visualization and comparison
"""

from .approval import ApprovalGate, ApprovalRequest, ApprovalResult
from .rollback import RollbackManager, VersionInfo
from .version_manager import ToolVersionManager, VersionMetadata

__all__ = [
    "ApprovalGate",
    "ApprovalRequest",
    "ApprovalResult",
    "RollbackManager",
    "VersionInfo",
    "ToolVersionManager",
    "VersionMetadata",
]
