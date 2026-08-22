import unittest

from runtime.learning import Learning
from runtime.memory import Memory
from runtime.safety_event import SafetyEvent


class TestLearningSafety(unittest.TestCase):
    def test_safety_candidate_cannot_be_learned_normally(self):
        memory = Memory()
        learning = Learning(memory)

        candidate = learning.create_candidate(
            "move limit exceeded",
            category="SAFETY",
            confidence=1.0,
        )

        result = learning.evaluate(candidate)

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.reason,
            "SAFETY_CANDIDATE_REQUIRES_SEPARATE_POLICY",
        )

        self.assertTrue(memory.is_empty())

    def test_safety_event_is_observed_without_changing_memory(self):
        memory = Memory()
        learning = Learning(memory)

        event = SafetyEvent(
            action="move",
            value=(2.0, 0.0),
            reason="move_limit_exceeded",
        )

        result = learning.observe_safety_event(event)

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.reason,
            "SAFETY_EVENT_OBSERVED_ONLY",
        )

        self.assertTrue(memory.is_empty())


if __name__ == "__main__":
    unittest.main()
