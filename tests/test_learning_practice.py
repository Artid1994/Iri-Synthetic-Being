import unittest

from runtime.learning_exercise import LearningExercise
from runtime.learning_practice import LearningPractice


class TestLearningPractice(unittest.TestCase):
    def test_correct_answer_passes(self):
        exercise = LearningExercise(
            "2+2 = ?",
            "4",
        )

        result = LearningPractice().check(
            exercise,
            "4",
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.reason, "ANSWER_CORRECT")

    def test_incorrect_answer_fails(self):
        exercise = LearningExercise(
            "2+2 = ?",
            "4",
        )

        result = LearningPractice().check(
            exercise,
            "5",
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "ANSWER_INCORRECT")

    def test_invalid_exercise_is_rejected(self):
        result = LearningPractice().check(
            None,
            "4",
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "INVALID_EXERCISE")


if __name__ == "__main__":
    unittest.main()
