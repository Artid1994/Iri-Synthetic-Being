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
from runtime.virtual_body import VirtualBody
from runtime.embodiment import EmbodimentLoop
from runtime.autonomous_controller import AutonomousController
from runtime.human_data import HumanData
from runtime.memory_processing import MemoryProcessor
from runtime.identity_representation import IdentityRepresentation
from runtime.cognitive_loop import CognitiveLoop
from runtime.experience import Experience
from runtime.sensor_source import MockSensor


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
        self.virtual_body = VirtualBody()
        self.embodiment = EmbodimentLoop(self.virtual_body)
        self.autonomous_controller = AutonomousController(self.embodiment)
        self.human_data = HumanData()
        self.memory_processor = MemoryProcessor()
        self.identity_representation = IdentityRepresentation()
        self.camera = MockSensor("camera", "")
        self.microphone = MockSensor("microphone", "")
        self.last_experience: Experience | None = None

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


    def process_sensor(
        self,
        sensor: str,
        value: object,
        timestamp: float,
        modality: str,
    ) -> bool:
        if sensor == "camera":
            source = self.camera
        elif sensor == "microphone":
            source = self.microphone
        else:
            return False

        source.value = value
        reading = source.read(timestamp)

        perception = self.cognitive_loop.perception.process(
            str(reading.value)
        )

        if not perception.has_input:
            return False

        experience = Experience(
            source=reading.sensor,
            content=perception.normalized_input,
            timestamp=reading.timestamp,
            modality=modality,
        )

        self.last_experience = experience

        self.cognitive_loop.process(
            experience.content
        )

        return True

    def import_human_data(self, data: HumanData) -> None:
        structured = self.memory_processor.process(data)

        self.memory.import_structured(structured)
        self.human_data = data
        self.identity_representation = (
            IdentityRepresentation.from_structured_memory(structured)
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
            "virtual_body": self.virtual_body.snapshot(),
            "embodiment": self.embodiment.observe(),
            "human_data": self.human_data,
            "identity_representation": self.identity_representation,
            "development": self.development.assess(),
            "development_history": self.development.history_snapshot(),
        }
