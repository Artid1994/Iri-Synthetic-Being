"""
Workflow state machine and state tracking.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime
import json


class WorkflowStatus(Enum):
    """Explicit workflow states."""
    IDLE = "idle"
    PLANNING = "planning"
    PROMPT_AUDIT = "prompt_audit"
    CONTEXT_CHECK = "context_check"
    EXECUTING = "executing"
    TESTING = "testing"
    REVIEWING = "reviewing"
    FIX_REQUIRED = "fix_required"
    FINAL_GATE = "final_gate"
    DONE = "done"
    BUDGET_STOP = "budget_stop"
    CONTEXT_STOP = "context_stop"
    ITERATION_STOP = "iteration_stop"
    FAILED = "failed"


class FindingSeverity(Enum):
    """Reviewer finding severity."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


@dataclass
class ReviewerFinding:
    """A single reviewer finding."""
    severity: FindingSeverity
    description: str
    affected_files: List[str] = field(default_factory=list)
    evidence: str = ""


@dataclass
class IterationRecord:
    """Record of a single iteration."""
    iteration: int
    stage: str
    prompt_hash: Optional[str] = None
    estimated_tokens: int = 0
    actual_tokens: int = 0
    context_utilization: float = 0.0
    reviewer_result: Optional[str] = None
    findings: List[ReviewerFinding] = field(default_factory=list)
    git_commit: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class WorkflowState:
    """Complete workflow state for persistence and resume."""
    
    # Task definition
    task_id: str
    goal: str
    acceptance_criteria: List[str]
    
    # Current state
    status: WorkflowStatus = WorkflowStatus.IDLE
    iteration: int = 0
    fix_iteration: int = 0
    
    # Budget tracking
    total_token_budget: int = 0
    tokens_used: int = 0
    tokens_reserved: int = 0
    
    # Context tracking
    context_limit: int = 0
    context_used: int = 0
    context_utilization: float = 0.0
    compaction_count: int = 0
    
    # Limits
    max_iterations: int = 5
    max_fix_iterations: int = 3
    
    # History
    iterations: List[IterationRecord] = field(default_factory=list)
    unresolved_findings: List[ReviewerFinding] = field(default_factory=list)
    
    # Git state
    changed_files: List[str] = field(default_factory=list)
    latest_commit: Optional[str] = None
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def tokens_remaining(self) -> int:
        """Calculate remaining token budget."""
        return self.total_token_budget - self.tokens_used - self.tokens_reserved
    
    @property
    def context_remaining(self) -> int:
        """Calculate remaining context."""
        return self.context_limit - self.context_used
    
    def to_dict(self) -> Dict:
        """Serialize to dict."""
        return {
            'task_id': self.task_id,
            'goal': self.goal,
            'acceptance_criteria': self.acceptance_criteria,
            'status': self.status.value,
            'iteration': self.iteration,
            'fix_iteration': self.fix_iteration,
            'total_token_budget': self.total_token_budget,
            'tokens_used': self.tokens_used,
            'tokens_reserved': self.tokens_reserved,
            'tokens_remaining': self.tokens_remaining,
            'context_limit': self.context_limit,
            'context_used': self.context_used,
            'context_utilization': self.context_utilization,
            'context_remaining': self.context_remaining,
            'compaction_count': self.compaction_count,
            'max_iterations': self.max_iterations,
            'max_fix_iterations': self.max_fix_iterations,
            'iterations': [
                {
                    'iteration': rec.iteration,
                    'stage': rec.stage,
                    'prompt_hash': rec.prompt_hash,
                    'estimated_tokens': rec.estimated_tokens,
                    'actual_tokens': rec.actual_tokens,
                    'context_utilization': rec.context_utilization,
                    'reviewer_result': rec.reviewer_result,
                    'findings': [
                        {
                            'severity': f.severity.value,
                            'description': f.description,
                            'affected_files': f.affected_files,
                            'evidence': f.evidence,
                        }
                        for f in rec.findings
                    ],
                    'git_commit': rec.git_commit,
                    'timestamp': rec.timestamp,
                }
                for rec in self.iterations
            ],
            'unresolved_findings': [
                {
                    'severity': f.severity.value,
                    'description': f.description,
                    'affected_files': f.affected_files,
                    'evidence': f.evidence,
                }
                for f in self.unresolved_findings
            ],
            'changed_files': self.changed_files,
            'latest_commit': self.latest_commit,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
    
    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps(self.to_dict(), indent=2)
    
    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now().isoformat()
