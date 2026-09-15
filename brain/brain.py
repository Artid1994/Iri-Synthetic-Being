"""
Brain: Computational brain substrate.

Integrates regions and provides neural projection capabilities.
"""
import numpy as np
from regions.hippocampus import Hippocampus
from regions.motor_cortex import MotorCortex
from brain.plasticity import Plasticity
from brain.synapse import Synapse
from brain.neural_state import NeuralState


class Brain:
    """
    Computational brain with hippocampus and motor cortex.

    Provides:
    - Memory storage (hippocampus)
    - Action execution (motor cortex)
    - Neural projection cycles (synapse + plasticity)
    """

    def __init__(self):
        self.hippocampus = Hippocampus()
        self.motor_cortex = MotorCortex()

        # Total neuron count
        self.neuron_count = (
            self.hippocampus.neuron_count +
            self.motor_cortex.neuron_count
        )

        # Neural state from last projection cycle
        self.neural_state: NeuralState = None

    def store_memory(self, content: str) -> bool:
        """
        Store memory in hippocampus.

        Args:
            content: Memory content

        Returns:
            True if new memory, False if duplicate or empty
        """
        return self.hippocampus.store(content)

    def sync_memory(self, memory) -> int:
        """
        Sync episodic memories from Memory to hippocampus.

        Args:
            memory: Memory object with episodic memories

        Returns:
            Number of new memories synced
        """
        synced = 0

        for experience in memory.state.episodic:
            if self.hippocampus.store(experience):
                synced += 1

        return synced

    def has_memory(self, content: str) -> bool:
        """Check if memory exists in hippocampus."""
        return self.hippocampus.has_memory(content)

    def execute_action(self, action_type: str) -> bool:
        """
        Execute action via motor cortex.

        Args:
            action_type: Type of action

        Returns:
            True if executed
        """
        return self.motor_cortex.execute_action(action_type)

    def neural_state_snapshot(self) -> dict | None:
        """
        Export neural state snapshot for bridge.

        Returns:
            Dict with neural state data, or None if no activity
        """
        # Return None if no neural state from projection cycle
        if self.neural_state is None:
            return None

        # Return snapshot with membrane and spike data
        return {
            "source_membrane": self.neural_state.source_membrane.copy(),
            "source_spikes": self.neural_state.source_spikes.copy(),
            "target_membrane": self.neural_state.target_membrane.copy(),
            "target_current": self.neural_state.target_current.copy(),
            "target_spikes": self.neural_state.target_spikes.copy(),
        }

    def stats(self) -> dict:
        """
        Get brain statistics.

        Returns:
            Dictionary with region statistics
        """
        return {
            "neuron_count": self.neuron_count,
            "hippocampus": {
                "memory_count": self.hippocampus.memory_count,
                "allocated_neurons": self.hippocampus.population.stats.allocated_neurons,
            },
            "motor_cortex": {
                "action_count": self.motor_cortex.action_count,
                "allocated_neurons": self.motor_cortex.population.stats.allocated_neurons,
            },
        }

    def run_neural_projection_cycle(
        self,
        synapse: Synapse,
        source_input: np.ndarray,
        plasticity: Plasticity,
    ) -> dict:
        """
        Run one cycle of neural projection with plasticity.

        Args:
            synapse: Connection to propagate
            source_input: Input current to source neurons
            plasticity: Plasticity rule

        Returns:
            Cycle result with spikes and adaptation info
        """
        # Step source population
        source_spikes = synapse.source.step_chunk(
            synapse.source_chunk_index,
            source_input
        )

        # Propagate through synapse
        target_current = synapse.propagate(source_spikes)

        # Step target population
        target_spikes = synapse.target.step_chunk(
            synapse.target_chunk_index,
            target_current
        )

        # Capture neural state snapshot (after propagation, before plasticity)
        source_chunk = synapse.source.allocate_chunk(synapse.source_chunk_index)
        target_chunk = synapse.target.allocate_chunk(synapse.target_chunk_index)

        self.neural_state = NeuralState(
            source_chunk_index=synapse.source_chunk_index,
            target_chunk_index=synapse.target_chunk_index,
            source_membrane=source_chunk.membrane,
            target_membrane=target_chunk.membrane,
            source_spikes=source_spikes,
            target_current=target_current,
            target_spikes=target_spikes,
        )

        # Apply plasticity
        weights_before = synapse.weights.copy()
        weights_after = plasticity.adapt(synapse, source_spikes, target_spikes)

        return {
            "source_spikes": source_spikes,
            "target_spikes": target_spikes,
            "target_current": target_current,
            "weights_before": weights_before,
            "weights_after": weights_after,
            "weights": weights_after,  # Alias for compatibility
            "adapted": not np.array_equal(weights_before, weights_after),
        }
