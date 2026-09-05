import unittest

from runtime.learning_exercise import LearningExercise


class TestLearningExercise(unittest.TestCase):
    def test_exercise_requires_question(self):
        with self.assertRaises(ValueError):
            LearningExercise("", "4")

    def test_exercise_requires_expected_answer(self):
        with self.assertRaises(ValueError):
            LearningExercise("2+2 = ?", "")

    def test_correct_answer_passes(self):
        exercise = LearningExercise(
            "2+2 = ?",
            "4",
        )

        self.assertTrue(
            exercise.verify("4")
        )

    def test_incorrect_answer_fails(self):
        exercise = LearningExercise(
            "2+2 = ?",
            "4",
        )

        self.assertFalse(
            exercise.verify("5")
        )

    def test_answer_whitespace_is_ignored(self):
        exercise = LearningExercise(
            "2+2 = ?",
            "4",
        )

        self.assertTrue(
            exercise.verify(" 4 ")
        )


if __name__ == "__main__":
    unittest.main()
