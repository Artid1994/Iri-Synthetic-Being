import unittest

from runtime.learning import Learning
from runtime.learning_exercise import LearningExercise
from runtime.learning_practice import LearningPractice
from runtime.memory import Memory


class TestLearningPracticeFeedback(unittest.TestCase):
    def test_correct_exercise_answer_can_be_learned(self):
        memory = Memory()
        learning = Learning(memory)
        exercise = LearningExercise(
            "2+2 = ?",
            "4",
        )

        practice = LearningPractice()
        result = practice.check(exercise, "4")

        learning_result = learning.learn_from_prediction(
            "2+2 = 4",
            type(
                "Evaluation",
                (),
                {
                    "correct": result.passed,
                    "reason": result.reason,
                },
            )(),
        )

        self.assertTrue(result.passed)
        self.assertTrue(learning_result.accepted)
        self.assertIn(
            "2+2 = 4",
            memory.state.episodic,
        )

    def test_incorrect_exercise_answer_is_not_learned(self):
        memory = Memory()
        learning = Learning(memory)
        exercise = LearningExercise(
            "2+2 = ?",
            "4",
        )

        practice = LearningPractice()
        result = practice.check(exercise, "5")

        learning_result = learning.learn_from_prediction(
            "2+2 = 5",
            type(
                "Evaluation",
                (),
                {
                    "correct": result.passed,
                    "reason": result.reason,
                },
            )(),
        )

        self.assertFalse(result.passed)
        self.assertFalse(learning_result.accepted)
        self.assertEqual(
            len(memory.state.episodic),
            0,
        )


if __name__ == "__main__":
    unittest.main()
