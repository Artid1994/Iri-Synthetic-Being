"""
Token and context budget governors.
"""

from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ContextStatus(Enum):
    """Context utilization status."""
    SAFE = "safe"
    WARNING = "warning"
    COMPACTION_REQUIRED = "compaction_required"
    HARD_STOP = "hard_stop"


@dataclass
class BudgetReservation:
    """Token budget reservation."""
    estimated_tokens: int
    reserved: bool = False
    actual_tokens: Optional[int] = None
    
    def release_unused(self, actual: int) -> int:
        """Release unused portion of reservation."""
        if not self.reserved:
            return 0
        self.actual_tokens = actual
        unused = max(0, self.estimated_tokens - actual)
        return unused


class BudgetGovernor:
    """
    Enforces hard token budget limits.
    
    Rules:
    - Never allow negative remaining budget
    - Reserve before execution
    - Track actual usage
    - Release unused reservation
    - Reject calls that exceed budget
    """
    
    def __init__(self, total_budget: int):
        self.total_budget = total_budget
        self.used = 0
        self.reserved = 0
        self.history = []
    
    @property
    def remaining(self) -> int:
        """Calculate remaining budget."""
        return self.total_budget - self.used - self.reserved
    
    def can_reserve(self, estimated_tokens: int) -> bool:
        """Check if reservation is possible."""
        return estimated_tokens <= self.remaining
    
    def reserve(self, estimated_tokens: int) -> Tuple[bool, str]:
        """
        Reserve tokens before execution.
        
        Returns:
            (success, message)
        """
        if estimated_tokens <= 0:
            return False, "Invalid token estimate: must be positive"
        
        if not self.can_reserve(estimated_tokens):
            return False, (
                f"Insufficient budget: need {estimated_tokens}, "
                f"remaining {self.remaining}"
            )
        
        self.reserved += estimated_tokens
        reservation = BudgetReservation(estimated_tokens=estimated_tokens, reserved=True)
        self.history.append(('reserve', estimated_tokens, self.remaining))
        return True, f"Reserved {estimated_tokens} tokens"
    
    def commit(self, estimated_tokens: int, actual_tokens: int) -> Tuple[bool, str]:
        """
        Commit actual usage and release unused reservation.
        
        Args:
            estimated_tokens: originally reserved amount
            actual_tokens: actual usage
        
        Returns:
            (success, message)
        """
        if actual_tokens < 0:
            return False, "Invalid actual tokens: must be non-negative"
        
        # Release reservation
        if estimated_tokens > 0:
            self.reserved = max(0, self.reserved - estimated_tokens)
        
        # Add actual usage
        self.used += actual_tokens
        
        # Track
        self.history.append(('commit', actual_tokens, self.remaining))
        
        unused = max(0, estimated_tokens - actual_tokens)
        return True, f"Committed {actual_tokens} tokens, released {unused} unused"
    
    def get_status(self) -> dict:
        """Get current budget status."""
        return {
            'total': self.total_budget,
            'used': self.used,
            'reserved': self.reserved,
            'remaining': self.remaining,
            'utilization': self.used / self.total_budget if self.total_budget > 0 else 0.0,
        }


class ContextGovernor:
    """
    Enforces context window limits.
    
    Thresholds:
    - SAFE: <70%
    - WARNING: 70-80%
    - COMPACTION_REQUIRED: 80-90%
    - HARD_STOP: >90%
    """
    
    def __init__(
        self,
        context_limit: int,
        safe_threshold: float = 0.70,
        warning_threshold: float = 0.80,
        compaction_threshold: float = 0.90,
    ):
        self.context_limit = context_limit
        self.context_used = 0
        self.compaction_count = 0
        
        self.safe_threshold = safe_threshold
        self.warning_threshold = warning_threshold
        self.compaction_threshold = compaction_threshold
        
        self.history = []
    
    @property
    def utilization(self) -> float:
        """Calculate context utilization."""
        if self.context_limit == 0:
            return 0.0
        return self.context_used / self.context_limit
    
    @property
    def remaining(self) -> int:
        """Calculate remaining context."""
        return max(0, self.context_limit - self.context_used)
    
    def get_status(self) -> ContextStatus:
        """Determine current context status."""
        util = self.utilization
        
        if util >= self.compaction_threshold:
            return ContextStatus.HARD_STOP
        elif util >= self.warning_threshold:
            return ContextStatus.COMPACTION_REQUIRED
        elif util >= self.safe_threshold:
            return ContextStatus.WARNING
        else:
            return ContextStatus.SAFE
    
    def can_continue(self, estimated_growth: int) -> Tuple[bool, ContextStatus, str]:
        """
        Check if operation can continue with estimated context growth.
        
        Returns:
            (can_continue, status, message)
        """
        projected = self.context_used + estimated_growth
        projected_util = projected / self.context_limit if self.context_limit > 0 else 0.0
        
        status = self.get_status()
        
        # Check projected utilization
        if projected_util >= self.compaction_threshold:
            return False, ContextStatus.HARD_STOP, (
                f"Projected context {projected}/{self.context_limit} "
                f"({projected_util:.1%}) exceeds hard limit"
            )
        
        if projected_util >= self.warning_threshold:
            return False, ContextStatus.COMPACTION_REQUIRED, (
                f"Projected context {projected}/{self.context_limit} "
                f"({projected_util:.1%}) requires compaction"
            )
        
        return True, status, f"Safe: {projected}/{self.context_limit} ({projected_util:.1%})"
    
    def update(self, new_context_used: int):
        """Update context usage."""
        self.context_used = new_context_used
        self.history.append(('update', new_context_used, self.utilization))
    
    def compact(self):
        """Record a compaction event."""
        self.compaction_count += 1
        self.history.append(('compact', self.compaction_count, self.utilization))
    
    def get_status_dict(self) -> dict:
        """Get current context status as dict."""
        return {
            'limit': self.context_limit,
            'used': self.context_used,
            'remaining': self.remaining,
            'utilization': self.utilization,
            'status': self.get_status().value,
            'compaction_count': self.compaction_count,
        }
