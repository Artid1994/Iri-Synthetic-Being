from __future__ import annotations


class LearningExerciseRetryPolicy:
    def __init__(self, max_attempts: int = 3) -> None:
        if max_attempts <= 0:
            raise ValueError(
                "Learning exercise max attempts must be positive"
            )

        self.max_attempts = max_attempts

    def can_retry(self, attempt: int) -> bool:
        if attempt <= 0:
            raise ValueError(
                "Learning exercise attempt must be positive"
            )

        return attempt < self.max_attempts
