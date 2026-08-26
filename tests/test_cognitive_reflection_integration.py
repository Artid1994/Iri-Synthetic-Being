import unittest
from unittest.mock import Mock

from runtime.cognitive_loop import CognitiveLoop
from runtime.development import Development
from runtime.identity_continuity import IdentityContinuity
from runtime.identity import Identity
from runtime.learning import Learning
from runtime.memory import Memory
from runtime.personality import Personality
from runtime.prediction import Prediction
from runtime.reflection import Reflection
from runtime.self_model import SelfModel


class FakeCognitive:
    def think(self, text, context=""):
        return "RESPOND"


class TestCognitiveReflectionIntegration(unittest.TestCase):
    def _create_loop(self):
        memory = Memory()
        learning = Learning(memory)

        development = Development(
            Identity(),
            memory,
            learning,
            Personality(),
            SelfModel(),
            Prediction(),
            IdentityContinuity(),
        )

        loop = CognitiveLoop(
            cognitive=FakeCognitive(),
            learning=learning,
            personality=Personality(),
            self_model=SelfModel(),
            development=development,
            prediction=Prediction(),
        )

        loop.reflection = Reflection()

        return loop, memory

    def test_successful_cognitive_cycle_can_create_reflection_lesson(self):
        loop, memory = self._create_loop()

        cycle = loop.process("tree detected")

        result = loop.reflection.reflect(
            "SUCCESS",
            observation=cycle.reasoning,
            task_topic=cycle.input_text,
        )

        self.assertEqual(result.outcome, "SUCCESS")
        self.assertTrue(result.lesson)

        memory.add_experience(result.lesson)

        self.assertIn(
            result.lesson,
            memory.state.episodic,
        )

    def test_failed_reflection_creates_next_task(self):
        loop, _ = self._create_loop()

        result = loop.reflection.reflect(
            "FAILURE",
            observation="response failed",
            task_topic="tree detection",
        )

        self.assertEqual(result.outcome, "FAILURE")
        self.assertIsNotNone(result.next_task)
        self.assertIn(
            "tree detection",
            result.next_task,
        )

    def test_missing_knowledge_reflection_creates_research_task(self):
        loop, _ = self._create_loop()

        result = loop.reflection.reflect(
            "MISSING_KNOWLEDGE",
            observation="knowledge insufficient",
            task_topic="tree detection",
        )

        self.assertEqual(
            result.outcome,
            "MISSING_KNOWLEDGE",
        )
        self.assertIsNotNone(result.next_task)
        self.assertIn(
            "tree detection",
            result.next_task,
        )


if __name__ == "__main__":
    unittest.main()
