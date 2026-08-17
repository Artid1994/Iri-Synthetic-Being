from __future__ import annotations

from runtime.body_action import BodyActionModule
from runtime.environment import Environment
from runtime.sensor import Sensor
from runtime.world_model import WorldModel


class VirtualBody:
    def __init__(self) -> None:
        self.sensor = Sensor("position")
        self.world_model = WorldModel()
        self.body_action = BodyActionModule()
        self.environment = Environment()

    def snapshot(self) -> dict:
        return {
            "sensor": self.sensor.snapshot(),
            "world_model": self.world_model.snapshot(),
            "body_action": self.body_action.snapshot(),
            "environment": self.environment.snapshot(),
        }
