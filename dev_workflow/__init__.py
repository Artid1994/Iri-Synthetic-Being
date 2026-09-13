"""
IRI Development Multi-Agent Workflow Orchestrator v1.4

Development infrastructure for controlled IRI development.
NOT part of IRI's cognitive architecture.

v1.3: Hermes-native execution with enforced safety policies.
v1 Autonomous Loop: Controlled mode with bounded task selection.
v1.4: Hermes Context Bridge - proper adapter pattern for execute_code.
"""

from .orchestrator import WorkflowOrchestrator
from .state import WorkflowState, WorkflowStatus
from .budget import BudgetGovernor, ContextGovernor
from .compaction import StateCompactor
from .execution import ExecutionEngine
from .hermes_executor import HermesNativeExecutor, ExecutionPlan, ExecutionResult
from .safety import ExecutionPolicy, PathPolicy, CommandPolicy, GitPolicy
from .hermes_adapter import HermesExecutionAdapter, HermesContextStatus, create_hermes_adapter_from_context
from .autonomous_loop import (
    TaskPlanner, AutonomousLoop, DevelopmentTask, 
    AutonomousLoopState, TaskStatus
)

__all__ = [
    'WorkflowOrchestrator',
    'WorkflowState',
    'WorkflowStatus',
    'BudgetGovernor',
    'ContextGovernor',
]
