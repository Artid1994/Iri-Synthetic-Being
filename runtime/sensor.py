from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SensorReading:
    sensor: str
    value: object
    timestamp: float


class Sensor:
    def __init__(self, name: str) -> None:
        name = name.strip()

        if not name:
            raise ValueError("Sensor name cannot be empty")

        self.name = name
        self.last_reading: SensorReading | None = None

    def read(self, value: object, timestamp: float) -> SensorReading:
        reading = SensorReading(
            sensor=self.name,
            value=value,
            timestamp=timestamp,
        )

        self.last_reading = reading
        return reading

    def snapshot(self) -> SensorReading | None:
        return self.last_reading
