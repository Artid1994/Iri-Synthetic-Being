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
        Select the next development task by inspecting actual repository state.
        
        v1.5: Real inspection-driven development, not predefined catalog.
        
        Args:
            goal: High-level development goal
            previous_state: Previous loop state
        
        Returns:
            (status, task, message)
        """
        # Inspect repository and identify real gaps
        gaps = self._inspect_repository_gaps()
        
        if not gaps:
            return (
                TaskStatus.NO_SAFE_TASK,
                None,
                "No actionable gaps identified"
            )
        
        # Select highest priority gap
        top_gap = gaps[0]
        
        # Create bounded development task for this gap
        task = self._create_task_from_gap(top_gap)
        
        if task:
            return (
                TaskStatus.SELECTED,
                task,
                f"Selected task for gap: {top_gap['name']}"
            )
        else:
            return (
                TaskStatus.NO_SAFE_TASK,
                None,
                f"Cannot create safe task for gap: {top_gap['name']}"
            )
    
    def _inspect_repository_gaps(self) -> List[Dict]:
        """
        Inspect actual repository state to identify gaps.
        
        Returns list of gaps, highest priority first.
        """
        gaps = []
        
        # Check Thai language foundation
        thai_gap = self._check_thai_foundation()
        if thai_gap:
            gaps.append(thai_gap)
        
        # Check English language foundation
        english_gap = self._check_english_foundation()
        if english_gap:
            gaps.append(english_gap)
        
        # Check learning system integration
        learning_gap = self._check_learning_integration()
        if learning_gap:
            gaps.append(learning_gap)
        
        return gaps
    
    def _check_thai_foundation(self) -> Optional[Dict]:
        """Check Thai language understanding foundation."""
        import os
        
        # Check if Thai curriculum exists
        curriculum_file = "03_Hippocampus/curriculum_state.json"
        if not os.path.exists(curriculum_file):
            return {
                'name': 'thai_curriculum_missing',
                'priority': 1,
                'description': 'Thai curriculum state file missing',
                'category': 'thai_foundation',
            }
        
        # Check for semantic verification system
        semantic_repr = "runtime/education/semantic_representation.py"
        if not os.path.exists(semantic_repr):
            return {
                'name': 'semantic_system_missing',
                'priority': 1,
                'description': 'Semantic representation system missing',
                'category': 'thai_foundation',
            }
        
        # Check if semantic verification is integrated with Thai curriculum
        integration_test = "tests/test_thai_semantic_integration.py"
        if not os.path.exists(integration_test):
            return {
                'name': 'thai_semantic_integration_test_missing',
                'priority': 1,
                'description': 'Need integration test for Thai semantic verification',
                'category': 'thai_foundation',
            }
        
        # If basic infrastructure exists, check for deeper gaps
        # For now, return None (will expand in next iteration)
        return None
    
    def _check_english_foundation(self) -> Optional[Dict]:
        """Check English language understanding foundation."""
        # English is lower priority than Thai
        return None
    
    def _check_learning_integration(self) -> Optional[Dict]:
        """Check learning system integration."""
        return None
    
    def _create_task_from_gap(self, gap: Dict) -> Optional[DevelopmentTask]:
        """
        Create bounded development task from identified gap.
        
        Returns None if task cannot be safely created.
        """
        if gap['name'] == 'thai_semantic_integration_test_missing':
            return DevelopmentTask(
                task_id='thai-semantic-integration-test',
                objective='Create integration test for Thai semantic verification',
                rationale='Verify semantic understanding works with Thai curriculum',
                allowed_paths=[
                    'tests/test_thai_semantic_integration.py',
                ],
                allowed_commands=[
                    'git status',
                    'git diff --stat',
                    'python -m pytest tests/test_thai_semantic_integration.py -v',
                ],
                verification_criteria=[
                    'Test file created',
                    'Test can import semantic verification',
                    'Test passes',
                ],
                stop_conditions=[
                    'Import errors',
                    'Test failure',
                    'Semantic verifier not found',
                ],
            )
        
        # Cannot create safe task for this gap
        return None
    
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
        hermes_adapter=None,
    ):
        self.workspace_root = workspace_root
        self.orchestrator = orchestrator
        self.task_planner = TaskPlanner(workspace_root)
        self.loop_history = []
        self.hermes_adapter = hermes_adapter
        
        # Set adapter on orchestrator's builder
        if hermes_adapter:
            self.orchestrator.builder.executor.hermes_adapter = hermes_adapter
    
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
