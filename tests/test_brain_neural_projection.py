import unittest

import numpy as np

from brain.brain import Brain
from brain.plasticity import Plasticity
from brain.population import NeuronPopulation
from brain.synapse import Synapse
from config.anatomy_settings import NeuronParameters, RegionParameters


def population(name="test", size=4, threshold=1.0, chunk_size=None):
    return NeuronPopulation(RegionParameters(name=name, neuron_count=size, chunk_size=chunk_size or size, neuron=NeuronParameters(threshold=threshold)))


def projection(weights=(0.5, 0.25), target_threshold=1.0):
    source = population("source")
    target = population("target", threshold=target_threshold)
    return source, target, Synapse(source, 0, target, 0, [0, 1], [0, 1], weights)


class TestBrainNeuralProjection(unittest.TestCase):
    def test_one_cycle_returns_expected_activity_and_weights(self):
        brain = Brain()
        source, target, synapse = projection()
        result = brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity(learning_rate=0.1))
        np.testing.assert_array_equal(result["source_spikes"], [True, False, False, False])
        np.testing.assert_array_equal(result["target_current"], np.array([0.5, 0, 0, 0], dtype=np.float32))
        np.testing.assert_array_equal(result["target_spikes"], [False, False, False, False])
        np.testing.assert_array_equal(result["weights"], np.array([0.5, 0.25], dtype=np.float32))

    def test_target_spikes_are_generated_after_propagation_and_adapt(self):
        brain = Brain()
        source, target, synapse = projection(weights=(1.0, 0.0))
        result = brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity(learning_rate=0.1))
        self.assertTrue(result["source_spikes"][0])
        self.assertEqual(result["target_current"][0], 1.0)
        self.assertTrue(result["target_spikes"][0])
        self.assertEqual(result["weights"][0], 1.0)

    def test_plasticity_updates_only_coactive_mapped_weights(self):
        brain = Brain()
        source, target, synapse = projection(weights=(0.2, 0.3), target_threshold=0.1)
        result = brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity(learning_rate=0.1))
        np.testing.assert_allclose(result["weights"], np.array([0.3, 0.3], dtype=np.float32))

    def test_updated_weights_affect_subsequent_cycle(self):
        brain = Brain()
        source, target, synapse = projection(weights=(0.5, 0.0), target_threshold=0.1)
        rule = Plasticity(learning_rate=0.25)
        current = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        brain.run_neural_projection_cycle(synapse, current, rule)
        result = brain.run_neural_projection_cycle(synapse, current, rule)
        self.assertEqual(result["target_current"][0], 0.75)
        self.assertEqual(result["weights"][0], 1.0)

    def test_synapse_endpoints_and_mappings_remain_unchanged(self):
        brain = Brain()
        source, target, synapse = projection()
        before = (synapse.source, synapse.target, synapse.source_indices.copy(), synapse.target_indices.copy())
        brain.run_neural_projection_cycle(synapse, np.zeros(4, dtype=np.float32), Plasticity())
        self.assertIs(synapse.source, before[0])
        self.assertIs(synapse.target, before[1])
        np.testing.assert_array_equal(synapse.source_indices, before[2])
        np.testing.assert_array_equal(synapse.target_indices, before[3])

    def test_memory_behavior_remains_unchanged(self):
        brain = Brain()
        source, target, synapse = projection()
        brain.store_memory("existing memory")
        before = (brain.hippocampus.memory_count, brain.hippocampus.has_memory("existing memory"))
        brain.run_neural_projection_cycle(synapse, np.zeros(4, dtype=np.float32), Plasticity())
        self.assertEqual((brain.hippocampus.memory_count, brain.hippocampus.has_memory("existing memory")), before)

    def test_only_requested_chunks_are_allocated(self):
        brain = Brain()
        source = population("source", size=8, chunk_size=4)
        target = population("target", size=8, chunk_size=4)
        synapse = Synapse(source, 1, target, 1, [0], [0], [1.0])
        brain.run_neural_projection_cycle(synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity())
        self.assertEqual(source.allocated_chunk_indices(), (1,))
        self.assertEqual(target.allocated_chunk_indices(), (1,))

    def test_no_spike_cycle_leaves_weights_unchanged(self):
        brain = Brain()
        source, target, synapse = projection(weights=(0.2, 0.3))
        result = brain.run_neural_projection_cycle(synapse, np.zeros(4, dtype=np.float32), Plasticity(learning_rate=0.1))
        np.testing.assert_array_equal(result["source_spikes"], np.zeros(4, dtype=bool))
        np.testing.assert_array_equal(result["target_spikes"], np.zeros(4, dtype=bool))
        np.testing.assert_array_equal(result["weights"], np.array([0.2, 0.3], dtype=np.float32))

    def test_identical_initial_state_and_input_are_deterministic(self):
        current = np.array([1.0, 1.0, 0.0, 0.0], dtype=np.float32)
        results = []
        for _ in range(2):
            brain = Brain()
            source, target, synapse = projection(weights=(0.2, 0.3))
            results.append(brain.run_neural_projection_cycle(synapse, current, Plasticity(learning_rate=0.1)))
        for key in ("source_spikes", "target_current", "target_spikes", "weights"):
            np.testing.assert_array_equal(results[0][key], results[1][key])

    def test_invalid_source_chunk_fails_before_allocation(self):
        brain = Brain()
        source, target, synapse = projection()
        synapse.source_chunk_index = 1
        with self.assertRaises(IndexError):
            brain.run_neural_projection_cycle(synapse, np.zeros(4, dtype=np.float32), Plasticity())
        self.assertEqual(source.allocated_chunk_indices(), ())

    def test_invalid_target_chunk_fails_deterministically(self):
        brain = Brain()
        source, target, synapse = projection()
        synapse.target_chunk_index = 1
        with self.assertRaises(IndexError):
            brain.run_neural_projection_cycle(synapse, np.zeros(4, dtype=np.float32), Plasticity())

    def test_invalid_source_current_shape_fails_deterministically(self):
        brain = Brain()
        source, target, synapse = projection()
        with self.assertRaises(ValueError):
            brain.run_neural_projection_cycle(synapse, np.zeros(3, dtype=np.float32), Plasticity())

    def test_cycle_does_not_modify_source_current_input(self):
        brain = Brain()
        source, target, synapse = projection()
        current = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        before = current.copy()
        brain.run_neural_projection_cycle(synapse, current, Plasticity())
        np.testing.assert_array_equal(current, before)


if __name__ == "__main__":
    unittest.main()
