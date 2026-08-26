import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestBrainNeuralState(unittest.TestCase):

    def test_hippocampus_allocates_on_cognitive_input(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        before = (
            runtime.brain
            .hippocampus
            .population
            .stats
        )

        self.assertEqual(
            before.allocated_neurons,
            0,
        )

        runtime.cognitive_loop.process(
            "tree detected"
        )

        after = (
            runtime.brain
            .hippocampus
            .population
            .stats
        )

        self.assertGreater(
            after.allocated_neurons,
            0,
        )

    def test_motor_cortex_allocates_on_decision(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        before = (
            runtime.brain
            .motor_cortex
            .population
            .stats
        )

        self.assertEqual(
            before.allocated_neurons,
            0,
        )

        cycle = runtime.cognitive_loop.process(
            "move forward"
        )

        self.assertEqual(
            cycle.decision,
            "RESPOND",
        )

        after = (
            runtime.brain
            .motor_cortex
            .population
            .stats
        )

        self.assertGreater(
            after.allocated_neurons,
            0,
        )

    def test_neural_state_is_vectorized(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.cognitive_loop.process(
            "neural test"
        )

        hippocampus = (
            runtime.brain
            .hippocampus
            .population
            ._chunks[0]
        )

        motor = (
            runtime.brain
            .motor_cortex
            .population
            ._chunks[0]
        )

        self.assertEqual(
            hippocampus.membrane.dtype.str,
            "<f4",
        )

        self.assertEqual(
            motor.membrane.dtype.str,
            "<f4",
        )


if __name__ == "__main__":
    unittest.main()
