from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable

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


class CameraSensorSource(SensorSource):
    """Adapts an optional webcam frame reader to the sensor contract."""

    def __init__(self, read_frame: Callable[[], object]) -> None:
        self.read_frame = read_frame

    def read(self, timestamp: float) -> SensorReading:
        return SensorReading("camera", self.read_frame(), timestamp)


class MicrophoneSensorSource(SensorSource):
    """Adapts an optional microphone audio reader to the sensor contract."""

    def __init__(self, read_audio: Callable[[], object]) -> None:
        self.read_audio = read_audio

    def read(self, timestamp: float) -> SensorReading:
        return SensorReading("microphone", self.read_audio(), timestamp)
