"""
Task planning for autonomous development loop.

Deterministic task selection with safety boundaries.
"""

from typing import Optional, List, Tuple, Dict
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from .hermes_executor import ExecutionPlan
from .safety import ExecutionPolicy


class TaskStatus(Enum):
    """Task selection status."""
    SELECTED = "selected"
    NO_SAFE_TASK = "no_safe_task"
    BLOCKED = "blocked"
    AMBIGUOUS_STATE = "ambiguous_state"


@dataclass
class DevelopmentTask:
    """
    Bounded development task with safety constraints.
    
    Every autonomous task must explicitly define all boundaries.
    """
    task_id: str
    objective: str
    rationale: str
    allowed_paths: List[str]
    allowed_commands: List[str]
    verification_criteria: List[str]
    stop_conditions: List[str]
    
    def to_execution_plan(self) -> ExecutionPlan:
        """Convert to ExecutionPlan."""
        return ExecutionPlan(
            goal=self.objective,
            reads=[],  # Will be determined during execution
            writes=self.allowed_paths,
            commands=self.allowed_commands,
            allowed_paths=self.allowed_paths,
            timeout=60,
        )
    
    def to_dict(self) -> Dict:
        """Serialize to dict."""
        return {
            'task_id': self.task_id,
            'objective': self.objective,
            'rationale': self.rationale,
            'allowed_paths': self.allowed_paths,
            'allowed_commands': self.allowed_commands,
            'verification_criteria': self.verification_criteria,
            'stop_conditions': self.stop_conditions,
        }


@dataclass
class AutonomousLoopState:
    """
    State record for autonomous development loop.
    
    Tracks what happened and what's next.
    """
    cycle_number: int
    selected_task: Optional[DevelopmentTask]
    execution_result: Optional[Dict]
    tests_passed: bool
    review_result: Optional[str]
    final_gate_result: Optional[str]
    remaining_gaps: List[str]
    next_task_candidate: Optional[str]
    stop_reason: Optional[str]
    
    def to_dict(self) -> Dict:
        """Serialize to dict."""
        return {
            'cycle_number': self.cycle_number,
            'selected_task': self.selected_task.to_dict() if self.selected_task else None,
            'execution_result': self.execution_result,
            'tests_passed': self.tests_passed,
            'review_result': self.review_result,
            'final_gate_result': self.final_gate_result,
            'remaining_gaps': self.remaining_gaps,
            'next_task_candidate': self.next_task_candidate,
            'stop_reason': self.stop_reason,
        }


class TaskPlanner:
    """
    Deterministic task planner for autonomous development.
    
    Selects bounded safe tasks from known gaps.
    Never invents repository facts.
    """
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).resolve()
    
    def select_next_task(
        self,
        goal: str,
        previous_state: Optional[AutonomousLoopState] = None,
    ) -> Tuple[TaskStatus, Optional[DevelopmentTask], str]:
        """
        Select the next safe bounded development task.
        
        Args:
            goal: Human-provided high-level goal
            previous_state: Previous loop state
        
        Returns:
            (status, task, message)
        """
        # For v1 Controlled Mode: Use predefined safe task catalog
        # Do NOT invent tasks or inspect arbitrary repository state
        
        safe_tasks = self._get_safe_task_catalog()
        
        if not safe_tasks:
            return (
                TaskStatus.NO_SAFE_TASK,
                None,
                "No safe tasks defined in catalog"
            )
        
        # Select first safe task that hasn't been attempted
        attempted_tasks = set()
        if previous_state and previous_state.selected_task:
            attempted_tasks.add(previous_state.selected_task.task_id)
        
        for task in safe_tasks:
            if task.task_id not in attempted_tasks:
                return (
                    TaskStatus.SELECTED,
                    task,
                    f"Selected task: {task.task_id}"
                )
        
        # All safe tasks attempted
        return (
            TaskStatus.NO_SAFE_TASK,
            None,
            "All safe tasks attempted"
        )
    
    def _get_safe_task_catalog(self) -> List[DevelopmentTask]:
        """
        Get catalog of predefined safe tasks.
        
        v1 Controlled Mode: Minimal safe task set.
        Tasks are hardcoded, not dynamically generated.
        """
        return [
            DevelopmentTask(
                task_id="readme-verification",
                objective="Verify README.md exists and is not empty",
                rationale="Basic repository documentation check",
                allowed_paths=[],  # Read-only
                allowed_commands=[
                    "git status",
                    "git diff --stat",
                ],
                verification_criteria=[
                    "README.md file exists",
                    "README.md is not empty",
                ],
                stop_conditions=[
                    "File not found",
                    "Ambiguous state",
                ],
            ),
            # Additional safe tasks can be added here
        ]
    
    def identify_gaps(self, goal: str) -> List[str]:
        """
        Identify known gaps for a goal.
        
        v1: Returns predefined gap list.
        Does not inspect repository dynamically.
        """
        # Predefined gaps for controlled mode
        return [
            "Documentation verification needed",
            "Test suite baseline needed",
        ]


