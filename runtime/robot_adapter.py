from __future__ import annotations

from runtime.body_command import BodyCommand
from runtime.execution_result import ExecutionResult


class RobotAdapter:
    def __init__(self, hardware=None) -> None:
        self.hardware = hardware

    def execute(self, command: BodyCommand) -> ExecutionResult:
        if not isinstance(command, BodyCommand):
            return ExecutionResult(
                success=False,
                action="",
                value=None,
                error="invalid command",
            )

        if not command.action:
            return ExecutionResult(
                success=False,
                action="",
                value=command.value,
                error="invalid command",
            )

        if self.hardware is None:
            return ExecutionResult(
                success=False,
                action=command.action,
                value=command.value,
                error="hardware unavailable",
            )

        execute = getattr(self.hardware, "execute", None)

        if not callable(execute):
            return ExecutionResult(
                success=False,
                action=command.action,
                value=command.value,
                error="hardware interface unavailable",
            )

        try:
            success = bool(
                execute(
                    command.action,
                    command.value,
                )
            )

            return ExecutionResult(
                success=success,
                action=command.action,
                value=command.value,
                error=None if success else "hardware execution failed",
            )

        except Exception as exc:
            return ExecutionResult(
                success=False,
                action=command.action,
                value=command.value,
                error=str(exc),
            )
