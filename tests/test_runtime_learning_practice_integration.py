import unittest

from runtime.runtime import TranscendingRuntime
from runtime.learning_exercise import LearningExercise
from tests.cognitive_test_helper import FakeCognitive


class TestRuntimeLearningPracticeIntegration(unittest.TestCase):
    def test_runtime_practice_exercise_success_updates_memory_and_brain(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())
        exercise = LearningExercise(question="What is 7 * 8?", expected_answer="56")

        result = runtime.practice_exercise(exercise, "56")

        self.assertTrue(result.passed)
        self.assertEqual(result.reason, "ANSWER_CORRECT")
        self.assertIn("What is 7 * 8? = 56", runtime.memory.state.episodic)
        self.assertTrue(runtime.brain.hippocampus.has_memory("What is 7 * 8? = 56"))

    def test_runtime_practice_exercise_failure_does_not_update_memory(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())
        exercise = LearningExercise(question="What is 7 * 8?", expected_answer="56")

        result = runtime.practice_exercise(exercise, "54")

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "ANSWER_INCORRECT")
        self.assertNotIn("What is 7 * 8? = 54", runtime.memory.state.episodic)
        self.assertFalse(runtime.brain.hippocampus.has_memory("What is 7 * 8? = 54"))


if __name__ == "__main__":
    unittest.main()
