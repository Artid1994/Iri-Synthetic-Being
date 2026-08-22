from __future__ import annotations

from typing import Callable

from ttf_approval_gate import ActionState, ApprovalAction, ApprovalGate


class ExecutionAdapter:
    def __init__(self, gate: ApprovalGate) -> None:
        self.gate = gate

    def execute(
        self,
        action: ApprovalAction,
        executor: Callable[[ApprovalAction], object],
    ):
        if not self.gate.authorize_execution(action):
            return False, "EXECUTION BLOCKED: approval required"

        if not callable(executor):
            return False, "EXECUTION BLOCKED: invalid executor"

        try:
            result = executor(action)
        except Exception as exc:
            action.state = ActionState.FAILED
            return False, f"EXECUTION FAILED: {exc}"

        action.state = ActionState.EXECUTED
        return True, result
