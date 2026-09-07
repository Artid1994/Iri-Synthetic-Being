"""Test Plasticity & Dynamic Graph Triggering from External Experience."""

import unittest
import numpy as np

from runtime.runtime import TranscendingRuntime
from runtime.memory import Memory
from runtime.memory_graph import MemoryGraph
from brain.brain import Brain
from brain.plasticity import Plasticity
from brain.synapse import Synapse
from brain.population import NeuronPopulation
from config.anatomy_settings import RegionParameters, NeuronParameters
from tests.cognitive_test_helper import FakeCognitive


class TestExperiencePlasticityTrigger(unittest.TestCase):
    def test_blank_slate_begins_with_zero_edges_and_nodes(self):
        memory = Memory()
        self.assertEqual(len(memory.memory_graph.nodes), 0)
        self.assertEqual(len(memory.memory_graph.edges), 0)
        self.assertEqual(len(memory.state.episodic), 0)
        self.assertEqual(len(memory.state.semantic), 0)

    def test_experience_dynamically_generates_memory_graph_and_edges(self):
        memory = Memory()
        # Triggering dynamic experience
        memory.add_experience("Quantum observation", source_url="https://physics.org/quantum")
        self.assertEqual(len(memory.memory_graph.nodes), 1)
        self.assertIn("EPISODIC:Quantum observation", memory.memory_graph.nodes)
        
        # Associative plasticity: linking episodic experience to semantic principle
        memory.associate("Quantum observation", "Wavefunction collapse")
        self.assertEqual(len(memory.memory_graph.nodes), 2)
        self.assertIn("SEMANTIC:Wavefunction collapse", memory.memory_graph.nodes)
        self.assertIn(
            ("EPISODIC:Quantum observation", "SEMANTIC:Wavefunction collapse"),
            memory.memory_graph.edges,
        )
        edge = memory.memory_graph.edges[("EPISODIC:Quantum observation", "SEMANTIC:Wavefunction collapse")]
        self.assertGreaterEqual(edge.weight, 1.0)

        # Repeated co-activation strengthens connection (LTP in memory graph)
        prev_weight = edge.weight
        memory.associate("Quantum observation", "Wavefunction collapse")
        self.assertGreater(edge.weight, prev_weight)

    def test_neural_substrate_plasticity_adaptation_cycle(self):
        brain = Brain()
        source_pop = NeuronPopulation(RegionParameters("src", 4, 4, neuron=NeuronParameters(threshold=0.5)))
        target_pop = NeuronPopulation(RegionParameters("tgt", 4, 4, neuron=NeuronParameters(threshold=0.5)))
        synapse = Synapse(source_pop, 0, target_pop, 0, [0, 1], [0, 1], [0.6, 0.4])
        plasticity = Plasticity(learning_rate=0.15)

        # Apply input current driving spike in source 0
        input_current = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        cycle_result = brain.run_neural_projection_cycle(synapse, input_current, plasticity)

        # Verify source spiked, target received current, and synapse adapted
        self.assertTrue(cycle_result["source_spikes"][0])
        self.assertGreater(cycle_result["target_current"][0], 0.0)
        self.assertEqual(cycle_result["weights"][0], np.float32(0.75))
        self.assertEqual(cycle_result["weights"][1], np.float32(0.4))

    def test_runtime_closed_loop_experience_triggers_memory_and_brain_sync(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())
        self.assertEqual(runtime.brain.hippocampus.memory_count, 0)
        self.assertEqual(len(runtime.memory.memory_graph.nodes), 0)

        # Cognitive trigger through cognitive loop
        runtime.cognitive_loop.process("Optical lattice clock")

        # Verify dynamic creation in hippocampus and memory graph
        self.assertTrue(runtime.brain.hippocampus.has_memory("Optical lattice clock"))
        self.assertEqual(runtime.brain.hippocampus.memory_count, 1)
        self.assertIn("Optical lattice clock", runtime.memory.state.episodic)
        self.assertIn("EPISODIC:Optical lattice clock", runtime.memory.memory_graph.nodes)


if __name__ == "__main__":
    unittest.main()
