from __future__ import annotations

from runtime.learning_exercise_spec import LearningExerciseSpec
from runtime.learning_exercise_verifier import (
    LearningExerciseVerificationResult,
    LearningExerciseVerifier,
)
from runtime.learning_expression_evaluator import (
    LearningExpressionEvaluator,
)


class LearningExerciseRunner:
    def __init__(
        self,
        evaluator: LearningExpressionEvaluator | None = None,
        verifier: LearningExerciseVerifier | None = None,
    ) -> None:
        self.evaluator = evaluator or LearningExpressionEvaluator()
        self.verifier = verifier or LearningExerciseVerifier()

    def run(
        self,
        spec: LearningExerciseSpec | None,
        answer: str,
        tolerance: float = 1e-6,
    ) -> LearningExerciseVerificationResult:
        if not isinstance(spec, LearningExerciseSpec):
            return LearningExerciseVerificationResult(
                passed=False,
                reason="INVALID_EXERCISE",
            )

        try:
            expected = self.evaluator.evaluate(spec.expression)
        except ValueError:
            return LearningExerciseVerificationResult(
                passed=False,
                reason="INVALID_EXPRESSION",
            )

        from runtime.learning_exercise import LearningExercise

        exercise = LearningExercise(
            question=spec.question,
            expected_answer=str(expected),
            verification_type="NUMERICAL",
        )

        return self.verifier.verify(
            exercise,
            answer,
            tolerance=tolerance,
        )
