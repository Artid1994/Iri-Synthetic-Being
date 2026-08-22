from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecoveryDecision:
    action: str
    attempt: int
    reason: str


class ErrorRecovery:
    RETRY = "RETRY"
    ESCALATE = "ESCALATE"

    def __init__(
        self,
        max_attempts: int = 5,
    ) -> None:
        self.max_attempts = max_attempts
        self.attempt = 0

    def handle(
        self,
        error: str,
    ) -> RecoveryDecision:

        self.attempt += 1

        if self.attempt > self.max_attempts:
            return RecoveryDecision(
                self.ESCALATE,
                self.attempt,
                error,
            )

        return RecoveryDecision(
            self.RETRY,
            self.attempt,
            error,
        )

    def reset(self) -> None:
        self.attempt = 0
