from __future__ import annotations

from runtime.system_monitor import SystemMonitor
from runtime.identity import Identity
from runtime.memory import Memory
from runtime.internal_state import InternalStateManager
from runtime.personality import Personality
from runtime.self_model import SelfModel
from runtime.ae01m_cognitive_factory import create_cognitive_engine
from runtime.learning import Learning
from runtime.goal import Goal
from runtime.intention import Intention
from runtime.teaching import Teaching
from runtime.safety_policy import SafetyPolicy
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
from runtime.robot_adapter import RobotAdapter
from runtime.speech_output import SpeechOutput
from runtime.voice_conversation import VoiceConversation
from ttf_approval_gate import ActionState, ApprovalAction, ApprovalGate
from ttf_execution_adapter import ExecutionAdapter
from runtime.autonomous_policy_gate import AutonomousPolicyGate
from runtime.resource_guard import ResourceGuard
from runtime.auto_cooling import AutoCoolingController
from runtime.heartbeat import Heartbeat
from runtime.autonomous_loop import AutonomousLoopController


class TranscendingRuntime:
    def __init__(self, cognitive=None) -> None:
        self.system = SystemMonitor()
        self.identity = Identity()
        self.memory = Memory()
        self.safety_policy = SafetyPolicy()
        self.internal_state = InternalStateManager()
        self.personality = Personality()
        self.self_model = SelfModel()
        self.cognitive = cognitive or create_cognitive_engine(
            model_path="/home/artid1994/.local/share/ae01m/models/gemma-3-1b-it-Q4_K_M.gguf",
            executable="/home/artid1994/.local/src/ae01m-llama.cpp/build/bin/llama-completion",
        )
        self.learning = Learning(self.memory)
        self.goals: list[Goal] = []
        self.intentions: list[Intention] = []
        self.teachings: list[Teaching] = []
        self.prediction = Prediction()
        self.identity_continuity = IdentityContinuity()
        self.virtual_body = VirtualBody()
        self.embodiment = EmbodimentLoop(
            self.virtual_body,
            memory=self.memory,
        )
        self.autonomous_controller = AutonomousController(self.embodiment)
        self.approval_gate = ApprovalGate()
        self.pending_approval = None
        self.pending_command = None
        self.execution_adapter = ExecutionAdapter(self.approval_gate)
        self.autonomous_policy = AutonomousPolicyGate()
        self.autonomous_mode = False
        self.resource_guard = ResourceGuard()
        self.auto_cooling = AutoCoolingController()
        self.heartbeat = Heartbeat()
        self.autonomous_loop = None
        self._sync_safety_policy()
        self.robot_adapter = RobotAdapter()
        self.speech_output = SpeechOutput()
        self.voice_conversation = VoiceConversation(
            cognitive=self.cognitive,
            speech_output=self.speech_output,
        )
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
            self.prediction,
        )


    def enable_autonomous_mode(self) -> None:
        self.autonomous_mode = True
        self.autonomous_policy.enable()

    def disable_autonomous_mode(self) -> None:
        self.autonomous_mode = False
        self.autonomous_policy.disable()

    def run_autonomous_step(
        self,
        observation,
        memory_usage=0.0,
    ):
        if not self.autonomous_mode:
            return {
                "status": "BLOCKED",
                "reason": "AUTONOMOUS_MODE_DISABLED",
            }

        if self.autonomous_loop is None:
            self.autonomous_loop = AutonomousLoopController(
                self,
                self.resource_guard,
                self.auto_cooling,
                self.heartbeat,
            )

        return self.autonomous_loop.step(
            observation,
            memory_usage,
        )

    def add_goal(self, goal: Goal) -> None:
        if not isinstance(goal, Goal):
            raise TypeError("goal must be a Goal")

        self.goals.append(goal)

    def add_intention(self, intention: Intention) -> None:
        if not isinstance(intention, Intention):
            raise TypeError("intention must be an Intention")

        self.intentions.append(intention)

    def add_teaching(self, teaching: Teaching) -> None:
        if not isinstance(teaching, Teaching):
            raise TypeError("teaching must be a Teaching")

        self.teachings.append(teaching)

    def learn_teaching(self, teaching: Teaching):
        if not isinstance(teaching, Teaching):
            raise TypeError("teaching must be a Teaching")

        if teaching not in self.teachings:
            raise ValueError("teaching must be registered first")

        return self.learning.evaluate_teaching(teaching)

    def get_goal_for_intention(
        self,
        intention: Intention,
    ) -> Goal | None:
        if not isinstance(intention, Intention):
            raise TypeError("intention must be an Intention")

        if intention.goal_id is None:
            return None

        for goal in self.goals:
            if goal.id == intention.goal_id:
                return goal

        return None

    def _sync_safety_policy(self) -> None:
        for event in self.memory.state.safety_events:
            self.safety_policy.observe(event)

    def speak(self, text: str) -> bool:
        return self.speech_output.speak(text)

    def voice_respond(self, audio):
        return self.voice_conversation.respond(audio)

    def autonomous_step(self, observation):
        cycle = self.cognitive_loop.process(
            observation
        )

        command = self.autonomous_controller.decide(
            cycle
        )

        if command is None:
            return {
                "observation": observation,
                "reasoning": cycle.reasoning,
                "decision": cycle.decision,
                "command": None,
                "feedback": None,
                "evaluation": None,
                "learning": None,
            }

        approval = self.propose_action(command)

        if approval is None:
            return {
                "observation": observation,
                "reasoning": cycle.reasoning,
                "decision": cycle.decision,
                "command": command,
                "approval": None,
                "feedback": None,
                "evaluation": None,
                "learning": None,
            }

        return {
            "observation": observation,
            "reasoning": cycle.reasoning,
            "decision": cycle.decision,
            "command": command,
            "approval": approval,
            "feedback": None,
            "evaluation": None,
            "learning": None,
        }

    def propose_action(self, command):
        if command is None:
            return None
        action = ApprovalAction(action_type=command.action, path="")
        if not self.approval_gate.validate(action):
            return None
        self.pending_approval = action
        self.pending_command = command
        return action

    def approve_pending_action(self):
        if self.pending_approval is None:
            return False

        if self.autonomous_mode:
            decision = self.autonomous_policy.evaluate(
                self.pending_command
            )

            if not decision.allowed:
                return False

            self.pending_approval.human_approval = True
            self.pending_approval.state = ActionState.APPROVED
            return True

        return self.approval_gate.approve(
            self.pending_approval
        )

    def reject_pending_action(self):
        if self.pending_approval is None:
            return False
        return self.approval_gate.reject(self.pending_approval)

    def execute_pending_action(self):
        if self.pending_approval is None or self.pending_command is None:
            return None

        if not self.approval_gate.authorize_execution(
            self.pending_approval
        ):
            return None

        result = self.execution_adapter.execute(
            self.pending_approval,
            lambda action: self.robot_adapter.execute(
                self.pending_command
            ),
        )

        self.pending_approval = None
        self.pending_command = None

        return result

    def complete_pending_action(self):
        command = self.pending_command
        if command is None:
            return None
        result = self.execute_pending_action()
        if result is None:
            return None
        success, execution = result
        from runtime.robot_feedback import RobotFeedback
        return RobotFeedback(
            success=execution.success,
            action=execution.action,
            value=execution.value,
            error=execution.error,
        )

    def act(self, command):
        if not self.autonomous_controller.allowed(command):
            self._sync_safety_policy()
            return None

        safety = self.embodiment.safety_check(command)

        if not safety.allowed:
            self._sync_safety_policy()
            return None

        policy_decision = self.safety_policy.evaluate_command(
            command
        )

        if policy_decision.blocked:
            return None

        learned_policy_decision = (
            self.safety_policy.evaluate_learned_action(command)
        )

        if learned_policy_decision.blocked:
            return None

        result = self.robot_adapter.execute(command)

        from runtime.robot_feedback import RobotFeedback

        return RobotFeedback(
            success=result.success,
            action=result.action,
            value=result.value,
            error=result.error,
        )

    def complete_approved_cycle(self):
        feedback = self.complete_pending_action()
        if feedback is None:
            return None
        evaluation = self.process_feedback(feedback)
        return feedback, evaluation

    def process_feedback(self, feedback):
        if feedback is None:
            return None

        from runtime.robot_feedback import RobotFeedback

        if not isinstance(feedback, RobotFeedback):
            return None

        evaluation = self.prediction.evaluate(
            str(feedback.value)
        )

        prediction = self.prediction.state.last_prediction

        if prediction is None:
            return evaluation

        self.learning.learn_from_prediction(
            prediction,
            evaluation,
        )

        return evaluation

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

        self.memory.add_experience_object(
            experience
        )

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

    def serialize(self) -> dict:
        return {
            "goals": [
                {
                    "id": goal.id,
                    "description": goal.description,
                    "priority": goal.priority,
                    "status": goal.status,
                }
                for goal in self.goals
            ],
            "intentions": [
                {
                    "id": intention.id,
                    "description": intention.description,
                    "status": intention.status,
                    "goal_id": intention.goal_id,
                }
                for intention in self.intentions
            ],
            "teachings": [
                {
                    "id": teaching.id,
                    "content": teaching.content,
                    "status": teaching.status,
                }
                for teaching in self.teachings
            ],
        }

    def restore(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        self.goals = [
            Goal(
                id=item["id"],
                description=item["description"],
                priority=item["priority"],
                status=item["status"],
            )
            for item in data.get("goals", [])
        ]

        self.intentions = [
            Intention(
                id=item["id"],
                description=item["description"],
                status=item["status"],
                goal_id=item.get("goal_id"),
            )
            for item in data.get("intentions", [])
        ]

        self.teachings = [
            Teaching(
                id=item["id"],
                content=item["content"],
                status=item["status"],
            )
            for item in data.get("teachings", [])
        ]

        safety_policy = data.get("safety_policy")
        if isinstance(safety_policy, dict):
            self.safety_policy.restore(safety_policy)

    def snapshot(self) -> dict:
        return {
            "system": self.system.snapshot(),
            "identity": self.identity.snapshot(),
            "memory": self.memory.snapshot(),
            "internal_state": self.internal_state.snapshot(),
            "personality": self.personality.snapshot(),
            "self_model": self.self_model.snapshot(),
            "goals": list(self.goals),
            "intentions": list(self.intentions),
            "teachings": list(self.teachings),
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
            "safety_policy": self.safety_policy.persistence_snapshot(),
        }
