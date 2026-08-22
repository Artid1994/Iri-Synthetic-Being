from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ActionState(Enum):
    PROPOSED = "PROPOSED"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"


@dataclass
class ApprovalAction:
    action_type: str
    path: str
    state: ActionState = ActionState.PROPOSED
    human_approval: bool = False


class ApprovalGate:
    """
    v0.2 — Human Approval Gate

    Gate นี้จัดการเฉพาะ Lifecycle
    ยังไม่มี Automatic Execution
    """

    TRANSITIONS = {
        ActionState.PROPOSED: {
            ActionState.VALIDATED,
        },
        ActionState.VALIDATED: {
            ActionState.APPROVED,
            ActionState.REJECTED,
        },
        ActionState.APPROVED: {
            ActionState.EXECUTED,
        },
        ActionState.REJECTED: set(),
        ActionState.EXECUTED: set(),
        ActionState.FAILED: set(),
    }

    def validate(self, action: ApprovalAction) -> bool:
        if action.state != ActionState.PROPOSED:
            return False

        action.state = ActionState.VALIDATED
        return True

    def approve(self, action: ApprovalAction) -> bool:
        if action.state != ActionState.VALIDATED:
            return False

        action.human_approval = True
        action.state = ActionState.APPROVED
        return True

    def reject(self, action: ApprovalAction) -> bool:
        if action.state != ActionState.VALIDATED:
            return False

        action.human_approval = False
        action.state = ActionState.REJECTED
        return True

    def authorize_execution(
        self,
        action: ApprovalAction,
    ) -> bool:
        return (
            action.state == ActionState.APPROVED
            and action.human_approval
        )

    def transition(
        self,
        action: ApprovalAction,
        target: ActionState,
    ) -> bool:
        allowed = self.TRANSITIONS.get(
            action.state,
            set(),
        )

        if target not in allowed:
            return False

        action.state = target
        return True
