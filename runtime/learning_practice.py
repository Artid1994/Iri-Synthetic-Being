from __future__ import annotations

from dataclasses import dataclass

from runtime.learning_exercise import LearningExercise
from runtime.prediction import PredictionEvaluation


@dataclass(frozen=True)
class LearningPracticeResult:
    evaluation: PredictionEvaluation

    @property
    def passed(self) -> bool:
        return self.evaluation.correct is True

    @property
    def reason(self) -> str:
        return self.evaluation.reason


class LearningPractice:
    def check(
        self,
        exercise: LearningExercise | None,
        answer: str,
    ) -> LearningPracticeResult:
        if not isinstance(exercise, LearningExercise):
            return LearningPracticeResult(
                evaluation=PredictionEvaluation(
                    correct=None,
                    reason="INVALID_EXERCISE",
                )
            )

        if exercise.verify(answer):
            evaluation = PredictionEvaluation(
                correct=True,
                reason="ANSWER_CORRECT",
            )
        else:
            evaluation = PredictionEvaluation(
                correct=False,
                reason="ANSWER_INCORRECT",
            )

        return LearningPracticeResult(
            evaluation=evaluation,
        )