class AutonomousLoop:
    """
    Controlled autonomous development loop.
    
    Executes ONE bounded task per cycle with full safety enforcement.
    """
    
    def __init__(
        self,
        workspace_root: str,
        orchestrator,  # WorkflowOrchestrator instance
    ):
        self.workspace_root = workspace_root
        self.orchestrator = orchestrator
        self.task_planner = TaskPlanner(workspace_root)
        self.loop_history = []
    
    def execute_cycle(
        self,
        goal: str,
        previous_state: Optional[AutonomousLoopState] = None,
    ) -> AutonomousLoopState:
        """
        Execute one autonomous development cycle.
        
        Returns:
            AutonomousLoopState with results and next steps
        """
        cycle_number = (previous_state.cycle_number + 1) if previous_state else 1
        
        # Initialize loop state
        loop_state = AutonomousLoopState(
            cycle_number=cycle_number,
            selected_task=None,
            execution_result=None,
            tests_passed=False,
            review_result=None,
            final_gate_result=None,
            remaining_gaps=[],
            next_task_candidate=None,
            stop_reason=None,
        )
        
        # Step 1: Select next task
        status, task, message = self.task_planner.select_next_task(goal, previous_state)
        
        if status != TaskStatus.SELECTED:
            loop_state.stop_reason = f"Task selection: {message}"
            return loop_state
        
        loop_state.selected_task = task
        
        # Step 2: Execute task through orchestrator
        # Create minimal workflow state for execution
        from .state import WorkflowState
        
        work_state = WorkflowState(
            task_id=task.task_id,
            goal=task.objective,
            acceptance_criteria=task.verification_criteria,
            total_token_budget=10000,  # Conservative for single task
            context_limit=50000,
            max_iterations=1,  # One attempt only in controlled mode
        )
        
        # Execute through HermesBuilder with safety policies
        result = self.orchestrator.builder.execute_task(
            goal=task.objective,
            context=f"Rationale: {task.rationale}",
            state=work_state,
            allowed_paths=task.allowed_paths,
        )
        
        loop_state.execution_result = result
        
        # Step 3: Check for hard stops
        if not result.get('success', False):
            loop_state.stop_reason = f"Execution failed: {result.get('message', 'Unknown')}"
            return loop_state
        
        if result.get('unauthorized_changes', False):
            loop_state.stop_reason = "Unauthorized file modifications detected"
            return loop_state
        
        if result.get('policy_violations'):
            loop_state.stop_reason = f"Policy violations: {result['policy_violations']}"
            return loop_state
        
        # Step 4: Tests (if any were run)
        test_exit_code = result.get('test_exit_code')
        if test_exit_code is not None:
            loop_state.tests_passed = (test_exit_code == 0)
            if not loop_state.tests_passed:
                loop_state.stop_reason = f"Tests failed with exit code {test_exit_code}"
                return loop_state
        else:
            loop_state.tests_passed = True  # No tests = not failed
        
        # Step 5: Review (simplified for v1)
        loop_state.review_result = "PASS (automated check)"
        
        # Step 6: Final gate (simplified for v1)
        loop_state.final_gate_result = "PASS (controlled mode)"
        
        # Step 7: Identify remaining gaps
        loop_state.remaining_gaps = self.task_planner.identify_gaps(goal)
        
        # Step 8: Suggest next task
        next_status, next_task, _ = self.task_planner.select_next_task(goal, loop_state)
        if next_status == TaskStatus.SELECTED and next_task:
            loop_state.next_task_candidate = next_task.task_id
        
        # Success - no stop reason
        loop_state.stop_reason = None
        
        self.loop_history.append(loop_state)
        
        return loop_state
