import unittest

from runtime.learning_exercise_generation_result import (
    LearningExerciseGenerationResult,
)


class TestLearningExerciseGenerationResult(unittest.TestCase):

    def test_accepted_result(self):
        result = LearningExerciseGenerationResult(
            accepted=True,
            attempts=1,
            reason="ACCEPTED",
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.attempts, 1)
        self.assertEqual(result.reason, "ACCEPTED")

    def test_rejected_result(self):
        result = LearningExerciseGenerationResult(
            accepted=False,
            attempts=3,
            reason="MAX_ATTEMPTS_REACHED",
        )

        self.assertFalse(result.accepted)
        self.assertEqual(result.attempts, 3)
        self.assertEqual(
            result.reason,
            "MAX_ATTEMPTS_REACHED",
        )

    def test_attempts_must_be_positive(self):
        with self.assertRaises(ValueError):
            LearningExerciseGenerationResult(
                accepted=False,
                attempts=0,
                reason="MAX_ATTEMPTS_REACHED",
            )

    def test_reason_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            LearningExerciseGenerationResult(
                accepted=False,
                attempts=1,
                reason="",
            )


if __name__ == "__main__":
    unittest.main()
