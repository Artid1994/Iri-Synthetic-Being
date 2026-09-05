import unittest

from runtime.learning_exercise_spec import LearningExerciseSpec
from runtime.learning_exercise_spec_generator import (
    LearningExerciseSpecGenerator,
)


class TestLearningExerciseSpecGenerator(unittest.TestCase):

    def test_generator_creates_spec_from_valid_ai_output(self):
        inference = lambda prompt: (
            "Question: Calculate exp(-1).\n"
            "Expression: exp(-1)"
        )

        generator = LearningExerciseSpecGenerator(inference)

        spec = generator.generate(
            "The exponential function is used in decay models."
        )

        self.assertIsInstance(spec, LearningExerciseSpec)
        self.assertEqual(
            spec.question,
            "Calculate exp(-1).",
        )
        self.assertEqual(
            spec.expression,
            "exp(-1)",
        )

    def test_generator_rejects_invalid_ai_output(self):
        inference = lambda prompt: "invalid output"

        generator = LearningExerciseSpecGenerator(inference)

        with self.assertRaises(ValueError):
            generator.generate(
                "The exponential function is used in decay models."
            )

    def test_generator_rejects_empty_knowledge(self):
        generator = LearningExerciseSpecGenerator(
            lambda prompt: (
                "Question: Calculate exp(-1).\n"
                "Expression: exp(-1)"
            )
        )

        with self.assertRaises(ValueError):
            generator.generate("")

    def test_generator_prompt_contains_knowledge(self):
        prompts = []

        def inference(prompt):
            prompts.append(prompt)
            return (
                "Question: Calculate exp(-1).\n"
                "Expression: exp(-1)"
            )

        generator = LearningExerciseSpecGenerator(inference)

        generator.generate(
            "The exponential function is used in decay models."
        )

        self.assertIn(
            "The exponential function is used in decay models.",
            prompts[0],
        )

    def test_generator_requires_expression(self):
        inference = lambda prompt: (
            "Question: Calculate exp(-1)."
        )

        generator = LearningExerciseSpecGenerator(inference)

        with self.assertRaises(ValueError):
            generator.generate(
                "The exponential function is used in decay models."
            )


if __name__ == "__main__":
    unittest.main()
