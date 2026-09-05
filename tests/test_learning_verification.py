import unittest

from runtime.learning_exercise import LearningExercise
from runtime.learning_verification import LearningVerification


class TestLearningVerification(unittest.TestCase):
    def test_exact_verification_accepts_matching_answer(self):
        exercise = LearningExercise(
            "What is 2+2?",
            "4",
        )

        result = LearningVerification().check(
            exercise,
            "4",
            verification_type="EXACT",
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.reason, "ANSWER_CORRECT")

    def test_exact_verification_rejects_wrong_answer(self):
        exercise = LearningExercise(
            "What is 2+2?",
            "4",
        )

        result = LearningVerification().check(
            exercise,
            "5",
            verification_type="EXACT",
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "ANSWER_INCORRECT")

    def test_numerical_verification_accepts_close_value(self):
        exercise = LearningExercise(
            "Calculate exp(-1).",
            "0.367879",
        )

        result = LearningVerification().check(
            exercise,
            "0.3678791",
            verification_type="NUMERICAL",
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.reason, "ANSWER_CORRECT")

    def test_numerical_verification_rejects_wrong_value(self):
        exercise = LearningExercise(
            "Calculate exp(-1).",
            "0.367879",
        )

        result = LearningVerification().check(
            exercise,
            "0.5",
            verification_type="NUMERICAL",
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "ANSWER_INCORRECT")

    def test_invalid_verification_type_is_rejected(self):
        exercise = LearningExercise(
            "What is 2+2?",
            "4",
        )

        result = LearningVerification().check(
            exercise,
            "4",
            verification_type="UNKNOWN",
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "INVALID_VERIFICATION_TYPE")


if __name__ == "__main__":
    unittest.main()
