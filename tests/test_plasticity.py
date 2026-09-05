import unittest

import numpy as np

from brain.plasticity import Plasticity
from brain.population import NeuronPopulation
from brain.synapse import Synapse
from config.anatomy_settings import NeuronParameters, RegionParameters


def population(size=4, threshold=1.0):
    return NeuronPopulation(
        RegionParameters(
            name="test",
            neuron_count=size,
            chunk_size=size,
            neuron=NeuronParameters(threshold=threshold),
        )
    )


def synapse(source_indices=(0, 1), target_indices=(1, 2), weights=(0.2, 0.8)):
    return Synapse(
        population(),
        0,
        population(),
        0,
        source_indices,
        target_indices,
        weights,
    )


class TestPlasticity(unittest.TestCase):
    def test_coactive_connection_increases_by_learning_rate(self):
        connection = synapse()
        plasticity = Plasticity(learning_rate=0.1, min_weight=0.0, max_weight=1.0)

        result = plasticity.adapt(
            connection,
            np.array([True, False, False, False]),
            np.array([False, True, False, False]),
        )

        np.testing.assert_array_equal(result, np.array([0.3, 0.8], dtype=np.float32))
        np.testing.assert_array_equal(connection.weights, result)

    def test_source_only_activity_does_not_update(self):
        connection = synapse()
        before = connection.weights.copy()

        Plasticity(learning_rate=0.1).adapt(
            connection,
            np.array([True, False, False, False]),
            np.zeros(4, dtype=bool),
        )

        np.testing.assert_array_equal(connection.weights, before)

    def test_target_only_activity_does_not_update(self):
        connection = synapse()
        before = connection.weights.copy()

        Plasticity(learning_rate=0.1).adapt(
            connection,
            np.zeros(4, dtype=bool),
            np.array([False, True, False, False]),
        )

        np.testing.assert_array_equal(connection.weights, before)

    def test_only_coactive_mappings_update(self):
        connection = synapse()

        Plasticity(learning_rate=0.1).adapt(
            connection,
            np.array([True, True, False, False]),
            np.array([False, True, True, False]),
        )

        np.testing.assert_allclose(connection.weights, np.array([0.3, 0.9], dtype=np.float32))

    def test_weight_is_clamped_to_maximum(self):
        connection = synapse(weights=(0.95, 0.2))

        Plasticity(learning_rate=0.2, max_weight=1.0).adapt(
            connection,
            np.array([True, False, False, False]),
            np.array([False, True, False, False]),
        )

        self.assertEqual(connection.weights[0], 1.0)

    def test_weight_is_clamped_to_minimum(self):
        connection = synapse(weights=(0.2, 0.8))
        connection.weights[0] = -0.5

        Plasticity(learning_rate=0.1, min_weight=0.0).adapt(
            connection,
            np.zeros(4, dtype=bool),
            np.zeros(4, dtype=bool),
        )

        self.assertEqual(connection.weights[0], 0.0)

    def test_repeated_adaptation_is_bounded_and_deterministic(self):
        first = synapse(weights=(0.2, 0.8))
        second = synapse(weights=(0.2, 0.8))
        rule = Plasticity(learning_rate=0.3, max_weight=1.0)
        source = np.array([True, False, False, False])
        target = np.array([False, True, False, False])

        for _ in range(5):
            rule.adapt(first, source, target)
            rule.adapt(second, source, target)

        np.testing.assert_array_equal(first.weights, second.weights)
        self.assertEqual(first.weights[0], 1.0)

    def test_rejects_source_shape_mismatch(self):
        with self.assertRaises(ValueError):
            Plasticity().adapt(synapse(), np.zeros(3, dtype=bool), np.zeros(4, dtype=bool))

    def test_rejects_target_shape_mismatch(self):
        with self.assertRaises(ValueError):
            Plasticity().adapt(synapse(), np.zeros(4, dtype=bool), np.zeros(3, dtype=bool))

    def test_rejects_invalid_rule_configuration(self):
        with self.assertRaises(ValueError):
            Plasticity(learning_rate=-0.1)
        with self.assertRaises(ValueError):
            Plasticity(min_weight=1.0, max_weight=0.0)
        with self.assertRaises(ValueError):
            Plasticity(learning_rate=float("nan"))

    def test_does_not_mutate_spike_inputs(self):
        connection = synapse()
        source = np.array([True, False, False, False])
        target = np.array([False, True, False, False])
        source_before = source.copy()
        target_before = target.copy()

        Plasticity().adapt(connection, source, target)

        np.testing.assert_array_equal(source, source_before)
        np.testing.assert_array_equal(target, target_before)

    def test_preserves_synapse_endpoints_and_mapping(self):
        connection = synapse()
        before = (
            connection.source,
            connection.source_chunk_index,
            connection.target,
            connection.target_chunk_index,
            connection.source_indices.copy(),
            connection.target_indices.copy(),
        )

        Plasticity().adapt(
            connection,
            np.array([True, True, False, False]),
            np.array([False, True, True, False]),
        )

        self.assertIs(connection.source, before[0])
        self.assertEqual(connection.source_chunk_index, before[1])
        self.assertIs(connection.target, before[2])
        self.assertEqual(connection.target_chunk_index, before[3])
        np.testing.assert_array_equal(connection.source_indices, before[4])
        np.testing.assert_array_equal(connection.target_indices, before[5])

    def test_weights_remain_float32_and_shape_is_preserved(self):
        connection = synapse()

        result = Plasticity().adapt(
            connection,
            np.array([True, True, False, False]),
            np.array([False, True, True, False]),
        )

        self.assertEqual(result.dtype, np.dtype(np.float32))
        self.assertEqual(result.shape, (2,))
        self.assertEqual(connection.weights.dtype, np.dtype(np.float32))

    def test_updated_weights_change_future_propagation(self):
        connection = Synapse(
            population(), 0, population(), 0, [0], [1], [0.5]
        )
        source = np.array([True, False, False, False])
        target = np.array([False, True, False, False])
        Plasticity(learning_rate=0.25).adapt(connection, source, target)

        np.testing.assert_array_equal(
            connection.propagate(source),
            np.array([0.0, 0.75, 0.0, 0.0], dtype=np.float32),
        )

    def test_neural_activity_can_come_from_lif_populations(self):
        source = population(threshold=1.0)
        target = population(threshold=1.0)
        connection = Synapse(source, 0, target, 0, [0], [1], [0.5])
        source_spikes = source.step_chunk(0, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32))
        target_spikes = target.step_chunk(0, np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32))

        Plasticity(learning_rate=0.25).adapt(connection, source_spikes, target_spikes)

        self.assertEqual(connection.weights[0], 0.75)

    def test_has_no_memory_graph_dependency(self):
        plasticity = Plasticity()

        self.assertFalse(hasattr(plasticity, "memory_graph"))


if __name__ == "__main__":
    unittest.main()
