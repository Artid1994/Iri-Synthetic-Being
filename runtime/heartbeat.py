from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HeartbeatState:
    cycle_count: int = 0
    blocked_count: int = 0
    memory_level: str = "UNKNOWN"
    status: str = "IDLE"


class Heartbeat:
    def __init__(self) -> None:
        self.state = HeartbeatState()

    def record_cycle(
        self,
        memory_level: str,
        status: str,
    ) -> None:
        self.state.cycle_count += 1
        self.state.memory_level = memory_level
        self.state.status = status

    def record_block(self) -> None:
        self.state.blocked_count += 1

    def snapshot(self) -> dict:
        return {
            "cycle_count": self.state.cycle_count,
            "blocked_count": self.state.blocked_count,
            "memory_level": self.state.memory_level,
            "status": self.state.status,
        }
