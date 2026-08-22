from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionState:
    prediction_count: int = 0
    last_prediction: str | None = None


@dataclass(frozen=True)
class PredictionEvaluation:
    correct: bool | None
    reason: str


class Prediction:
    def __init__(self) -> None:
        self.state = PredictionState()

    def record(self, prediction: str) -> None:
        prediction = prediction.strip()

        if not prediction:
            return

        self.state = PredictionState(
            prediction_count=self.state.prediction_count + 1,
            last_prediction=prediction,
        )

    def evaluate(self, outcome: str) -> PredictionEvaluation:
        outcome = outcome.strip()

        if not self.state.last_prediction:
            return PredictionEvaluation(
                correct=None,
                reason="NO_PREDICTION",
            )

        if self.state.last_prediction == outcome:
            return PredictionEvaluation(
                correct=True,
                reason="PREDICTION_MATCHED_OUTCOME",
            )

        return PredictionEvaluation(
            correct=False,
            reason="PREDICTION_DID_NOT_MATCH_OUTCOME",
        )

    def snapshot(self) -> PredictionState:
        return PredictionState(
            prediction_count=self.state.prediction_count,
            last_prediction=self.state.last_prediction,
        )
