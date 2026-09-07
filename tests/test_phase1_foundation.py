import unittest
import numpy as np

from brain import Node, Neuron, LIFNeuronVector, Synapse, NeuralState, Plasticity, NeuronPopulation
from config.anatomy_settings import RegionParameters
from runtime.memory_graph import MemoryGraph
from runtime.memory import Memory
from runtime.gemma_cognitive_engine import GemmaCognitiveEngine
from runtime.cognitive_loop import CognitiveLoop
from runtime.development import Development
from runtime.identity import Identity
from runtime.learning import Learning
from runtime.personality import Personality
from runtime.self_model import SelfModel
from runtime.prediction import Prediction
from runtime.identity_continuity import IdentityContinuity


class TestPhase1FoundationBlankSlate(unittest.TestCase):
    def test_parietal_neural_substrate_primitives(self):
        # 1. Node primitive
        node = Node(node_id="parietal_01", label="SomaticNode")
        self.assertEqual(node.region, "parietal")
        self.assertFalse(node.active)
        node.activate()
        self.assertTrue(node.active)

        # 2. Neuron primitive (LIFNeuronVector)
        neuron = Neuron(size=4)
        self.assertIsInstance(neuron, LIFNeuronVector)
        self.assertEqual(neuron.membrane.shape, (4,))

        # 3. Synapse projection between populations
        params = RegionParameters(name="test_reg", neuron_count=4, chunk_size=4)
        pop_source = NeuronPopulation(params)
        pop_target = NeuronPopulation(params)
        synapse = Synapse(
            source=pop_source,
            source_chunk_index=0,
            target=pop_target,
            target_chunk_index=0,
            source_indices=[0, 1],
            target_indices=[2, 3],
            weights=[0.5, 0.8],
        )
        np.testing.assert_allclose(synapse.weights, np.array([0.5, 0.8], dtype=np.float32), rtol=1e-5)
        result = synapse.propagate(np.array([True, False, False, False]))
        np.testing.assert_allclose(result, np.array([0.0, 0.0, 0.5, 0.0], dtype=np.float32), rtol=1e-5)

        # 4. NeuralState snapshot primitive
        state = NeuralState(
            source_chunk_index=0,
            target_chunk_index=0,
            source_membrane=np.zeros(4, dtype=np.float32),
            target_membrane=np.zeros(4, dtype=np.float32),
            source_spikes=np.zeros(4, dtype=bool),
            target_current=np.zeros(4, dtype=np.float32),
            target_spikes=np.zeros(4, dtype=bool),
        )
        self.assertIsNotNone(state)
        self.assertEqual(state.source_chunk_index, 0)

        # 5. Plasticity interface
        plasticity = Plasticity(learning_rate=0.01)
        self.assertEqual(plasticity.learning_rate, 0.01)

    def test_temporal_blank_slate_initialization(self):
        # Blank slate verification: 0 memory nodes, 0 edges, empty working/episodic state
        memory_graph = MemoryGraph()
        self.assertEqual(len(memory_graph.nodes), 0, "MemoryGraph must initialize with zero nodes (blank slate)")
        self.assertEqual(len(memory_graph.edges), 0, "MemoryGraph must initialize with zero edges (blank slate)")

        memory = Memory()
        self.assertEqual(len(memory.state.experiences), 0)
        self.assertEqual(len(memory.state.working), 0)
        self.assertEqual(len(memory.state.episodic), 0)
        self.assertEqual(len(memory.memory_graph.nodes), 0)

    def test_frontal_cognitive_trigger_execution_cycle(self):
        # Inference function conforming to GemmaCognitiveEngine interface
        def fake_gemma_3_1b_inference(prompt: str) -> str:
            return '{"thought": "Phase 1 perception processed", "action": "none"}'

        engine = GemmaCognitiveEngine(inference=fake_gemma_3_1b_inference)
        identity = Identity()
        memory = Memory()
        learning = Learning(memory)
        personality = Personality()
        self_model = SelfModel()
        prediction = Prediction()
        continuity = IdentityContinuity()

        development = Development(
            identity,
            memory,
            learning,
            personality,
            self_model,
            prediction,
            continuity,
        )

        loop = CognitiveLoop(
            engine,
            learning,
            personality,
            self_model,
            development,
        )

        cycle = loop.process("Phase 1 trigger observation")
        self.assertIsNotNone(cycle)
        self.assertEqual(cycle.decision, "RESPOND")
        self.assertEqual(cycle.reasoning, '{"thought": "Phase 1 perception processed", "action": "none"}')
        self.assertEqual(engine.last_thought, '{"thought": "Phase 1 perception processed", "action": "none"}')
