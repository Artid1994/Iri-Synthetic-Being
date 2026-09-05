import unittest

import numpy as np

from brain.brain import Brain
from brain.neural_state import NeuralState
from brain.plasticity import Plasticity
from brain.population import NeuronPopulation
from brain.synapse import Synapse
from config.anatomy_settings import NeuronParameters, RegionParameters


def population(name="test", size=4, threshold=1.0):
    return NeuronPopulation(RegionParameters(name=name, neuron_count=size, chunk_size=size, neuron=NeuronParameters(threshold=threshold)))


def projection(weights=(1.0,), target_threshold=1.0):
    source = population("source")
    target = population("target", threshold=target_threshold)
    return source, target, Synapse(source, 0, target, 0, [0], [0], weights)


class TestNeuralState(unittest.TestCase):
    def test_state_represents_actual_cycle_state(self):
        brain = Brain()
        source, target, synapse = projection(target_threshold=0.1)
        result = brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity())
        state = brain.neural_state

        self.assertIsInstance(state, NeuralState)
        np.testing.assert_array_equal(state.source_spikes, result["source_spikes"])
        np.testing.assert_array_equal(state.target_current, result["target_current"])
        np.testing.assert_array_equal(state.target_spikes, result["target_spikes"])
        np.testing.assert_array_equal(state.source_membrane, source.allocate_chunk(0).membrane)
        np.testing.assert_array_equal(state.target_membrane, target.allocate_chunk(0).membrane)

    def test_state_reflects_source_and_target_activity(self):
        brain = Brain()
        source, target, synapse = projection(target_threshold=0.1)

        brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity())

        self.assertTrue(brain.neural_state.source_spikes[0])
        self.assertTrue(brain.neural_state.target_spikes[0])
        self.assertEqual(brain.neural_state.source_chunk_index, 0)
        self.assertEqual(brain.neural_state.target_chunk_index, 0)

    def test_state_does_not_contain_synapse_weights(self):
        brain = Brain()
        source, target, synapse = projection()
        brain.run_neural_projection_cycle(synapse, np.zeros(4, dtype=np.float32), Plasticity())

        self.assertFalse(hasattr(brain.neural_state, "weights"))
        self.assertFalse(hasattr(brain.neural_state, "synapse"))

    def test_state_snapshot_is_deterministic(self):
        snapshots = []
        for _ in range(2):
            brain = Brain()
            source, target, synapse = projection(target_threshold=0.1)
            brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity())
            snapshots.append(brain.neural_state)

        for field in ("source_membrane", "target_membrane", "source_spikes", "target_current", "target_spikes"):
            np.testing.assert_array_equal(getattr(snapshots[0], field), getattr(snapshots[1], field))

    def test_state_inspection_does_not_mutate_underlying_state(self):
        brain = Brain()
        source, target, synapse = projection()
        brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity())
        before = source.allocate_chunk(0).membrane.copy()

        state = brain.neural_state
        state.source_membrane[0] = 99.0

        np.testing.assert_array_equal(source.allocate_chunk(0).membrane, before)

    def test_projection_cycle_still_works_with_state_present(self):
        brain = Brain()
        source, target, synapse = projection(target_threshold=0.1)

        result = brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity())

        self.assertTrue(result["target_spikes"][0])
        self.assertIs(brain.neural_state, brain.neural_state)

    def test_plasticity_still_updates_synapse_weights(self):
        brain = Brain()
        source, target, synapse = projection(weights=(0.5,), target_threshold=0.1)

        brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity(learning_rate=0.25))

        self.assertEqual(synapse.weights[0], 0.75)

    def test_memory_behavior_is_unchanged(self):
        brain = Brain()
        source, target, synapse = projection()
        self.assertTrue(brain.store_memory("memory"))
        before = (brain.hippocampus.memory_count, brain.hippocampus.has_memory("memory"))

        brain.run_neural_projection_cycle(synapse, np.zeros(4, dtype=np.float32), Plasticity())

        self.assertEqual((brain.hippocampus.memory_count, brain.hippocampus.has_memory("memory")), before)

    def test_state_does_not_allocate_unrequested_chunks(self):
        brain = Brain()
        source = population("source", size=8)
        target = population("target", size=8)
        synapse = Synapse(source, 0, target, 0, [0], [0], [1.0])

        brain.run_neural_projection_cycle(synapse, np.zeros(8, dtype=np.float32), Plasticity())

        self.assertEqual(source.allocated_chunk_indices(), (0,))
        self.assertEqual(target.allocated_chunk_indices(), (0,))

    def test_invalid_state_arrays_fail_deterministically(self):
        with self.assertRaises(ValueError):
            NeuralState(0, 0, np.zeros(2), np.zeros(4), np.zeros(4, dtype=bool), np.zeros(4), np.zeros(4, dtype=bool))


if __name__ == "__main__":
    unittest.main()
