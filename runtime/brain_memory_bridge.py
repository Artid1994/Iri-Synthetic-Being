from __future__ import annotations

from typing import Any

import numpy as np

from brain.brain import Brain
from runtime.memory import Memory


class BrainMemoryBridge:
    """Narrow, snapshot-only boundary between Brain and Memory."""

    def __init__(self, brain: Brain, memory: Memory) -> None:
        if not isinstance(brain, Brain):
            raise TypeError("brain must be a Brain")
        if not isinstance(memory, Memory):
            raise TypeError("memory must be a Memory")
        self._brain = brain
        self._memory = memory

    def neural_state_snapshot(self) -> dict[str, Any] | None:
        state = self._brain.neural_state_snapshot()
        if state is None:
            return None
        return {
            key: value.copy() if isinstance(value, np.ndarray) else value
            for key, value in state.items()
        }

    def memory_activity_snapshot(self) -> dict[str, list]:
        activity = self._memory.memory_activity_snapshot()
        return {
            "nodes": list(activity["nodes"]),
            "edges": [list(edge) for edge in activity["edges"]],
        }
