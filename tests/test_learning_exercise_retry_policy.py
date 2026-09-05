import unittest

from runtime.learning_exercise_retry_policy import (
    LearningExerciseRetryPolicy,
)


class TestLearningExerciseRetryPolicy(unittest.TestCase):

    def test_first_attempt_is_allowed(self):
        policy = LearningExerciseRetryPolicy(max_attempts=3)

        self.assertTrue(policy.can_retry(1))

    def test_last_allowed_attempt_is_allowed(self):
        policy = LearningExerciseRetryPolicy(max_attempts=3)

        self.assertTrue(policy.can_retry(2))

    def test_max_attempt_is_not_retryable(self):
        policy = LearningExerciseRetryPolicy(max_attempts=3)

        self.assertFalse(policy.can_retry(3))

    def test_attempt_above_max_is_not_retryable(self):
        policy = LearningExerciseRetryPolicy(max_attempts=3)

        self.assertFalse(policy.can_retry(4))

    def test_max_attempts_must_be_positive(self):
        with self.assertRaises(ValueError):
            LearningExerciseRetryPolicy(max_attempts=0)

    def test_attempt_must_be_positive(self):
        policy = LearningExerciseRetryPolicy(max_attempts=3)

        with self.assertRaises(ValueError):
            policy.can_retry(0)


if __name__ == "__main__":
    unittest.main()
