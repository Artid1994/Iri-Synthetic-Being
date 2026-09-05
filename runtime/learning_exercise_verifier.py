from __future__ import annotations

from dataclasses import dataclass
import math

from runtime.learning_exercise import LearningExercise


@dataclass(frozen=True)
class LearningExerciseVerificationResult:
    passed: bool
    reason: str


class LearningExerciseVerifier:
    SUPPORTED_TYPES = {
        "EXACT",
        "NUMERICAL",
    }

    def verify(
        self,
        exercise: LearningExercise | None,
        answer: str,
        *,
        expected_answer: str | None = None,
        verification_type: str | None = None,
        tolerance: float = 1e-6,
    ) -> LearningExerciseVerificationResult:
        if not isinstance(exercise, LearningExercise):
            return LearningExerciseVerificationResult(
                passed=False,
                reason="INVALID_EXERCISE",
            )

        actual_type = (
            verification_type
            if verification_type is not None
            else exercise.verification_type
        ).strip().upper()

        if actual_type not in self.SUPPORTED_TYPES:
            return LearningExerciseVerificationResult(
                passed=False,
                reason="INVALID_VERIFICATION_TYPE",
            )

        if expected_answer is None:
            expected_answer = exercise.expected_answer

        expected_answer = expected_answer.strip()
        answer = answer.strip()

        if not expected_answer:
            return LearningExerciseVerificationResult(
                passed=False,
                reason="INVALID_EXPECTED_ANSWER",
            )

        if actual_type == "EXACT":
            passed = answer == expected_answer

        else:
            try:
                expected = float(expected_answer)
                actual = float(answer)
            except (TypeError, ValueError):
                return LearningExerciseVerificationResult(
                    passed=False,
                    reason="INVALID_NUMERICAL_ANSWER",
                )

            if not math.isfinite(expected) or not math.isfinite(actual):
                return LearningExerciseVerificationResult(
                    passed=False,
                    reason="NON_FINITE_NUMERICAL_ANSWER",
                )

            if tolerance < 0:
                return LearningExerciseVerificationResult(
                    passed=False,
                    reason="INVALID_TOLERANCE",
                )

            passed = abs(actual - expected) <= tolerance

        return LearningExerciseVerificationResult(
            passed=passed,
            reason="ANSWER_CORRECT" if passed else "ANSWER_INCORRECT",
        )
