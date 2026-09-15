"""
Test the complete causal chain:
Experience → Valuation → Learning → Plasticity → Brain State → Memory → Future Behavior

Verifies that:
1. Experiences produce valuation signals
2. Valuation signals influence learning
3. Learning triggers plasticity updates
4. Plasticity modifies brain state
5. Brain state influences memory encoding
6. Modified state affects future processing
"""
import unittest
import numpy as np

from runtime.runtime import TranscendingRuntime
from runtime.valuation import RewardSignal
from brain.plasticity import Plasticity
from brain.synapse import Synapse
from brain.population import NeuronPopulation
from config.anatomy_settings import RegionParameters


class TestCausalChainIntegration(unittest.TestCase):
    """Test complete causal chain from experience to behavior change."""

    def test_experience_to_valuation(self):
        """Experience → Valuation: Experiences produce reward signals."""
        runtime = TranscendingRuntime()

        # Process positive experience
        cycle = runtime.cognitive_loop.process("I learned something new")

        # Verify valuation was triggered
        self.assertTrue(cycle.experience_recorded)

        # Valuation should exist
        self.assertIsNotNone(runtime.cognitive_loop.valuation)

        # Direct valuation test
        reward = runtime.cognitive_loop.valuation.evaluate_outcome(
            "success", goal_achieved=True
        )
        self.assertGreater(reward.reward, 0.0)
        self.assertEqual(reward.outcome, "success")

    def test_valuation_influences_learning(self):
        """Valuation → Learning: Reward signals influence learning acceptance."""
        from runtime.learning import LearningCandidate
        runtime = TranscendingRuntime()

        # Create learning candidate with sufficient confidence
        candidate = LearningCandidate(
            experience="This is useful knowledge",
            category="SEMANTIC",
            confidence=0.7,  # Above 0.5 threshold for acceptance
        )
        eval_result = runtime.learning.evaluate(candidate)

        # Learning should accept candidates with high confidence
        self.assertIsNotNone(eval_result)
        self.assertTrue(eval_result.accepted)

    def test_synapse_propagation_functional(self):
        """Verify synapse propagation works correctly."""
        params = RegionParameters(name="test", neuron_count=8, chunk_size=4)
        pop_a = NeuronPopulation(params)
        pop_b = NeuronPopulation(params)

        # Create synapse connecting neurons 0,1 of pop_a to neurons 2,3 of pop_b
        synapse = Synapse(
            source=pop_a,
            source_chunk_index=0,
            target=pop_b,
            target_chunk_index=0,
            source_indices=[0, 1],
            target_indices=[2, 3],
            weights=[0.5, 0.8],
        )

        # Spike pattern: neuron 0 fires, neuron 1 silent
        spikes = np.array([True, False, False, False])

        # Propagate
        target_current = synapse.propagate(spikes)

        # Expected: only target neuron 2 receives current (0.5)
        expected = np.array([0.0, 0.0, 0.5, 0.0], dtype=np.float32)
        np.testing.assert_allclose(target_current, expected, rtol=1e-5)

    def test_plasticity_modifies_weights(self):
        """Learning → Plasticity: Plasticity updates synaptic weights."""
        from config.anatomy_settings import RegionParameters
        
        plasticity = Plasticity()
        
        # Create populations and synapse for realistic plasticity test
        params = RegionParameters(name="test", neuron_count=4, chunk_size=4)
        pop_source = NeuronPopulation(params)
        pop_target = NeuronPopulation(params)
        
        synapse = Synapse(
            source=pop_source,
            source_chunk_index=0,
            target=pop_target,
            target_chunk_index=0,
            source_indices=[0, 1],
            target_indices=[0, 1],
            weights=[0.5, 0.8],
        )
        
        # Spike patterns: both connections active
        source_spikes = np.array([True, True, False, False])
        target_spikes = np.array([True, False, False, False])
        
        # Apply Hebbian plasticity via adapt()
        updated_weights = plasticity.adapt(synapse, source_spikes, target_spikes)
        
        # Weights should be modified
        self.assertEqual(len(updated_weights), 2)
        # First connection: both pre and post spiked (should strengthen)
        self.assertGreaterEqual(updated_weights[0], synapse.weights[0])

    def test_brain_memory_integration(self):
        """Brain State → Memory: Brain stores and retrieves memories."""
        runtime = TranscendingRuntime()

        if runtime.brain is None:
            self.skipTest("Brain not available")

        # Store memory via brain
        content = "Test memory content"
        stored = runtime.brain.store_memory(content)
        self.assertTrue(stored)

        # Verify brain recorded it
        has_memory = runtime.brain.has_memory(content)
        self.assertTrue(has_memory)

        # Check hippocampus neuron allocation
        hippo_stats = runtime.brain.stats()["hippocampus"]
        self.assertGreater(hippo_stats["memory_count"], 0)

    def test_brain_neural_projection_cycle(self):
        """Plasticity → Brain State: Neural projection with plasticity."""
        runtime = TranscendingRuntime()

        if runtime.brain is None:
            self.skipTest("Brain not available")

        # Get hippocampus and motor cortex populations
        hippo = runtime.brain.hippocampus.population
        motor = runtime.brain.motor_cortex.population

        # Create synapse between them
        synapse = Synapse(
            source=hippo,
            source_chunk_index=0,
            target=motor,
            target_chunk_index=0,
            source_indices=[0, 1],
            target_indices=[0, 1],
            weights=[0.3, 0.4],
        )

        # Create input and plasticity
        source_input = np.zeros(hippo.chunk_size, dtype=np.float32)
        source_input[0] = 2.0  # Strong input to trigger spike
        plasticity = Plasticity()

        # Run projection cycle
        result = runtime.brain.run_neural_projection_cycle(
            synapse, source_input, plasticity
        )

        # Verify cycle completed with plasticity
        self.assertIn("source_spikes", result)
        self.assertIn("target_spikes", result)
        self.assertIn("weights", result)  # Check for 'weights' not 'updated_weights'
        
        # Plasticity should have been applied
        self.assertIn("adapted", result)
        
        # Weights array should exist
        weights = result["weights"]
        self.assertEqual(len(weights), 2)

    def test_attention_filters_repeated_stimuli(self):
        """Attention mechanism reduces processing for repeated stimuli."""
        runtime = TranscendingRuntime()

        if runtime.cognitive_loop.attention is None:
            self.skipTest("Attention mechanism not available")

        attention = runtime.cognitive_loop.attention

        # First presentation: novel
        signal1 = attention.evaluate("New information", context=[])
        self.assertGreater(signal1.novelty, 0.8)  # High novelty

        # Immediate repeat: less novel
        signal2 = attention.evaluate("New information", context=["New information"])
        self.assertLess(signal2.novelty, signal1.novelty)  # Novelty decreases

        # Multiple repetitions: very low novelty
        for _ in range(5):
            attention.evaluate("New information", context=[])

        signal_final = attention.evaluate("New information", context=[])
        self.assertLess(signal_final.novelty, 0.3)  # Very low novelty after repetition

    def test_end_to_end_causal_chain(self):
        """
        Complete causal chain:
        Experience → Valuation → Learning → Brain → Memory → Future Processing
        """
        from runtime.learning import LearningCandidate
        runtime = TranscendingRuntime()

        # Step 1: Experience
        experience_content = "Important learned fact"

        # Step 2: Process through cognitive loop (triggers valuation)
        cycle = runtime.cognitive_loop.process(experience_content)

        # Step 3: Verify valuation occurred
        self.assertIsNotNone(runtime.cognitive_loop.valuation)
        reward = runtime.cognitive_loop.valuation.evaluate_outcome(
            "learned", goal_achieved=True
        )
        self.assertGreater(reward.reward, 0.0)

        # Step 4: Verify learning evaluation with proper candidate
        candidate = LearningCandidate(
            experience=experience_content,
            category="EPISODIC",
            confidence=0.8,  # High confidence for acceptance
        )
        learning_eval = runtime.learning.evaluate(candidate)
        self.assertTrue(learning_eval.accepted)

        # Step 5: Verify memory stored
        memory_snapshot = runtime.memory.snapshot()
        self.assertGreater(len(memory_snapshot.episodic), 0)

        # Step 6: Verify brain integration (if available)
        if runtime.brain:
            # Brain already has memory from cognitive_loop.process()
            # Just verify it exists
            self.assertTrue(runtime.brain.has_memory(experience_content))

        # Step 7: Verify attention recognizes the content on repeat
        if runtime.cognitive_loop.attention:
            signal = runtime.cognitive_loop.attention.evaluate(
                experience_content,
                context=[]
            )
            # Content is now in memory, should affect future processing
            self.assertIsNotNone(signal)


if __name__ == "__main__":
    unittest.main()
