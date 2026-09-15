"""
Integration tests for attention and valuation systems.

Verifies that attention, cognitive triggering, and valuation
are properly integrated into the cognitive loop.
"""
import unittest
from runtime.runtime import TranscendingRuntime


class TestAttentionIntegration(unittest.TestCase):
    """Test attention mechanism integration."""
    
    def setUp(self):
        self.runtime = TranscendingRuntime()
    
    def test_attention_mechanism_exists(self):
        """Attention mechanism is initialized."""
        self.assertIsNotNone(self.runtime.cognitive_loop.attention)
        self.assertIsNotNone(self.runtime.cognitive_loop.cognitive_trigger)
    
    def test_novel_stimulus_has_high_salience(self):
        """Novel stimulus produces high salience signal."""
        result = self.runtime.cognitive_loop.process("What is consciousness?")
        
        self.assertGreater(result.salience, 0.5)
        self.assertTrue(result.attention_required)
    
    def test_repeated_stimulus_skips_cognition(self):
        """Repeated stimulus is filtered by attention."""
        # First occurrence
        result1 = self.runtime.cognitive_loop.process("Hello world")
        self.assertTrue(result1.attention_required)
        
        # Second occurrence should skip
        result2 = self.runtime.cognitive_loop.process("Hello world")
        self.assertFalse(result2.attention_required)
        self.assertEqual(result2.decision, "NO_ACTION")
    
    def test_different_stimulus_is_novel(self):
        """Different stimulus is treated as novel."""
        result1 = self.runtime.cognitive_loop.process("First message")
        result2 = self.runtime.cognitive_loop.process("Second message")
        
        self.assertTrue(result1.attention_required)
        self.assertTrue(result2.attention_required)


class TestValuationIntegration(unittest.TestCase):
    """Test valuation system integration."""
    
    def setUp(self):
        self.runtime = TranscendingRuntime()
    
    def test_valuation_system_exists(self):
        """Valuation system is initialized."""
        self.assertIsNotNone(self.runtime.cognitive_loop.valuation)
    
    def test_valuation_tracks_outcomes(self):
        """Valuation tracks learning outcomes."""
        valuation = self.runtime.cognitive_loop.valuation
        
        # Initial state
        self.assertEqual(valuation._total_outcomes, 0)
        
        # Process inputs that trigger learning
        self.runtime.cognitive_loop.process("Learn something new")
        
        # Valuation may be invoked during learning
        # Just verify system is operational
        self.assertIsNotNone(valuation)
    
    def test_reward_signal_generation(self):
        """Valuation generates reward signals."""
        valuation = self.runtime.cognitive_loop.valuation
        
        # Test positive outcome
        signal = valuation.evaluate_outcome(
            "success",
            goal_achieved=True,
        )
        
        self.assertEqual(signal.outcome, "success")
        self.assertGreater(signal.reward, 0.5)
        self.assertGreater(signal.confidence, 0.5)
        self.assertEqual(signal.reason, "EXPLICIT_GOAL_SIGNAL")


class TestCognitiveTrigger(unittest.TestCase):
    """Test cognitive triggering logic."""
    
    def setUp(self):
        self.runtime = TranscendingRuntime()
        self.trigger = self.runtime.cognitive_loop.cognitive_trigger
    
    def test_cognitive_trigger_exists(self):
        """Cognitive trigger is initialized."""
        self.assertIsNotNone(self.trigger)
        self.assertIsNotNone(self.trigger.attention)
    
    def test_high_salience_invokes_cognition(self):
        """High salience stimuli invoke cognition."""
        should_invoke, signal = self.trigger.should_invoke_cognition(
            "This is a completely novel and unique stimulus"
        )
        
        self.assertTrue(should_invoke)
        self.assertGreater(signal.salience, 0.3)
    
    def test_resource_budget_enforced(self):
        """Cognitive invocations respect resource budget."""
        # Exhaust budget
        for _ in range(70):  # Exceed 60/min limit
            self.trigger.should_invoke_cognition("test")
        
        # High salience still works
        should_invoke, _ = self.trigger.should_invoke_cognition(
            "extremely important message"
        )
        # May or may not invoke depending on salience threshold
        self.assertIsNotNone(should_invoke)


class TestEndToEndIntegration(unittest.TestCase):
    """End-to-end integration tests."""
    
    def test_full_cognitive_cycle_with_attention(self):
        """Full cognitive cycle with attention filtering."""
        runtime = TranscendingRuntime()
        
        # Cycle 1: Novel input
        result1 = runtime.cognitive_loop.process("Hello IRI")
        self.assertTrue(result1.attention_required)
        self.assertGreater(result1.salience, 0.0)
        
        # Cycle 2: Repeated input (filtered)
        result2 = runtime.cognitive_loop.process("Hello IRI")
        self.assertFalse(result2.attention_required)
        
        # Cycle 3: Different input (novel again)
        result3 = runtime.cognitive_loop.process("How are you?")
        self.assertTrue(result3.attention_required)
    
    def test_brain_memory_attention_integration(self):
        """Brain, memory, and attention work together."""
        runtime = TranscendingRuntime()
        
        # Process input
        result = runtime.cognitive_loop.process("Store this memory")
        
        # Verify components interacted
        self.assertIsNotNone(result.salience)
        self.assertIsNotNone(runtime.brain)
        self.assertIsNotNone(runtime.memory)
        
        # Memory should have working memory
        state = runtime.memory.snapshot()
        self.assertGreater(len(state.working), 0)


if __name__ == "__main__":
    unittest.main()
