from __future__ import annotations

from runtime.body_command import BodyCommand


class AutonomousGate:
    def __init__(self, enabled: bool = False) -> None:
        self.enabled = bool(enabled)

    def allow(self, command: BodyCommand | None) -> bool:
        if command is None:
            return False

        if not isinstance(command, BodyCommand):
            return False

        if not command.action:
            return False

        return self.enabled

    def snapshot(self) -> bool:
        return self.enabled
