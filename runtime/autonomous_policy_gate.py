from __future__ import annotations

from dataclasses import dataclass

from runtime.body_command import BodyCommand


@dataclass(frozen=True)
class AutonomousPolicyDecision:
    allowed: bool
    reason: str


class AutonomousPolicyGate:
    def __init__(self, enabled: bool = False) -> None:
        self.enabled = bool(enabled)

    def evaluate(
        self,
        command: BodyCommand | None,
    ) -> AutonomousPolicyDecision:
        if not self.enabled:
            return AutonomousPolicyDecision(
                False,
                "AUTONOMOUS_MODE_DISABLED",
            )

        if not isinstance(command, BodyCommand):
            return AutonomousPolicyDecision(
                False,
                "INVALID_COMMAND",
            )

        return AutonomousPolicyDecision(
            True,
            "AUTONOMOUS_POLICY_ALLOW",
        )

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False
