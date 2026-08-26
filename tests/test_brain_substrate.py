import unittest

import numpy as np

from brain.brain import Brain
from brain.neuron import LIFNeuronVector
from config.anatomy_settings import (
    HIPPOCAMPUS,
    MOTOR_CORTEX,
    TOTAL_NEURONS,
)
from brain.population import NeuronPopulation


class TestBrainSubstrate(unittest.TestCase):

    def test_biological_scale(self):
        brain = Brain()

        self.assertEqual(
            brain.hippocampus.neuron_count,
            40_000_000,
        )
        self.assertEqual(
            brain.motor_cortex.neuron_count,
            60_000_000,
        )
        self.assertEqual(
            brain.neuron_count,
            100_000_000,
        )

    def test_large_population_is_lazy(self):
        population = NeuronPopulation(
            HIPPOCAMPUS
        )

        self.assertEqual(
            population.stats.logical_neurons,
            40_000_000,
        )
        self.assertEqual(
            population.stats.allocated_neurons,
            0,
        )

    def test_only_requested_chunk_is_allocated(self):
        population = NeuronPopulation(
            MOTOR_CORTEX
        )

        current = np.ones(
            MOTOR_CORTEX.chunk_size,
            dtype=np.float32,
        )

        spikes = population.step_chunk(
            0,
            current,
        )

        self.assertEqual(
            len(spikes),
            MOTOR_CORTEX.chunk_size,
        )
        self.assertEqual(
            population.stats.allocated_neurons,
            MOTOR_CORTEX.chunk_size,
        )

    def test_lif_generates_spike(self):
        neuron = LIFNeuronVector(4)

        spikes = neuron.step(
            np.array(
                [1.0, 0.0, 1.2, 0.0],
                dtype=np.float32,
            )
        )

        self.assertTrue(spikes[0])
        self.assertFalse(spikes[1])
        self.assertTrue(spikes[2])

        self.assertEqual(
            neuron.membrane[0],
            0.0,
        )
        self.assertEqual(
            neuron.membrane[2],
            0.0,
        )


if __name__ == "__main__":
    unittest.main()
