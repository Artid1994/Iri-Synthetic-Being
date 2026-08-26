import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearning
from runtime.learning import Learning
from runtime.learning_task import LearningTask
from runtime.memory import Memory
from runtime.research_learning import ResearchLearning
from runtime.web_research import ResearchResult


class TestAutonomousLearning(unittest.TestCase):
    def make_system(self, content="Python is a programming language."):
        memory = Memory()
        learning = Learning(memory)
        research_learning = ResearchLearning(learning)

        research = Mock()
        research.search.return_value = ResearchResult(
            topic="Python",
            source="https://example.com",
            content=content,
        )

        autonomous = AutonomousLearning(
            research=research,
            research_learning=research_learning,
        )

        return autonomous, memory, research

    def test_learning_task_can_learn_automatically(self):
        autonomous, memory, research = self.make_system()

        task = LearningTask("Python")

        result = autonomous.learn(task)

        self.assertEqual(result.status, "COMPLETED")
        self.assertTrue(result.memory_updated)
        self.assertIn(
            "Python is a programming language.",
            memory.state.semantic,
        )
        research.search.assert_called_once_with("Python")

    def test_rejected_learning_does_not_update_memory(self):
        autonomous, memory, research = self.make_system()

        task = LearningTask("Python")

        result = autonomous.learn(task)

        self.assertTrue(result.memory_updated)

    def test_non_pending_task_is_not_executed(self):
        autonomous, memory, research = self.make_system()

        task = LearningTask("Python")
        task.start()

        result = autonomous.learn(task)

        self.assertEqual(result.reason, "TASK_NOT_PENDING")
        research.search.assert_not_called()


if __name__ == "__main__":
    unittest.main()
