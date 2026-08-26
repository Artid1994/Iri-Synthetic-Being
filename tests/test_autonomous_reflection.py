import unittest

from runtime.autonomous_learning import AutonomousLearning
from runtime.learning_task import LearningTask
from runtime.reflection import Reflection
from runtime.research_learning import ResearchLearning
from runtime.research_safety import ResearchSafetyGate
from runtime.web_research import ResearchResult


class FakeResearch:
    def search(self, topic):
        return ResearchResult(
            topic=topic,
            source="fake://research",
            content="Verified research result",
        )


class FakeLearning:
    def create_candidate(self, content, category, confidence):
        return object()

    def evaluate(self, candidate):
        class Evaluation:
            accepted = True
            reason = "CONFIDENCE_THRESHOLD_MET"

        return Evaluation()


class TestAutonomousReflection(unittest.TestCase):
    def test_success_reflection(self):
        learning = ResearchLearning(FakeLearning())

        autonomous = AutonomousLearning(
            research=FakeResearch(),
            research_learning=learning,
            safety_gate=ResearchSafetyGate(),
        )

        task = LearningTask("Python")

        result = autonomous.learn(task)

        reflection = Reflection().reflect(
            "SUCCESS",
            observation=result.reason,
            task_topic=task.topic,
        )

        self.assertTrue(result.memory_updated)
        self.assertEqual(reflection.outcome, "SUCCESS")
        self.assertIsNone(reflection.next_task)


if __name__ == "__main__":
    unittest.main()
