from __future__ import annotations

from runtime.body_action import BodyAction
from runtime.body_command import BodyCommand
from runtime.body_command_adapter import BodyCommandAdapter
from runtime.virtual_body import VirtualBody


class EmbodimentLoop:
    def __init__(self, virtual_body: VirtualBody) -> None:
        self.virtual_body = virtual_body

    def observe(self):
        return self.virtual_body.world_model.snapshot()

    def observe_sensor(self, reading) -> None:
        if reading is None:
            return

        value = getattr(reading, "value", None)

        if not isinstance(value, tuple):
            return

        if len(value) != 2:
            return

        try:
            position = (float(value[0]), float(value[1]))
        except (TypeError, ValueError):
            return

        self.virtual_body.world_model.update(
            position=position
        )

    def decide(self, cognitive_cycle) -> BodyAction | None:
        if cognitive_cycle is None:
            return None

        decision = getattr(cognitive_cycle, "decision", "")

        if not decision:
            return None

        return self.virtual_body.body_action.execute(decision)

    def apply(self, action: BodyAction | None):
        if action is None:
            return self.observe()

        value = action.value

        if not isinstance(value, tuple):
            return self.observe()

        if len(value) != 2:
            return self.observe()

        self.virtual_body.world_model.update(
            position=(float(value[0]), float(value[1]))
        )

        return self.observe()

    def execute_command(self, command: BodyCommand):
        if command is None:
            return self.observe()

        action = BodyCommandAdapter.to_body_action(command)

        self.virtual_body.body_action.execute(
            action.action,
            action.value,
        )

        return self.apply(action)

    def step(self, cognitive_cycle):
        action = self.decide(cognitive_cycle)
        return self.apply(action)
