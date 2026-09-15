"""
Token Governor - Hard Budget Enforcement for Hermes Integration
Prevents token budget overruns through reserve-commit-release mechanism.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime
import uuid


@dataclass
class TokenRequest:
    """Request for token budget allocation."""
    estimated_tokens: int
    task_id: str
    description: str = ""
    
    def __post_init__(self):
        if self.estimated_tokens <= 0:
            raise ValueError("estimated_tokens must be positive")


@dataclass
class TokenResponse:
    """Response to budget request."""
    approved: bool
    request_id: str
    tokens_reserved: int
    denial_reason: str = ""
    remaining_budget: int = 0


class TokenGovernor:
    """
    Hard token budget enforcer for Hermes integration.
    
    Every Hermes request MUST pass through this governor.
    Denies requests that would exceed budget limits.
    
    Architecture:
        request → estimate → check budget → ALLOW or DENY
        
    If DENY: RESOURCE_LIMIT → stop loop
    """
    
    def __init__(
        self,
        per_request_limit: int = 10000,
        per_task_limit: int = 50000,
        per_mission_limit: int = 500000,
        max_calls: Optional[int] = None,
    ):
        """
        Initialize governor with budget limits.
        
        Args:
            per_request_limit: Max tokens per single request
            per_task_limit: Max tokens per task
            per_mission_limit: Max tokens for entire mission
            max_calls: Optional max number of calls (None = unlimited)
        """
        self.per_request_limit = per_request_limit
        self.per_task_limit = per_task_limit
        self.per_mission_limit = per_mission_limit
        self.max_calls = max_calls
        
        # Usage tracking
        self.total_used = 0
        self.total_reserved = 0
        self.call_count = 0
        self.task_usage: Dict[str, int] = {}
        
        # Reservation tracking
        self._reservations: Dict[str, int] = {}  # request_id -> tokens
        self._reservation_tasks: Dict[str, str] = {}  # request_id -> task_id
        self._committed: set = set()  # request_ids that have been committed
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count from text.
        
        Heuristic: ~4 chars per token + 20% safety margin.
        This is conservative to avoid underestimation.
        """
        char_count = len(text)
        base_estimate = char_count / 4
        safety_margin = base_estimate * 0.2
        return int(base_estimate + safety_margin)
    
    def remaining_budget(self) -> int:
        """Calculate remaining mission budget."""
        return self.per_mission_limit - self.total_used - self.total_reserved
    
    def request_budget(self, request: TokenRequest) -> TokenResponse:
        """
        Request token budget allocation.
        
        Returns:
            TokenResponse with approved=True if allowed, False if denied
        """
        request_id = uuid.uuid4().hex[:16]
        
        # Check per-request limit
        if request.estimated_tokens > self.per_request_limit:
            return TokenResponse(
                approved=False,
                request_id=request_id,
                tokens_reserved=0,
                denial_reason=f"Request exceeds per-request limit ({self.per_request_limit} tokens)",
                remaining_budget=self.remaining_budget()
            )
        
        # Check call limit
        if self.max_calls is not None and self.call_count >= self.max_calls:
            return TokenResponse(
                approved=False,
                request_id=request_id,
                tokens_reserved=0,
                denial_reason=f"Max calls limit reached ({self.max_calls})",
                remaining_budget=self.remaining_budget()
            )
        
        # Check mission budget
        if request.estimated_tokens > self.remaining_budget():
            return TokenResponse(
                approved=False,
                request_id=request_id,
                tokens_reserved=0,
                denial_reason=f"Insufficient mission budget (remaining: {self.remaining_budget()})",
                remaining_budget=self.remaining_budget()
            )
        
        # Check task limit
        task_used = self.task_usage.get(request.task_id, 0)
        if task_used + request.estimated_tokens > self.per_task_limit:
            return TokenResponse(
                approved=False,
                request_id=request_id,
                tokens_reserved=0,
                denial_reason=f"Task would exceed per-task limit ({self.per_task_limit} tokens)",
                remaining_budget=self.remaining_budget()
            )
        
        # APPROVE - reserve budget
        self.total_reserved += request.estimated_tokens
        self._reservations[request_id] = request.estimated_tokens
        self._reservation_tasks[request_id] = request.task_id
        
        return TokenResponse(
            approved=True,
            request_id=request_id,
            tokens_reserved=request.estimated_tokens,
            remaining_budget=self.remaining_budget()
        )
    
    def commit_usage(self, request_id: str, actual_tokens: int) -> None:
        """
        Commit actual token usage after request completes.
        
        Releases reservation and records actual usage.
        
        Args:
            request_id: ID from TokenResponse
            actual_tokens: Actual tokens used
        """
        if request_id not in self._reservations:
            raise ValueError(f"No reservation found for request_id: {request_id}")
        
        if request_id in self._committed:
            raise ValueError(f"Request {request_id} already committed")
        
        # Release reservation
        reserved = self._reservations[request_id]
        self.total_reserved -= reserved
        
        # Record actual usage
        self.total_used += actual_tokens
        self.call_count += 1
        
        # Update task usage
        task_id = self._reservation_tasks[request_id]
        self.task_usage[task_id] = self.task_usage.get(task_id, 0) + actual_tokens
        
        # Mark as committed
        self._committed.add(request_id)
        
        # Clean up
        del self._reservations[request_id]
        del self._reservation_tasks[request_id]
    
    def release_reservation(self, request_id: str) -> None:
        """
        Release reservation without committing usage.
        
        Use when request is cancelled or fails before completion.
        """
        if request_id not in self._reservations:
            return  # Already released or never reserved
        
        reserved = self._reservations[request_id]
        self.total_reserved -= reserved
        
        del self._reservations[request_id]
        del self._reservation_tasks[request_id]
    
    def get_usage_summary(self) -> Dict:
        """Get current usage statistics."""
        return {
            "total_used": self.total_used,
            "total_reserved": self.total_reserved,
            "remaining_budget": self.remaining_budget(),
            "call_count": self.call_count,
            "max_calls": self.max_calls,
            "per_request_limit": self.per_request_limit,
            "per_task_limit": self.per_task_limit,
            "per_mission_limit": self.per_mission_limit,
            "task_usage": dict(self.task_usage),
        }
