#!/usr/bin/env python3
"""
Goal Management & Task Planning Engine for AE01M (Iri)
Autonomous goal decomposition and task execution planning.
"""
import json
import time
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass, asdict
import sys

# Add paths for directives
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex"))

from core_directives import CoreDirectives, DirectiveViolation

# Goal storage location
HIPPOCAMPUS_DIR = PROJECT_ROOT / "03_Hippocampus"
HIPPOCAMPUS_DIR.mkdir(parents=True, exist_ok=True)
GOALS_FILE = HIPPOCAMPUS_DIR / "goals.json"


class GoalPriority(Enum):
    """Goal priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class GoalStatus(Enum):
    """Goal execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class SubtaskType(Enum):
    """Type of subtask action."""
    TERMINAL = "terminal"
    UI_AUTOMATION = "ui_automation"
    FILE_OPERATION = "file_operation"
    WAIT = "wait"
    VERIFICATION = "verification"
    RESEARCH = "research"


@dataclass
class Subtask:
    """Individual subtask within a goal."""
    id: str
    title: str
    type: SubtaskType
    command: Optional[str]  # Terminal command or action description
    estimated_duration: int  # Seconds
    status: GoalStatus
    safety_checks: List[str]  # Required directive checks
    result: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type.value,
            "command": self.command,
            "estimated_duration": self.estimated_duration,
            "status": self.status.value,
            "safety_checks": self.safety_checks,
            "result": self.result
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Subtask':
        """Create from dictionary."""
        return Subtask(
            id=data["id"],
            title=data["title"],
            type=SubtaskType(data["type"]),
            command=data.get("command"),
            estimated_duration=data.get("estimated_duration", 300),
            status=GoalStatus(data["status"]),
            safety_checks=data.get("safety_checks", []),
            result=data.get("result")
        )


@dataclass
class Goal:
    """High-level goal with decomposed subtasks."""
    id: str
    title: str
    description: str
    priority: GoalPriority
    status: GoalStatus
    created_at: float
    updated_at: float
    subtasks: List[Subtask]
    result: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "subtasks": [task.to_dict() for task in self.subtasks],
            "result": self.result
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Goal':
        """Create from dictionary."""
        return Goal(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            priority=GoalPriority(data["priority"]),
            status=GoalStatus(data["status"]),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            subtasks=[Subtask.from_dict(t) for t in data.get("subtasks", [])],
            result=data.get("result")
        )


