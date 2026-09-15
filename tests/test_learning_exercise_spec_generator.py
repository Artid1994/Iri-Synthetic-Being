import unittest

from runtime.learning_exercise_spec_generator import LearningExerciseSpecGenerator
from runtime.learning_exercise_spec import LearningExerciseSpec


class TestLearningExerciseSpecGenerator(unittest.TestCase):
    def test_generator_creates_spec_from_knowledge(self):
        # Generator now uses template-based generation
        generator = LearningExerciseSpecGenerator()

        spec = generator.generate("Calculate 15 plus 25")

        self.assertIsInstance(spec, LearningExerciseSpec)
        self.assertTrue(spec.question)
        self.assertTrue(spec.expression)

    def test_generator_extracts_numbers_for_arithmetic(self):
        generator = LearningExerciseSpecGenerator()

        spec = generator.generate("The numbers 7 and 8")

        self.assertEqual(spec.question, "Calculate: 7 + 8")
        self.assertEqual(spec.expression, "7 + 8")

    def test_generator_provides_default_exercise(self):
        generator = LearningExerciseSpecGenerator()

        spec = generator.generate("no numbers here")

        self.assertEqual(spec.question, "Calculate: 2 + 2")
        self.assertEqual(spec.expression, "2 + 2")

    def test_generator_rejects_empty_knowledge(self):
        generator = LearningExerciseSpecGenerator()

        with self.assertRaises(ValueError) as context:
            generator.generate("")

        self.assertEqual(
            str(context.exception),
            "KNOWLEDGE_CANNOT_BE_EMPTY",
        )


if __name__ == "__main__":
    unittest.main()
