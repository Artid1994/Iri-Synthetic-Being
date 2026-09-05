import unittest

from runtime.learning_exercise_runner import (
    LearningExerciseRunner,
)
from runtime.learning_exercise_spec import LearningExerciseSpec


class TestLearningExerciseRunner(unittest.TestCase):

    def setUp(self):
        self.runner = LearningExerciseRunner()

    def test_correct_numerical_answer_passes(self):
        spec = LearningExerciseSpec(
            question="Calculate exp(-1).",
            expression="exp(-1)",
        )

        result = self.runner.run(spec, "0.36787944117144233")

        self.assertTrue(result.passed)
        self.assertEqual(result.reason, "ANSWER_CORRECT")

    def test_wrong_numerical_answer_fails(self):
        spec = LearningExerciseSpec(
            question="Calculate exp(-1).",
            expression="exp(-1)",
        )

        result = self.runner.run(spec, "0.5")

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "ANSWER_INCORRECT")

    def test_invalid_answer_fails(self):
        spec = LearningExerciseSpec(
            question="Calculate exp(-1).",
            expression="exp(-1)",
        )

        result = self.runner.run(spec, "not-a-number")

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "INVALID_NUMERICAL_ANSWER")

    def test_invalid_expression_is_rejected(self):
        spec = LearningExerciseSpec(
            question="Invalid exercise.",
            expression="sqrt(2)",
        )

        result = self.runner.run(spec, "1.41421356")

        self.assertFalse(result.passed)
        self.assertEqual(result.reason, "INVALID_EXPRESSION")


if __name__ == "__main__":
    unittest.main()
