from __future__ import annotations

from config.anatomy_settings import MOTOR_CORTEX
from brain.population import NeuronPopulation


class MotorCortex:
    def __init__(self) -> None:
        self.population = NeuronPopulation(
            MOTOR_CORTEX
        )

    @property
    def neuron_count(self) -> int:
        return self.population.logical_neurons

    def step(self, chunk_index: int, input_current):
        return self.population.step_chunk(
            chunk_index,
            input_current,
        )
