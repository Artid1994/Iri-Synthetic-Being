from __future__ import annotations

from runtime.body_command import BodyCommand
from runtime.embodiment import EmbodimentLoop


class AutonomousController:
    def __init__(self, embodiment: EmbodimentLoop) -> None:
        self.embodiment = embodiment

    def decide(self, cognitive_cycle) -> BodyCommand | None:
        return self.embodiment.decide_command(cognitive_cycle)

    def allowed(self, command: BodyCommand | None) -> bool:
        return self.embodiment.autonomous_allowed(command)

    def enable(self) -> None:
        self.embodiment.autonomous_gate.enabled = True

    def disable(self) -> None:
        self.embodiment.autonomous_gate.enabled = False

    def enabled(self) -> bool:
        return self.embodiment.autonomous_gate.snapshot()