class GoalEngine:
    """
    Goal management and task planning engine.
    Decomposes high-level goals into executable subtasks with safety validation.
    """
    
    def __init__(self):
        """Initialize goal engine."""
        self.goals: List[Goal] = []
        self.load_goals()
        print(f"[GoalEngine] Initialized with {len(self.goals)} goals")
    
    def load_goals(self):
        """Load goals from persistent storage."""
        if GOALS_FILE.exists():
            try:
                with open(GOALS_FILE, 'r') as f:
                    data = json.load(f)
                    self.goals = [Goal.from_dict(g) for g in data]
                print(f"[GoalEngine] Loaded {len(self.goals)} goals from {GOALS_FILE}")
            except Exception as e:
                print(f"[GoalEngine] Error loading goals: {e}")
                self.goals = []
        else:
            self.goals = []
    
    def save_goals(self):
        """Save goals to persistent storage."""
        try:
            with open(GOALS_FILE, 'w') as f:
                data = [g.to_dict() for g in self.goals]
                json.dump(data, f, indent=2)
            print(f"[GoalEngine] Saved {len(self.goals)} goals to {GOALS_FILE}")
        except Exception as e:
            print(f"[GoalEngine] Error saving goals: {e}")
    
    def add_goal(self, title: str, description: str, priority: GoalPriority = GoalPriority.MEDIUM) -> Goal:
        """
        Register a new goal.
        
        Args:
            title: Goal title
            description: Detailed description
            priority: Priority level (HIGH/MEDIUM/LOW)
        
        Returns:
            Created Goal object
        """
        goal = Goal(
            id=str(uuid.uuid4())[:8],
            title=title,
            description=description,
            priority=priority,
            status=GoalStatus.PENDING,
            created_at=time.time(),
            updated_at=time.time(),
            subtasks=[]
        )
        
        self.goals.append(goal)
        self.save_goals()
        
        print(f"[GoalEngine] Added goal: {title} ({priority.value})")
        return goal
    
    def decompose_goal(self, goal_id: str) -> Optional[Goal]:
        """
        Decompose a goal into actionable subtasks.
        Uses rule-based decomposition for safety and predictability.
        
        Args:
            goal_id: ID of goal to decompose
        
        Returns:
            Updated Goal with subtasks, or None if not found
        """
        goal = self._find_goal(goal_id)
        if not goal:
            print(f"[GoalEngine] Goal {goal_id} not found")
            return None
        
        print(f"[GoalEngine] Decomposing goal: {goal.title}")
        
        # Rule-based decomposition based on goal content
        subtasks = self._create_subtasks_for_goal(goal)
        
        # Validate all subtasks against directives
        validated_subtasks = []
        for subtask in subtasks:
            if self._validate_subtask(subtask):
                validated_subtasks.append(subtask)
            else:
                print(f"[GoalEngine] Subtask blocked by safety directives: {subtask.title}")
        
        goal.subtasks = validated_subtasks
        goal.updated_at = time.time()
        self.save_goals()
        
        print(f"[GoalEngine] Decomposed into {len(validated_subtasks)} subtasks")
        return goal
    
    def _create_subtasks_for_goal(self, goal: Goal) -> List[Subtask]:
        """
        Create subtasks based on goal content.
        Rule-based decomposition for common goal patterns.
        """
        subtasks = []
        title_lower = goal.title.lower()
        desc_lower = goal.description.lower()
        
        # Pattern: System health check
        if any(word in title_lower or word in desc_lower for word in ["health", "status", "check"]):
            subtasks.extend([
                Subtask(
                    id=str(uuid.uuid4())[:8],
                    title="Check system resources",
                    type=SubtaskType.TERMINAL,
                    command="free -h && df -h",
                    estimated_duration=5,
                    status=GoalStatus.PENDING,
                    safety_checks=["DIRECTIVE_1"]
                ),
                Subtask(
                    id=str(uuid.uuid4())[:8],
                    title="Check service status",
                    type=SubtaskType.TERMINAL,
                    command="systemctl --user status iri-voice.service iri-autonomous.service --no-pager",
                    estimated_duration=5,
                    status=GoalStatus.PENDING,
                    safety_checks=["DIRECTIVE_1"]
                ),
                Subtask(
                    id=str(uuid.uuid4())[:8],
                    title="Verify log health",
                    type=SubtaskType.TERMINAL,
                    command="ls -lh ~/Projects/THE_TRANSCENDING_FORM/logs/ | tail -10",
                    estimated_duration=3,
                    status=GoalStatus.PENDING,
                    safety_checks=["DIRECTIVE_1"]
                )
            ])
        
        # Pattern: Clean/cleanup
        if any(word in title_lower or word in desc_lower for word in ["clean", "cleanup", "remove", "delete"]):
            subtasks.extend([
                Subtask(
                    id=str(uuid.uuid4())[:8],
                    title="Identify temporary files",
                    type=SubtaskType.TERMINAL,
                    command="find ~/Projects/THE_TRANSCENDING_FORM -name '*.tmp' -o -name '*~' | head -20",
                    estimated_duration=5,
                    status=GoalStatus.PENDING,
                    safety_checks=["DIRECTIVE_1", "DIRECTIVE_9"]
                ),
                Subtask(
                    id=str(uuid.uuid4())[:8],
                    title="Clean old cache files",
                    type=SubtaskType.FILE_OPERATION,
                    command="Clean files older than 7 days in cache directories",
                    estimated_duration=10,
                    status=GoalStatus.PENDING,
                    safety_checks=["DIRECTIVE_1", "DIRECTIVE_9"]
                ),
                Subtask(
                    id=str(uuid.uuid4())[:8],
                    title="Verify cleanup success",
                    type=SubtaskType.VERIFICATION,
                    command="du -sh ~/Projects/THE_TRANSCENDING_FORM/*/cache/",
                    estimated_duration=3,
                    status=GoalStatus.PENDING,
                    safety_checks=["DIRECTIVE_1"]
                )
            ])
        
        # Pattern: Update/upgrade
        if any(word in title_lower or word in desc_lower for word in ["update", "upgrade", "install"]):
            subtasks.extend([
                Subtask(
                    id=str(uuid.uuid4())[:8],
                    title="Check for updates",
                    type=SubtaskType.TERMINAL,
                    command="cd ~/Projects/THE_TRANSCENDING_FORM && git fetch",
                    estimated_duration=10,
                    status=GoalStatus.PENDING,
                    safety_checks=["DIRECTIVE_1"]
                ),
                Subtask(
                    id=str(uuid.uuid4())[:8],
                    title="Review changes",
                    type=SubtaskType.TERMINAL,
                    command="cd ~/Projects/THE_TRANSCENDING_FORM && git log --oneline -10",
                    estimated_duration=5,
                    status=GoalStatus.PENDING,
                    safety_checks=["DIRECTIVE_1"]
                )
            ])
        
        # Fallback: Generic task
        if not subtasks:
            subtasks.append(
                Subtask(
                    id=str(uuid.uuid4())[:8],
                    title=f"Execute: {goal.title}",
                    type=SubtaskType.TERMINAL,
                    command=f"# Manual execution required: {goal.description}",
                    estimated_duration=60,
                    status=GoalStatus.PENDING,
                    safety_checks=["DIRECTIVE_1", "DIRECTIVE_2"]
                )
            )
        
        return subtasks
    
    def _validate_subtask(self, subtask: Subtask) -> bool:
        """
        Validate subtask against safety directives.
        
        Args:
            subtask: Subtask to validate
        
        Returns:
            True if safe to execute
        """
        if subtask.type == SubtaskType.TERMINAL and subtask.command:
            # Check command safety (DIRECTIVE_1)
            is_safe, violation = CoreDirectives.check_command_safety(subtask.command)
            if not is_safe:
                print(f"[GoalEngine] Command blocked: {violation.reason}")
                return False
            
            # Check for malware patterns (DIRECTIVE_9)
            is_malware, violation = CoreDirectives.check_malware_operation(subtask.command)
            if is_malware:
                print(f"[GoalEngine] Malware pattern detected: {violation.reason}")
                return False
            
            # Check project integrity (DIRECTIVE_9)
            threatens, violation = CoreDirectives.check_project_integrity(subtask.command)
            if threatens:
                print(f"[GoalEngine] Project integrity threat: {violation.reason}")
                return False
        
        return True
    
    def _find_goal(self, goal_id: str) -> Optional[Goal]:
        """Find goal by ID."""
        for goal in self.goals:
            if goal.id == goal_id:
                return goal
        return None
    
    def get_active_goal(self) -> Optional[Goal]:
        """
        Get highest priority pending/in-progress goal for execution.
        
        Returns:
            Next goal to work on, or None if no active goals
        """
        # Priority order: HIGH > MEDIUM > LOW
        priority_order = [GoalPriority.HIGH, GoalPriority.MEDIUM, GoalPriority.LOW]
        
        for priority in priority_order:
            # First check for in-progress goals
            for goal in self.goals:
                if goal.priority == priority and goal.status == GoalStatus.IN_PROGRESS:
                    return goal
            
            # Then check for pending goals
            for goal in self.goals:
                if goal.priority == priority and goal.status == GoalStatus.PENDING:
                    return goal
        
        return None
    
    def get_next_subtask(self, goal: Goal) -> Optional[Subtask]:
        """
        Get next pending subtask for a goal.
        
        Args:
            goal: Goal to get subtask from
        
        Returns:
            Next subtask to execute, or None if all complete
        """
        for subtask in goal.subtasks:
            if subtask.status == GoalStatus.PENDING:
                return subtask
        return None
    
    def update_subtask_status(self, goal_id: str, subtask_id: str, 
                             status: GoalStatus, result: Optional[str] = None):
        """Update subtask status and result."""
        goal = self._find_goal(goal_id)
        if not goal:
            return
        
        for subtask in goal.subtasks:
            if subtask.id == subtask_id:
                subtask.status = status
                subtask.result = result
                break
        
        # Check if all subtasks complete
        if all(t.status == GoalStatus.COMPLETED for t in goal.subtasks):
            goal.status = GoalStatus.COMPLETED
        
        goal.updated_at = time.time()
        self.save_goals()
    
    def list_goals(self, status: Optional[GoalStatus] = None) -> List[Goal]:
        """
        List goals, optionally filtered by status.
        
        Args:
            status: Filter by status (optional)
        
        Returns:
            List of goals
        """
        if status:
            return [g for g in self.goals if g.status == status]
        return self.goals
    
    def get_goal_summary(self, goal: Goal) -> str:
        """Get human-readable goal summary."""
        completed = sum(1 for t in goal.subtasks if t.status == GoalStatus.COMPLETED)
        total = len(goal.subtasks)
        
        return f"""
Goal: {goal.title} [{goal.id}]
Priority: {goal.priority.value.upper()}
Status: {goal.status.value}
Progress: {completed}/{total} subtasks completed
Description: {goal.description}
"""


