"""
Attention and salience mechanism.

Determines what requires cognitive processing based on novelty,
relevance, and resource constraints.
"""
from dataclasses import dataclass
from typing import List, Optional
import time


@dataclass(frozen=True)
class SalienceSignal:
    """Immutable salience evaluation for a stimulus."""
    stimulus: str
    salience: float          # 0.0 to 1.0
    novelty: float          # 0.0 to 1.0
    relevance: float        # 0.0 to 1.0
    timestamp: float
    requires_cognition: bool

    def __post_init__(self):
        if not 0.0 <= self.salience <= 1.0:
            raise ValueError("salience must be in [0, 1]")
        if not 0.0 <= self.novelty <= 1.0:
            raise ValueError("novelty must be in [0, 1]")
        if not 0.0 <= self.relevance <= 1.0:
            raise ValueError("relevance must be in [0, 1]")


class AttentionMechanism:
    """
    Attention mechanism with novelty and relevance detection.

    Determines which stimuli require cognitive processing
    based on salience thresholds and resource constraints.
    """

    def __init__(
        self,
        novelty_threshold: float = 0.3,
        relevance_threshold: float = 0.4,
        salience_threshold: float = 0.5,
    ):
        if not 0.0 <= novelty_threshold <= 1.0:
            raise ValueError("novelty_threshold must be in [0, 1]")
        if not 0.0 <= relevance_threshold <= 1.0:
            raise ValueError("relevance_threshold must be in [0, 1]")
        if not 0.0 <= salience_threshold <= 1.0:
            raise ValueError("salience_threshold must be in [0, 1]")

        self.novelty_threshold = novelty_threshold
        self.relevance_threshold = relevance_threshold
        self.salience_threshold = salience_threshold

        # Track seen stimuli for novelty detection
        self._seen_stimuli: set = set()
        self._stimulus_counts: dict = {}

    def evaluate(
        self,
        stimulus: str,
        context: Optional[List[str]] = None,
    ) -> SalienceSignal:
        """
        Evaluate salience of a stimulus.

        Args:
            stimulus: Input stimulus
            context: Optional context for relevance evaluation

        Returns:
            SalienceSignal with evaluation results
        """
        stimulus = stimulus.strip()

        # Novelty: decreases with repetition
        if stimulus in self._stimulus_counts:
            self._stimulus_counts[stimulus] += 1
            novelty = max(0.0, 1.0 - (self._stimulus_counts[stimulus] - 1) * 0.2)
        else:
            self._stimulus_counts[stimulus] = 1
            novelty = 1.0

        self._seen_stimuli.add(stimulus)

        # Relevance: based on context overlap
        relevance = self._compute_relevance(stimulus, context)

        # Salience: weighted combination
        salience = (0.5 * novelty) + (0.5 * relevance)

        # Decision: does this require cognition?
        requires_cognition = (
            salience >= self.salience_threshold or
            novelty >= self.novelty_threshold or
            relevance >= self.relevance_threshold
        )

        return SalienceSignal(
            stimulus=stimulus,
            salience=salience,
            novelty=novelty,
            relevance=relevance,
            timestamp=time.time(),
            requires_cognition=requires_cognition,
        )

    def _compute_relevance(
        self,
        stimulus: str,
        context: Optional[List[str]],
    ) -> float:
        """Compute relevance based on context overlap."""
        if not context:
            return 0.5  # Neutral relevance

        # Simple word overlap measure
        stimulus_words = set(stimulus.lower().split())
        context_words = set()
        for ctx in context:
            context_words.update(ctx.lower().split())

        if not stimulus_words or not context_words:
            return 0.5

        overlap = len(stimulus_words & context_words)
        total = len(stimulus_words)

        return min(1.0, overlap / total) if total > 0 else 0.5

    def reset_novelty(self):
        """Reset novelty tracking (for testing or session reset)."""
        self._seen_stimuli.clear()
        self._stimulus_counts.clear()


class CognitiveTrigger:
    """
    Decides when to invoke the cognitive engine.

    Respects resource constraints and salience signals.
    """

    def __init__(
        self,
        attention: AttentionMechanism,
        max_cognitive_calls_per_minute: int = 60,
    ):
        self.attention = attention
        self.max_calls_per_minute = max_cognitive_calls_per_minute

        # Track cognitive invocations
        self._call_timestamps: List[float] = []

    def should_invoke_cognition(
        self,
        stimulus: str,
        context: Optional[List[str]] = None,
    ) -> tuple[bool, SalienceSignal]:
        """
        Determine if cognitive engine should be invoked.

        Args:
            stimulus: Input stimulus
            context: Optional context

        Returns:
            (should_invoke, salience_signal)
        """
        # Evaluate salience
        signal = self.attention.evaluate(stimulus, context)

        # Check resource budget
        now = time.time()
        self._prune_old_calls(now)

        if len(self._call_timestamps) >= self.max_calls_per_minute:
            # Budget exceeded, skip unless extremely salient
            return (signal.salience >= 0.9, signal)

        # Invoke if salient
        if signal.requires_cognition:
            self._call_timestamps.append(now)
            return (True, signal)

        return (False, signal)

    def _prune_old_calls(self, now: float):
        """Remove call timestamps older than 1 minute."""
        cutoff = now - 60.0
        self._call_timestamps = [
            ts for ts in self._call_timestamps if ts > cutoff
        ]

    def reset(self):
        """Reset cognitive trigger state."""
        self._call_timestamps.clear()
        self.attention.reset_novelty()
