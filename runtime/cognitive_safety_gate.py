from __future__ import annotations

import math
from dataclasses import dataclass

from runtime.body_command import BodyCommand


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str


class CognitiveSafetyGate:
    """
    Safety boundary ระหว่าง cognitive decision กับการกระทำจริง

    กฎในขั้นแรกต้องเป็น deterministic และไม่สามารถถูก Learning
    แก้ไขได้โดยตรง
    """

    _ALLOWED_ACTIONS = frozenset({
        "move",
        "respond",
    })

    def evaluate(
        self,
        command: BodyCommand | None,
    ) -> SafetyDecision:
        if command is None:
            return SafetyDecision(
                allowed=False,
                reason="missing_command",
            )

        if not isinstance(command, BodyCommand):
            return SafetyDecision(
                allowed=False,
                reason="invalid_command_type",
            )

        if not command.action:
            return SafetyDecision(
                allowed=False,
                reason="empty_action",
            )

        if command.action not in self._ALLOWED_ACTIONS:
            return SafetyDecision(
                allowed=False,
                reason="action_not_allowed",
            )

        if command.action == "move":
            return self._evaluate_move(command)

        if command.action == "respond":
            if command.value is not None:
                return SafetyDecision(
                    allowed=False,
                    reason="invalid_respond_value",
                )

            return SafetyDecision(
                allowed=True,
                reason="safe",
            )

        return SafetyDecision(
            allowed=False,
            reason="unhandled_action",
        )

    def _evaluate_move(
        self,
        command: BodyCommand,
    ) -> SafetyDecision:
        value = command.value

        if not isinstance(value, tuple):
            return SafetyDecision(
                allowed=False,
                reason="invalid_move_value",
            )

        if len(value) != 2:
            return SafetyDecision(
                allowed=False,
                reason="invalid_move_dimensions",
            )

        try:
            x = float(value[0])
            y = float(value[1])
        except (TypeError, ValueError):
            return SafetyDecision(
                allowed=False,
                reason="non_numeric_move_value",
            )

        if not math.isfinite(x) or not math.isfinite(y):
            return SafetyDecision(
                allowed=False,
                reason="non_finite_move_value",
            )

        if abs(x) > 1.0 or abs(y) > 1.0:
            return SafetyDecision(
                allowed=False,
                reason="move_limit_exceeded",
            )

        return SafetyDecision(
            allowed=True,
            reason="safe",
        )
