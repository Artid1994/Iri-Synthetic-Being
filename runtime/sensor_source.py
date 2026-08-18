from __future__ import annotations

from abc import ABC, abstractmethod

from runtime.sensor import SensorReading


class SensorSource(ABC):
    @abstractmethod
    def read(self, timestamp: float) -> SensorReading:
        raise NotImplementedError


class MockSensor(SensorSource):
    def __init__(self, name: str, value: object) -> None:
        self.name = name
        self.value = value

    def read(self, timestamp: float) -> SensorReading:
        return SensorReading(
            sensor=self.name,
            value=self.value,
            timestamp=timestamp,
        )
