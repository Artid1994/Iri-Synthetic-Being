from __future__ import annotations

import numpy as np

from config.anatomy_settings import (
    HIPPOCAMPUS,
    MOTOR_CORTEX,
    TOTAL_NEURONS,
)
from regions.hippocampus import Hippocampus
from regions.motor_cortex import MotorCortex


class Brain:
    def __init__(self) -> None:
        self.hippocampus = Hippocampus()
        self.motor_cortex = MotorCortex()

    @property
    def neuron_count(self) -> int:
        return TOTAL_NEURONS

    def store_memory(self, memory: str) -> bool:
        memory = memory.strip()

        if not memory:
            return False

        if not self.hippocampus.store_memory(memory):
            return False

        chunk_size = self.hippocampus.population.chunk_size

        current = np.zeros(
            chunk_size,
            dtype=np.float32,
        )

        current[0] = 1.0

        self.hippocampus.population.step_chunk(
            0,
            current,
        )

        return True

    def has_memory(self, memory: str) -> bool:
        return self.hippocampus.has_memory(memory)

    def sync_memory(self, memory) -> int:
        episodic = getattr(
            getattr(memory, "state", None),
            "episodic",
            (),
        )

        synced = 0

        for item in episodic:
            if self.hippocampus.has_memory(item):
                continue

            if self.store_memory(item):
                synced += 1

        return synced

    def stats(self) -> dict:
        return {
            "total_neurons": self.neuron_count,
            "hippocampus": self.hippocampus.population.stats,
            "motor_cortex": self.motor_cortex.population.stats,
        }
