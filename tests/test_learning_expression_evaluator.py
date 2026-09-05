import unittest

from runtime.learning_expression_evaluator import (
    LearningExpressionEvaluator,
)


class TestLearningExpressionEvaluator(unittest.TestCase):

    def setUp(self):
        self.evaluator = LearningExpressionEvaluator()

    def test_evaluates_exponential(self):
        result = self.evaluator.evaluate("exp(-1)")

        self.assertAlmostEqual(
            result,
            0.36787944117144233,
        )

    def test_evaluates_integer(self):
        result = self.evaluator.evaluate("2")

        self.assertEqual(result, 2.0)

    def test_evaluates_division(self):
        result = self.evaluator.evaluate("1 / 2")

        self.assertEqual(result, 0.5)

    def test_rejects_unknown_function(self):
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("sqrt(2)")

    def test_rejects_python_code(self):
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("__import__('os').system('id')")

    def test_rejects_empty_expression(self):
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("")


if __name__ == "__main__":
    unittest.main()
