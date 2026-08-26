import unittest
from unittest.mock import Mock

from brain.brain import Brain
from runtime.autonomous_learning import AutonomousLearning
from runtime.learning_task import LearningTask
from runtime.research_learning import ResearchLearning
from runtime.research_safety import ResearchSafetyGate
from runtime.web_research import ResearchResult


class TestAutonomousLearningBrain(unittest.TestCase):
    def _create(self, content):
        research = Mock()
        research.search.return_value = ResearchResult(
            topic="Python",
            source="test",
            content=content,
        )

        learning = Mock()
        learning_result = Mock()
        learning_result.accepted = True
        learning_result.reason = "CONFIDENCE_THRESHOLD_MET"
        learning.evaluate.return_value = learning_result

        research_learning = ResearchLearning(learning)

        brain = Brain()

        autonomous = AutonomousLearning(
            research=research,
            research_learning=research_learning,
            safety_gate=ResearchSafetyGate(),
        )

        return autonomous, brain

    def test_successful_learning_updates_hippocampus(self):
        autonomous, brain = self._create(
            "Python is a programming language."
        )

        task = LearningTask("Python")

        result = autonomous.learn(task)

        if result.memory_updated:
            brain.store_memory(result.topic)

        self.assertTrue(result.memory_updated)
        self.assertTrue(brain.has_memory("Python"))
        self.assertEqual(
            brain.hippocampus.memory_count,
            1,
        )

    def test_failed_learning_does_not_update_hippocampus(self):
        autonomous, brain = self._create("")

        task = LearningTask("Python")

        result = autonomous.learn(task)

        if result.memory_updated:
            brain.store_memory(result.topic)

        self.assertFalse(result.memory_updated)
        self.assertFalse(brain.has_memory("Python"))
        self.assertEqual(
            brain.hippocampus.memory_count,
            0,
        )


if __name__ == "__main__":
    unittest.main()
