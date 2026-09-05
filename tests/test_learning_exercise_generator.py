import unittest

from runtime.learning_exercise import LearningExercise
from runtime.learning_exercise_generator import LearningExerciseGenerator


class TestLearningExerciseGenerator(unittest.TestCase):
    def test_generator_creates_exercise_from_valid_ai_output(self):
        inference = lambda prompt: (
            "Question: What is 2+2?\n"
            "Expected Answer: 4\n"
            "Verification Type: EXACT"
        )

        generator = LearningExerciseGenerator(inference)

        exercise = generator.generate(
            "Addition combines quantities."
        )

        self.assertIsInstance(
            exercise,
            LearningExercise,
        )
        self.assertEqual(
            exercise.question,
            "What is 2+2?",
        )
        self.assertEqual(
            exercise.expected_answer,
            "4",
        )

    def test_generator_rejects_invalid_ai_output(self):
        inference = lambda prompt: "invalid output"

        generator = LearningExerciseGenerator(inference)

        with self.assertRaises(ValueError):
            generator.generate(
                "Addition combines quantities."
            )

    def test_generator_prompt_contains_knowledge(self):
        prompts = []

        def inference(prompt):
            prompts.append(prompt)
            return (
                "Question: What is 2+2?\n"
                "Expected Answer: 4\n"
            "Verification Type: EXACT"
            )

        generator = LearningExerciseGenerator(inference)

        generator.generate(
            "Addition combines quantities."
        )

        self.assertIn(
            "Addition combines quantities.",
            prompts[0],
        )


if __name__ == "__main__":
    unittest.main()
