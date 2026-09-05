from __future__ import annotations

from runtime.learning_exercise_generation_result import (
    LearningExerciseGenerationResult,
)
from runtime.learning_exercise_retry_policy import (
    LearningExerciseRetryPolicy,
)


class LearningExerciseGenerationLoop:
    def __init__(
        self,
        generator,
        runner,
        max_attempts: int = 3,
    ) -> None:
        self.generator = generator
        self.runner = runner
        self.retry_policy = LearningExerciseRetryPolicy(
            max_attempts=max_attempts,
        )

    def run(
        self,
        knowledge: str,
        answer: str,
    ) -> LearningExerciseGenerationResult:
        for attempt in range(1, self.retry_policy.max_attempts + 1):
            try:
                spec = self.generator.generate(knowledge)
            except ValueError:
                if not self.retry_policy.can_retry(attempt):
                    return LearningExerciseGenerationResult(
                        accepted=False,
                        attempts=attempt,
                        reason="MAX_ATTEMPTS_REACHED",
                    )
                continue

            result = self.runner.run(spec, answer)

            if result.passed:
                return LearningExerciseGenerationResult(
                    accepted=True,
                    attempts=attempt,
                    reason=result.reason,
                )

            if not self.retry_policy.can_retry(attempt):
                return LearningExerciseGenerationResult(
                    accepted=False,
                    attempts=attempt,
                    reason="MAX_ATTEMPTS_REACHED",
                )

        return LearningExerciseGenerationResult(
            accepted=False,
            attempts=self.retry_policy.max_attempts,
            reason="MAX_ATTEMPTS_REACHED",
        )
