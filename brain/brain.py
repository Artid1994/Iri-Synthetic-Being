from __future__ import annotations

import numpy as np

from config.anatomy_settings import (
    HIPPOCAMPUS,
    MOTOR_CORTEX,
    TOTAL_NEURONS,
)
from regions.hippocampus import Hippocampus
from regions.motor_cortex import MotorCortex
from brain.plasticity import Plasticity
from brain.synapse import Synapse
from brain.neural_state import NeuralState


class Brain:
    def __init__(self) -> None:
        self.hippocampus = Hippocampus()
        self.motor_cortex = MotorCortex()
        self.neural_state: NeuralState | None = None

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

    def run_neural_projection_cycle(
        self,
        synapse: Synapse,
        source_current,
        plasticity: Plasticity,
    ) -> dict[str, np.ndarray]:
        if not isinstance(synapse, Synapse):
            raise TypeError("synapse must be a Synapse")
        if not isinstance(plasticity, Plasticity):
            raise TypeError("plasticity must be a Plasticity")

        source_length = synapse._chunk_length(
            synapse.source,
            synapse.source_chunk_index,
        )
        target_length = synapse._chunk_length(
            synapse.target,
            synapse.target_chunk_index,
        )
        source_current = np.asarray(source_current, dtype=np.float32)
        if source_current.shape != (source_length,):
            raise ValueError("source_current shape must match source population chunk")

        source_spikes = synapse.source.step_chunk(
            synapse.source_chunk_index,
            source_current,
        )
        target_current = synapse.propagate(source_spikes)
        target_spikes = synapse.target.step_chunk(
            synapse.target_chunk_index,
            target_current,
        )
        weights = plasticity.adapt(
            synapse,
            source_spikes,
            target_spikes,
        )

        self.neural_state = NeuralState(
            source_chunk_index=synapse.source_chunk_index,
            target_chunk_index=synapse.target_chunk_index,
            source_membrane=synapse.source.allocate_chunk(
                synapse.source_chunk_index
            ).membrane,
            target_membrane=synapse.target.allocate_chunk(
                synapse.target_chunk_index
            ).membrane,
            source_spikes=source_spikes,
            target_current=target_current,
            target_spikes=target_spikes,
        )

        return {
            "source_spikes": source_spikes,
            "target_current": target_current,
            "target_spikes": target_spikes,
            "weights": weights,
        }

    def neural_state_snapshot(self) -> dict[str, np.ndarray | int] | None:
        """Return an isolated view of the latest neural cycle snapshot."""
        state = self.neural_state
        if state is None:
            return None

        return {
            "source_chunk_index": state.source_chunk_index,
            "target_chunk_index": state.target_chunk_index,
            "source_membrane": state.source_membrane.copy(),
            "target_membrane": state.target_membrane.copy(),
            "source_spikes": state.source_spikes.copy(),
            "target_current": state.target_current.copy(),
            "target_spikes": state.target_spikes.copy(),
        }

    def stats(self) -> dict:
        return {
            "total_neurons": self.neuron_count,
            "hippocampus": self.hippocampus.population.stats,
            "motor_cortex": self.motor_cortex.population.stats,
        }
