from __future__ import annotations

from runtime.body_command import BodyCommand


class ActionMapper:
    @staticmethod
    def map_decision(
        decision: str,
    ) -> BodyCommand | None:
        if not decision:
            return None

        if decision == "MOVE":
            return BodyCommand(
                action="move",
                value=(1.0, 0.0),
            )

        return None
