from __future__ import annotations

from runtime.system_monitor import SystemMonitor
from runtime.identity import Identity
from runtime.memory import Memory
from runtime.internal_state import InternalStateManager
from runtime.personality import Personality
from runtime.self_model import SelfModel
from runtime.cognitive_engine import CognitiveEngine
from runtime.learning import Learning
from runtime.development import Development
from runtime.prediction import Prediction
from runtime.identity_continuity import IdentityContinuity
from runtime.cognitive_loop import CognitiveLoop


class TranscendingRuntime:
    def __init__(self) -> None:
        self.system = SystemMonitor()
        self.identity = Identity()
        self.memory = Memory()
        self.internal_state = InternalStateManager()
        self.personality = Personality()
        self.self_model = SelfModel()
        self.cognitive = CognitiveEngine(self.memory)
        self.learning = Learning(self.memory)
        self.prediction = Prediction()
        self.identity_continuity = IdentityContinuity()

        self.development = Development(
            self.identity,
            self.memory,
            self.learning,
            self.personality,
            self.self_model,
            self.prediction,
            self.identity_continuity,
        )

        self.cognitive_loop = CognitiveLoop(
            self.cognitive,
            self.learning,
            self.personality,
            self.self_model,
            self.development,
        )


    def snapshot(self) -> dict:
        return {
            "system": self.system.snapshot(),
            "identity": self.identity.snapshot(),
            "memory": self.memory.snapshot(),
            "internal_state": self.internal_state.snapshot(),
            "personality": self.personality.snapshot(),
            "self_model": self.self_model.snapshot(),
            "cognitive": self.cognitive.snapshot(),
            "cognitive_loop": self.cognitive_loop.snapshot(),
            "learning": self.learning.snapshot(),
            "prediction": self.prediction.snapshot(),
            "identity_continuity": self.identity_continuity.snapshot(),
            "development": self.development.assess(),
            "development_history": self.development.history_snapshot(),
        }
