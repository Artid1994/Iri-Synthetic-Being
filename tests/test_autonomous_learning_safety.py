import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearning
from runtime.learning import Learning
from runtime.learning_task import LearningTask
from runtime.memory import Memory
from runtime.research_learning import ResearchLearning
from runtime.research_safety import ResearchSafetyGate
from runtime.web_research import ResearchResult


class TestAutonomousLearningSafety(unittest.TestCase):
    def make_system(self):
        memory = Memory()
        learning = Learning(memory)
        research_learning = ResearchLearning(learning)

        research = Mock()
        research.search.return_value = ResearchResult(
            topic="TTF",
            source="https://example.com",
            content="External information.",
        )

        return (
            AutonomousLearning(
                research,
                research_learning,
                ResearchSafetyGate(),
            ),
            memory,
            research,
        )

    def test_protected_research_never_reaches_memory(self):
        autonomous, memory, research = self.make_system()

        task = LearningTask("TTF")

        result = autonomous.learn(
            task,
            category="CORE",
        )

        self.assertFalse(result.memory_updated)
        self.assertEqual(
            result.reason,
            "PROTECTED_CATEGORY",
        )
        self.assertTrue(memory.is_empty())

        research.search.assert_called_once_with("TTF")

    def test_general_research_can_reach_learning(self):
        autonomous, memory, _ = self.make_system()

        task = LearningTask("TTF")

        result = autonomous.learn(
            task,
            category="GENERAL",
        )

        self.assertTrue(result.memory_updated)
        self.assertEqual(
            result.status,
            "COMPLETED",
        )
        self.assertIn(
            "External information.",
            memory.state.semantic,
        )


if __name__ == "__main__":
    unittest.main()
