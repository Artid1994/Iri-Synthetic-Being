import unittest
from runtime.learning import Learning
from runtime.memory import Memory


class TestLearning(unittest.TestCase):
    def test_low_confidence_is_rejected(self):
        memory = Memory()
        learning = Learning(memory)

        candidate = learning.create_candidate(
            "low confidence",
            confidence=0.4,
        )
        result = learning.evaluate(candidate)

        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "CONFIDENCE_TOO_LOW")
        self.assertTrue(memory.is_empty())

    def test_confidence_threshold_is_accepted(self):
        memory = Memory()
        learning = Learning(memory)

        candidate = learning.create_candidate(
            "learned experience",
            confidence=0.5,
        )
        result = learning.evaluate(candidate)

        self.assertTrue(result.accepted)
        self.assertEqual(
            result.reason,
            "CONFIDENCE_THRESHOLD_MET",
        )
        self.assertIn(
            "learned experience",
            memory.state.episodic,
        )
        self.assertIn(
            "learned experience",
            memory.state.semantic,
        )

    def test_confidence_is_clamped(self):
        memory = Memory()
        learning = Learning(memory)

        high = learning.create_candidate("high", confidence=2.0)
        low = learning.create_candidate("low", confidence=-1.0)

        self.assertEqual(high.confidence, 1.0)
        self.assertEqual(low.confidence, 0.0)

    def test_empty_candidate_is_rejected(self):
        memory = Memory()
        learning = Learning(memory)

        candidate = learning.create_candidate("   ")
        result = learning.evaluate(candidate)

        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "NO_CANDIDATE")


if __name__ == "__main__":
    unittest.main()
