from __future__ import annotations

from dataclasses import dataclass

from runtime.action import Action
from runtime.action import ActionModule
from runtime.current_state import CurrentState
from runtime.current_state import CurrentStateModule
from runtime.perception import Perception
from runtime.perception import PerceptionModule


@dataclass(frozen=True)
class CognitiveCycle:
    input_text: str
    recalled: str
    reasoning: str
    decision: str
    experience_recorded: bool
    perception: Perception | None = None
    current_state: CurrentState | None = None
    action: Action | None = None


class CognitiveLoop:
    def __init__(
        self,
        cognitive,
        learning,
        personality,
        self_model,
        development,
    ) -> None:
        self.cognitive = cognitive
        self.learning = learning
        self.personality = personality
        self.self_model = self_model
        self.development = development

        self.perception = PerceptionModule()
        self.current_state = CurrentStateModule()
        self.action = ActionModule()

        self.last_cycle: CognitiveCycle | None = None

    def process(self, user_input: str) -> CognitiveCycle:
        perception = self.perception.process(user_input)

        current_state = self.current_state.capture(
            perception.normalized_input
        )

        if not perception.has_input:
            cycle = CognitiveCycle(
                input_text="",
                recalled="",
                reasoning="",
                decision="NO_ACTION",
                experience_recorded=False,
                perception=perception,
                current_state=current_state,
                action=self.action.execute("NO_ACTION"),
            )
            self.last_cycle = cycle
            return cycle

        if (
            self.last_cycle is not None
            and self.last_cycle.input_text == perception.normalized_input
        ):
            decision = "NO_ACTION"
        else:
            decision = self.cognitive.process(
                perception.normalized_input,
                record_experience=False,
            )

        action = self.action.execute(decision)

        experience_recorded = False

        if decision == "RESPOND":
            candidate = self.learning.create_candidate(
                perception.normalized_input,
                "GENERAL",
                1.0,
            )

            evaluation = self.learning.evaluate(candidate)
            experience_recorded = evaluation.accepted

            if evaluation.accepted and candidate is not None:
                self.personality.adapt(
                    openness_delta=0.1,
                    conscientiousness_delta=0.05,
                )

                self.self_model.update(
                    self_awareness_delta=0.1,
                    self_knowledge_delta=0.1,
                    history_entry=candidate.experience,
                )

                self.development.sync()

        cycle = CognitiveCycle(
            input_text=perception.normalized_input,
            recalled=perception.normalized_input,
            reasoning=perception.normalized_input,
            decision=decision,
            experience_recorded=experience_recorded,
            perception=perception,
            current_state=current_state,
            action=action,
        )

        self.last_cycle = cycle
        return cycle

    def snapshot(self) -> CognitiveCycle | None:
        if self.last_cycle is None:
            return None

        return CognitiveCycle(
            input_text=self.last_cycle.input_text,
            recalled=self.last_cycle.recalled,
            reasoning=self.last_cycle.reasoning,
            decision=self.last_cycle.decision,
            experience_recorded=self.last_cycle.experience_recorded,
            perception=self.perception.snapshot(
                self.last_cycle.perception
            ),
            current_state=self.current_state.snapshot(
                self.last_cycle.current_state
            ),
            action=self.action.snapshot(
                self.last_cycle.action
            ),
        )
