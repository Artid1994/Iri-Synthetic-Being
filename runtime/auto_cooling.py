from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CoolingDecision:
    action: str
    delay: float


class AutoCoolingController:
    NORMAL = "NORMAL"
    COOLING = "COOLING"
    PAUSE = "PAUSE"

    def __init__(
        self,
        cooling_delay: float = 1.0,
        pause_delay: float = 5.0,
    ) -> None:
        self.cooling_delay = cooling_delay
        self.pause_delay = pause_delay

    def handle(self, level: str) -> CoolingDecision:

        if level == "CRITICAL":
            return CoolingDecision(
                self.PAUSE,
                self.pause_delay,
            )

        if level == "COOLING":
            return CoolingDecision(
                self.COOLING,
                self.cooling_delay,
            )

        return CoolingDecision(
            self.NORMAL,
            0.0,
        )
