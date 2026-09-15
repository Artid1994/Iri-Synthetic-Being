import unittest

from runtime.learning_exercise_generator import LearningExerciseGenerator
from runtime.learning_exercise import LearningExercise


class TestLearningExerciseGenerator(unittest.TestCase):
    def test_generator_creates_exercise_from_knowledge(self):
        # Generator now uses template-based generation
        generator = LearningExerciseGenerator()

        exercise = generator.generate("Python sum of 5 and 3")

        self.assertIsInstance(exercise, LearningExercise)
        self.assertTrue(exercise.question)
        self.assertTrue(exercise.expected_answer)
        self.assertIn(exercise.verification_type, {"EXACT", "NUMERICAL"})

    def test_generator_extracts_numbers_for_numerical_exercises(self):
        generator = LearningExerciseGenerator()

        exercise = generator.generate("The values are 10 and 20")

        self.assertEqual(exercise.verification_type, "NUMERICAL")
        self.assertEqual(exercise.expected_answer, "30")

    def test_generator_creates_text_exercises_without_numbers(self):
        generator = LearningExerciseGenerator()

        exercise = generator.generate("Python is a programming language")

        self.assertEqual(exercise.verification_type, "EXACT")
        self.assertTrue(exercise.question)
        self.assertTrue(exercise.expected_answer)

    def test_generator_rejects_empty_knowledge(self):
        generator = LearningExerciseGenerator()

        with self.assertRaises(ValueError) as context:
            generator.generate("")

        self.assertEqual(
            str(context.exception),
            "KNOWLEDGE_CANNOT_BE_EMPTY",
        )


if __name__ == "__main__":
    unittest.main()
