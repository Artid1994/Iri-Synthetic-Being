import unittest

from runtime.learning_exercise_spec import LearningExerciseSpec


class TestLearningExerciseSpec(unittest.TestCase):

    def test_valid_spec(self):
        spec = LearningExerciseSpec(
            question="Calculate exp(-1).",
            expression="exp(-1)",
        )

        self.assertEqual(spec.question, "Calculate exp(-1).")
        self.assertEqual(spec.expression, "exp(-1)")

    def test_empty_question_is_rejected(self):
        with self.assertRaises(ValueError):
            LearningExerciseSpec(
                question="",
                expression="exp(-1)",
            )

    def test_empty_expression_is_rejected(self):
        with self.assertRaises(ValueError):
            LearningExerciseSpec(
                question="Calculate exp(-1).",
                expression="",
            )


if __name__ == "__main__":
    unittest.main()


class TestLearningExerciseSpecValidation(unittest.TestCase):

    def test_incomplete_expression_is_rejected(self):
        with self.assertRaises(ValueError):
            LearningExerciseSpec(
                question="What is the exponential function?",
                expression=r"\( y",
            )

    def test_latex_expression_is_rejected(self):
        with self.assertRaises(ValueError):
            LearningExerciseSpec(
                question="Calculate the decay.",
                expression=r"y = e^{-x}",
            )
