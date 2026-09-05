import unittest

import numpy as np

from brain.population import NeuronPopulation
from brain.synapse import Synapse
from config.anatomy_settings import (
    HIPPOCAMPUS,
    MOTOR_CORTEX,
    NeuronParameters,
    RegionParameters,
)
from regions.hippocampus import Hippocampus
from regions.motor_cortex import MotorCortex


def population(neuron_count=4):
    return NeuronPopulation(
        RegionParameters(
            name="test",
            neuron_count=neuron_count,
            chunk_size=neuron_count,
        )
    )


class TestSynapse(unittest.TestCase):
    def test_propagates_weighted_spikes_to_targets(self):
        source = population()
        target = population()
        synapse = Synapse(source, 0, target, 0, [0, 2], [1, 3], [0.5, 2.0])

        result = synapse.propagate(np.array([True, False, True, False]))

        np.testing.assert_array_equal(result, np.array([0, 0.5, 0, 2.0], dtype=np.float32))

    def test_no_spikes_produce_zero_current(self):
        synapse = Synapse(population(), 0, population(), 0, [0], [1], [2.0])

        result = synapse.propagate(np.zeros(4, dtype=bool))

        np.testing.assert_array_equal(result, np.zeros(4, dtype=np.float32))

    def test_multiple_spikes_sum_at_one_target(self):
        synapse = Synapse(population(), 0, population(), 0, [0, 1], [2, 2], [0.25, 0.75])

        result = synapse.propagate(np.array([True, True, False, False]))

        self.assertEqual(result[2], 1.0)

    def test_output_shape_and_dtype_match_target_chunk(self):
        synapse = Synapse(population(), 0, population(6), 0, [0], [5], [1.0])

        result = synapse.propagate(np.array([True, False, False, False]))

        self.assertEqual(result.shape, (6,))
        self.assertEqual(result.dtype, np.dtype(np.float32))

    def test_does_not_mutate_source_spikes(self):
        synapse = Synapse(population(), 0, population(), 0, [0], [1], [1.0])
        spikes = np.array([True, False, False, False])

        synapse.propagate(spikes)

        np.testing.assert_array_equal(spikes, np.array([True, False, False, False]))

    def test_rejects_source_shape_mismatch(self):
        synapse = Synapse(population(), 0, population(), 0, [0], [1], [1.0])

        with self.assertRaises(ValueError):
            synapse.propagate(np.zeros(3, dtype=bool))

    def test_rejects_index_weight_length_mismatch(self):
        with self.assertRaises(ValueError):
            Synapse(population(), 0, population(), 0, [0, 1], [1], [1.0])

    def test_rejects_out_of_range_indices(self):
        with self.assertRaises(IndexError):
            Synapse(population(), 0, population(), 0, [4], [1], [1.0])

    def test_propagation_drives_target_lif_population(self):
        source = population()
        target = NeuronPopulation(
            RegionParameters(
                name="target",
                neuron_count=1,
                chunk_size=1,
                neuron=NeuronParameters(threshold=1.0),
            )
        )
        synapse = Synapse(source, 0, target, 0, [0], [0], [1.0])

        spikes = synapse.propagate(np.array([True, False, False, False]))

        self.assertTrue(target.step_chunk(0, spikes)[0])

    def test_connects_hippocampus_to_motor_cortex_chunks(self):
        hippocampus = Hippocampus()
        motor_cortex = MotorCortex()
        synapse = Synapse(
            hippocampus.population,
            0,
            motor_cortex.population,
            0,
            [0],
            [0],
            [1.0],
        )

        result = synapse.propagate(np.array([True] + [False] * (HIPPOCAMPUS.chunk_size - 1)))

        self.assertEqual(result.shape, (MOTOR_CORTEX.chunk_size,))
        self.assertEqual(result[0], 1.0)

    def test_rejects_same_endpoint_connection(self):
        neurons = population()

        with self.assertRaises(ValueError):
            Synapse(neurons, 0, neurons, 0, [0], [1], [1.0])

    def test_synapse_has_no_memory_graph_integration(self):
        synapse = Synapse(population(), 0, population(), 0, [0], [1], [1.0])

        self.assertFalse(hasattr(synapse, "memory_graph"))


if __name__ == "__main__":
    unittest.main()
