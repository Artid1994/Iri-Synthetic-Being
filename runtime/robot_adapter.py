from __future__ import annotations

from runtime.body_command import BodyCommand


class RobotAdapter:
    def __init__(self, hardware=None) -> None:
        self.hardware = hardware

    def execute(self, command: BodyCommand) -> bool:
        if not isinstance(command, BodyCommand):
            return False

        if not command.action:
            return False

        if self.hardware is None:
            return False

        execute = getattr(self.hardware, "execute", None)

        if not callable(execute):
            return False

        try:
            return bool(
                execute(
                    command.action,
                    command.value,
                )
            )
        except Exception:
            return False
