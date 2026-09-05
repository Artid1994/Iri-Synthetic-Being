import unittest

from runtime.learning_exercise import LearningExercise
from runtime.learning_exercise_verifier import (
    LearningExerciseVerifier,
)


class TestLearningExerciseVerifier(unittest.TestCase):

    def setUp(self):
        self.verifier = LearningExerciseVerifier()

    def test_exact_answer_is_verified(self):
        exercise = LearningExercise(
            question="What is 2+2?",
            expected_answer="4",
            verification_type="EXACT",
        )

        result = self.verifier.verify(exercise, "4")

        self.assertTrue(result.passed)
        self.assertEqual(result.reason, "ANSWER_CORRECT")

    def test_exact_wrong_answer_is_rejected(self):
        exercise = LearningExercise(
            question="What is 2+2?",
            expected_answer="4",
            verification_type="EXACT",
        )

        result = self.verifier.verify(exercise, "5")

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "ANSWER_INCORRECT")

    def test_numerical_answer_uses_tolerance(self):
        exercise = LearningExercise(
            question="Calculate exp(-1).",
            expected_answer="0.36787944117",
            verification_type="NUMERICAL",
        )

        result = self.verifier.verify(
            exercise,
            "0.36787944120",
            tolerance=1e-9,
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.reason, "ANSWER_CORRECT")

    def test_numerical_wrong_answer_is_rejected(self):
        exercise = LearningExercise(
            question="Calculate exp(-1).",
            expected_answer="0.36787944117",
            verification_type="NUMERICAL",
        )

        result = self.verifier.verify(
            exercise,
            "0.5",
            tolerance=1e-6,
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "ANSWER_INCORRECT")

    def test_invalid_numerical_answer_is_rejected(self):
        exercise = LearningExercise(
            question="Calculate exp(-1).",
            expected_answer="0.36787944117",
            verification_type="NUMERICAL",
        )

        result = self.verifier.verify(
            exercise,
            "not-a-number",
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "INVALID_NUMERICAL_ANSWER")

    def test_non_finite_numerical_answer_is_rejected(self):
        exercise = LearningExercise(
            question="Calculate a value.",
            expected_answer="1.0",
            verification_type="NUMERICAL",
        )

        result = self.verifier.verify(
            exercise,
            "nan",
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "NON_FINITE_NUMERICAL_ANSWER")

    def test_invalid_exercise_is_rejected(self):
        result = self.verifier.verify(None, "4")

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "INVALID_EXERCISE")

    def test_invalid_tolerance_is_rejected(self):
        exercise = LearningExercise(
            question="Calculate exp(-1).",
            expected_answer="0.367879",
            verification_type="NUMERICAL",
        )

        result = self.verifier.verify(
            exercise,
            "0.367879",
            tolerance=-1.0,
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "INVALID_TOLERANCE")

    def test_external_expected_answer_can_override_exercise_answer(self):
        exercise = LearningExercise(
            question="What is 2+2?",
            expected_answer="5",
            verification_type="EXACT",
        )

        result = self.verifier.verify(
            exercise,
            "4",
            expected_answer="4",
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.reason, "ANSWER_CORRECT")


if __name__ == "__main__":
    unittest.main()