def test_goal_engine():
    """Test goal engine functionality."""
    print("=" * 60)
    print("Goal Management & Task Planning Engine Test")
    print("=" * 60)
    
    engine = GoalEngine()
    
    # Test 1: Add goal
    print("\n1. Adding test goal...")
    goal = engine.add_goal(
        title="Check system health and clean temporary log cache",
        description="Perform system health check and remove old temporary files to free up disk space",
        priority=GoalPriority.HIGH
    )
    print(f"   ✓ Goal added: {goal.id}")
    
    # Test 2: Decompose goal
    print("\n2. Decomposing goal into subtasks...")
    goal = engine.decompose_goal(goal.id)
    if goal:
        print(f"   ✓ Decomposed into {len(goal.subtasks)} subtasks:")
        for i, task in enumerate(goal.subtasks, 1):
            print(f"     [{i}] {task.title} ({task.type.value})")
            if task.command:
                print(f"         Command: {task.command[:60]}...")
            print(f"         Safety: {', '.join(task.safety_checks)}")
    
    # Test 3: Get active goal
    print("\n3. Getting active goal...")
    active_goal = engine.get_active_goal()
    if active_goal:
        print(f"   ✓ Active goal: {active_goal.title}")
        print(engine.get_goal_summary(active_goal))
    
    # Test 4: Get next subtask
    print("\n4. Getting next subtask for execution...")
    if active_goal:
        next_task = engine.get_next_subtask(active_goal)
        if next_task:
            print(f"   ✓ Next task: {next_task.title}")
            print(f"     Type: {next_task.type.value}")
            print(f"     Est. duration: {next_task.estimated_duration}s")
    
    print("\n" + "=" * 60)
    print("Goal engine test complete")
    print(f"Goals file: {GOALS_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    test_goal_engine()
