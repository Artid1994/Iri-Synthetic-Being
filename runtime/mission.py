"""
Mission State Machine for IRI Autonomous Controller
Implements the minimal mission control architecture for Mission 001.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
from pathlib import Path


class MissionStatus(Enum):
    """Mission execution states."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    BLOCKED = "blocked"
    RESOURCE_LIMIT = "resource_limit"


@dataclass
class KnowledgeGap:
    """Represents insufficient information requiring research."""
    topic: str
    required_for: str
    detected_at: float
    resolution_attempted: bool = False
    hermes_requested: bool = False
    verified: bool = False


@dataclass
class MissionProgress:
    """Tracks objective-level progress."""
    thai_competency: float = 0.0  # 0.0 to 1.0
    english_competency: float = 0.0  # 0.0 to 1.0
    lessons_completed: int = 0
    assessments_passed: int = 0
    last_updated: Optional[float] = None


@dataclass
class ResourceUsage:
    """Tracks resource consumption."""
    hermes_calls: int = 0
    tokens_used: int = 0
    research_count: int = 0
    self_inspection_count: int = 0


@dataclass
class Mission:
    """
    One-prompt autonomous mission state.
    
    Represents the entire mission lifecycle from user prompt to completion.
    """
    mission_id: str
    objective: str  # User's original high-level prompt
    status: MissionStatus
    created_at: float
    updated_at: float
    
    # State tracking
    progress: MissionProgress = field(default_factory=MissionProgress)
    current_task: Optional[str] = None
    active_gap: Optional[KnowledgeGap] = None
    attempt_count: int = 0
    resource_usage: ResourceUsage = field(default_factory=ResourceUsage)
    
    # Completion tracking
    blockers: List[str] = field(default_factory=list)
    completion_evidence: Dict[str, Any] = field(default_factory=dict)
    
    # Budget limits
    max_hermes_calls: int = 100
    max_tokens: int = 500000
    max_attempts_per_task: int = 3
    
    def is_complete(self) -> bool:
        """Check if mission completion criteria are met."""
        return (
            self.progress.thai_competency >= 1.0
            and self.progress.english_competency >= 1.0
        )
    
    def is_blocked(self) -> bool:
        """Check if mission is blocked."""
        return len(self.blockers) > 0 or self.attempt_count >= self.max_attempts_per_task
    
    def is_resource_exhausted(self) -> bool:
        """Check if resource limits are exceeded."""
        return (
            self.resource_usage.hermes_calls >= self.max_hermes_calls
            or self.resource_usage.tokens_used >= self.max_tokens
        )
    
    def update_status(self) -> MissionStatus:
        """Determine and update status based on current state."""
        if self.is_complete():
            self.status = MissionStatus.COMPLETE
        elif self.is_resource_exhausted():
            self.status = MissionStatus.RESOURCE_LIMIT
        elif self.is_blocked():
            self.status = MissionStatus.BLOCKED
        elif self.status == MissionStatus.PENDING:
            self.status = MissionStatus.RUNNING
        
        self.updated_at = datetime.now().timestamp()
        return self.status
    
    def record_hermes_call(self, tokens_used: int) -> None:
        """Record Hermes API usage."""
        self.resource_usage.hermes_calls += 1
        self.resource_usage.tokens_used += tokens_used
        self.updated_at = datetime.now().timestamp()
    
    def record_research(self) -> None:
        """Record research activity."""
        self.resource_usage.research_count += 1
        self.updated_at = datetime.now().timestamp()
    
    def add_blocker(self, reason: str) -> None:
        """Add a blocking issue."""
        if reason not in self.blockers:
            self.blockers.append(reason)
        self.updated_at = datetime.now().timestamp()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "mission_id": self.mission_id,
            "objective": self.objective,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "progress": asdict(self.progress),
            "current_task": self.current_task,
            "active_gap": asdict(self.active_gap) if self.active_gap else None,
            "attempt_count": self.attempt_count,
            "resource_usage": asdict(self.resource_usage),
            "blockers": self.blockers,
            "completion_evidence": self.completion_evidence,
            "max_hermes_calls": self.max_hermes_calls,
            "max_tokens": self.max_tokens,
            "max_attempts_per_task": self.max_attempts_per_task,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Mission:
        """Deserialize from dictionary."""
        progress_data = data.get("progress", {})
        progress = MissionProgress(**progress_data)
        
        gap_data = data.get("active_gap")
        active_gap = KnowledgeGap(**gap_data) if gap_data else None
        
        usage_data = data.get("resource_usage", {})
        resource_usage = ResourceUsage(**usage_data)
        
        return Mission(
            mission_id=data["mission_id"],
            objective=data["objective"],
            status=MissionStatus(data["status"]),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            progress=progress,
            current_task=data.get("current_task"),
            active_gap=active_gap,
            attempt_count=data.get("attempt_count", 0),
            resource_usage=resource_usage,
            blockers=data.get("blockers", []),
            completion_evidence=data.get("completion_evidence", {}),
            max_hermes_calls=data.get("max_hermes_calls", 100),
            max_tokens=data.get("max_tokens", 500000),
            max_attempts_per_task=data.get("max_attempts_per_task", 3),
        )
    
    def save(self, filepath: Path | str) -> None:
        """Persist mission state to disk."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @staticmethod
    def load(filepath: Path | str) -> Mission:
        """Load mission state from disk."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return Mission.from_dict(data)


def create_mission(objective: str, mission_id: Optional[str] = None) -> Mission:
    """
    Create a new mission from a user prompt.
    
    Args:
        objective: User's high-level goal (e.g., "Make IRI a capable Thai + English AI assistant")
        mission_id: Optional custom mission ID
    
    Returns:
        New Mission instance in PENDING state
    """
    import uuid
    
    if mission_id is None:
        mission_id = f"mission_{uuid.uuid4().hex[:8]}"
    
    now = datetime.now().timestamp()
    
    return Mission(
        mission_id=mission_id,
        objective=objective,
        status=MissionStatus.PENDING,
        created_at=now,
        updated_at=now,
    )
