from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BodyAction:
    action: str
    value: object | None = None


class BodyActionModule:
    def __init__(self) -> None:
        self.last_action: BodyAction | None = None

    def execute(
        self,
        action: str,
        value: object | None = None,
    ) -> BodyAction:
        action = action.strip()

        if not action:
            raise ValueError("Body action cannot be empty")

        result = BodyAction(
            action=action,
            value=value,
        )

        self.last_action = result
        return result

    def snapshot(self) -> BodyAction | None:
        return self.last_action
