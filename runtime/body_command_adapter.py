from __future__ import annotations

from runtime.body_action import BodyAction
from runtime.body_command import BodyCommand


class BodyCommandAdapter:
    @staticmethod
    def to_body_action(
        command: BodyCommand,
    ) -> BodyAction:
        return BodyAction(
            action=command.action,
            value=command.value,
        )
