import unittest

import numpy as np

from brain.brain import Brain
from brain.plasticity import Plasticity
from brain.population import NeuronPopulation
from brain.synapse import Synapse
from config.anatomy_settings import NeuronParameters, RegionParameters
from runtime.brain_memory_bridge import BrainMemoryBridge
from runtime.cognitive_context import CognitiveContext
from runtime.cognitive_loop import CognitiveLoop
from runtime.development import Development
from runtime.identity import Identity
from runtime.identity_continuity import IdentityContinuity
from runtime.learning import Learning
from runtime.memory import Memory
from runtime.personality import Personality
from runtime.prediction import Prediction
from runtime.self_model import SelfModel
from tests.cognitive_test_helper import FakeCognitive


def make_population(name: str, threshold: float = 1.0) -> NeuronPopulation:
    return NeuronPopulation(
        RegionParameters(
            name=name,
            neuron_count=4,
            chunk_size=4,
            neuron=NeuronParameters(threshold=threshold),
        )
    )


class TestBrainCognitiveBoundary(unittest.TestCase):
    def setUp(self):
        self.brain = Brain()
        self.memory = Memory()
        self.identity = Identity()
        self.learning = Learning(self.memory)
        self.personality = Personality()
        self.self_model = SelfModel()
        self.prediction = Prediction()
        self.continuity = IdentityContinuity()
        self.development = Development(
            identity=self.identity,
            memory=self.memory,
            learning=self.learning,
            personality=self.personality,
            self_model=self.self_model,
            prediction=self.prediction,
            identity_continuity=self.continuity,
        )
        self.cognitive = FakeCognitive()
        self.cognitive_loop = CognitiveLoop(
            cognitive=self.cognitive,
            learning=self.learning,
            personality=self.personality,
            self_model=self.self_model,
            development=self.development,
            prediction=self.prediction,
            brain=self.brain,
        )
        self.bridge = BrainMemoryBridge(self.brain, self.memory)

    def test_cognitive_context_immutability_and_field_isolation(self):
        context = CognitiveContext(
            identity_stage="NEWBORN",
            identity_experience=0,
            self_awareness=0.0,
            self_knowledge=0.0,
            episodic_memory=("exp1",),
            semantic_memory=("rule1",),
            working_memory=("item1",),
            self_history=("history1",),
            recalled_memory=("recalled1",),
        )
        # Verify frozen contract
        with self.assertRaises(AttributeError):
            context.identity_stage = "INFANT"  # type: ignore

        rendered = context.render()
        self.assertIn("IDENTITY_STAGE: NEWBORN", rendered)
        self.assertIn("RECALLED_MEMORY:\n- recalled1", rendered)
        self.assertIn("KNOWN_KNOWLEDGE:\n- rule1", rendered)

    def test_cognitive_loop_reads_state_and_delivers_to_memory_and_brain(self):
        # 1. Experience entry
        cycle = self.cognitive_loop.process("Sensory event alpha")
        self.assertEqual(cycle.decision, "RESPOND")
        self.assertTrue(cycle.experience_recorded)

        # 2. Verify state delivered to Memory
        self.assertIn("Sensory event alpha", self.memory.state.episodic)

        # 3. Verify state delivered to Brain hippocampus storage
        self.assertTrue(self.brain.hippocampus.has_memory("Sensory event alpha"))

        # 4. Verify motor cortex stimulated on decision
        self.assertGreater(
            self.brain.motor_cortex.population.stats.allocated_neurons, 0
        )

    def test_cognitive_processing_does_not_mutate_synapse_weights_or_neural_arrays(self):
        # Setup projection synapse in brain
        source = make_population("src")
        target = make_population("tgt")
        synapse = Synapse(source, 0, target, 0, [0], [0], [1.0])
        initial_weights = synapse.weights.copy()

        # Run projection cycle
        self.brain.run_neural_projection_cycle(
            synapse, np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32), Plasticity()
        )
        cycle_weights = synapse.weights.copy()

        # Run cognitive processing
        self.cognitive_loop.process("Cognitive reasoning input")

        # Synapse weights must NOT be touched or mutated by cognitive core
        np.testing.assert_array_equal(synapse.weights, cycle_weights)
        self.assertNotEqual(id(synapse.weights), id(initial_weights))

    def test_bridge_snapshot_remains_isolated_from_cognitive_loop(self):
        # Inspection via bridge
        neural_snap = self.bridge.neural_state_snapshot()
        memory_snap = self.bridge.memory_activity_snapshot()

        # Run cognitive loop
        self.cognitive_loop.process("Cognitive event beta")

        # Prior snapshots must remain unaffected
        if neural_snap is not None:
            self.assertNotIn("Cognitive event beta", str(neural_snap))
        self.assertEqual(memory_snap["nodes"], [])


if __name__ == "__main__":
    unittest.main()
