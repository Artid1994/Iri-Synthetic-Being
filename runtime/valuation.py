"""
Valuation and reward mechanism.

Evaluates outcomes and produces learning signals.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RewardSignal:
    """Immutable reward evaluation."""
    outcome: str
    reward: float           # -1.0 to 1.0
    confidence: float       # 0.0 to 1.0
    reason: str

    def __post_init__(self):
        if not -1.0 <= self.reward <= 1.0:
            raise ValueError("reward must be in [-1, 1]")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")


class ValuationSystem:
    """
    Evaluates outcomes and produces reward signals.

    Provides learning feedback based on outcome assessment.
    """

    def __init__(self):
        # Track outcome history for adaptive valuation
        self._positive_outcomes = 0
        self._negative_outcomes = 0
        self._total_outcomes = 0

    def evaluate_outcome(
        self,
        outcome: str,
        expected: Optional[str] = None,
        goal_achieved: Optional[bool] = None,
    ) -> RewardSignal:
        """
        Evaluate an outcome and produce reward signal.

        Args:
            outcome: Actual outcome
            expected: Expected outcome (for prediction eval)
            goal_achieved: Explicit goal achievement signal

        Returns:
            RewardSignal with valuation
        """
        outcome = outcome.strip()

        # Determine reward
        if goal_achieved is not None:
            # Explicit goal achievement signal
            reward = 1.0 if goal_achieved else -0.5
            confidence = 0.9
            reason = "EXPLICIT_GOAL_SIGNAL"

        elif expected is not None:
            # Compare with prediction
            if outcome == expected:
                reward = 0.8
                confidence = 0.8
                reason = "PREDICTION_MATCHED"
            else:
                reward = -0.3
                confidence = 0.7
                reason = "PREDICTION_MISMATCH"

        elif self._is_positive_outcome(outcome):
            # Heuristic: contains positive indicators
            reward = 0.6
            confidence = 0.5
            reason = "POSITIVE_INDICATOR"

        elif self._is_negative_outcome(outcome):
            # Heuristic: contains negative indicators
            reward = -0.6
            confidence = 0.5
            reason = "NEGATIVE_INDICATOR"

        else:
            # Neutral outcome
            reward = 0.0
            confidence = 0.3
            reason = "NEUTRAL"

        # Update history
        self._total_outcomes += 1
        if reward > 0:
            self._positive_outcomes += 1
        elif reward < 0:
            self._negative_outcomes += 1

        return RewardSignal(
            outcome=outcome,
            reward=reward,
            confidence=confidence,
            reason=reason,
        )

    def _is_positive_outcome(self, outcome: str) -> bool:
        """Detect positive outcome indicators."""
        positive_words = {
            'success', 'correct', 'pass', 'good', 'excellent',
            'achieved', 'completed', 'solved', 'learned',
        }
        words = set(outcome.lower().split())
        return bool(words & positive_words)

    def _is_negative_outcome(self, outcome: str) -> bool:
        """Detect negative outcome indicators."""
        negative_words = {
            'fail', 'error', 'wrong', 'incorrect', 'bad',
            'failed', 'missed', 'rejected', 'blocked',
        }
        words = set(outcome.lower().split())
        return bool(words & negative_words)

    @property
    def positive_rate(self) -> float:
        """Fraction of positive outcomes."""
        if self._total_outcomes == 0:
            return 0.0
        return self._positive_outcomes / self._total_outcomes

    @property
    def negative_rate(self) -> float:
        """Fraction of negative outcomes."""
        if self._total_outcomes == 0:
            return 0.0
        return self._negative_outcomes / self._total_outcomes

    def reset(self):
        """Reset outcome history."""
        self._positive_outcomes = 0
        self._negative_outcomes = 0
        self._total_outcomes = 0
