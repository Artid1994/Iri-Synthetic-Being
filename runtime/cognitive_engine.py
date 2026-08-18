from __future__ import annotations

from dataclasses import dataclass

from runtime.memory import Memory


@dataclass
class CognitiveState:
    recall_active: bool = False
    reasoning_active: bool = False
    decision_active: bool = False
    last_input: str = ""
    last_recalled: str = ""
    last_reasoning: str = ""
    last_decision: str = ""


class CognitiveEngine:
    def __init__(self, memory: Memory) -> None:
        self.state = CognitiveState()
        self.memory = memory

    def snapshot(self) -> CognitiveState:
        return CognitiveState(
            recall_active=self.state.recall_active,
            reasoning_active=self.state.reasoning_active,
            decision_active=self.state.decision_active,
            last_input=self.state.last_input,
            last_recalled=self.state.last_recalled,
            last_reasoning=self.state.last_reasoning,
            last_decision=self.state.last_decision,
        )

    def process(self, user_input: str, record_experience: bool = True) -> str:
        self.state.last_input = user_input

        self.state.recall_active = True
        recalled = self._recall(user_input)
        self.state.last_recalled = recalled

        self.state.reasoning_active = True
        reasoning = self._reason(recalled)
        self.state.last_reasoning = reasoning

        self.state.decision_active = True
        decision = self._decide(reasoning)

        self.state.last_decision = decision

        if decision == "RESPOND" and record_experience:
            self.memory.add_experience(user_input)

        self.state.recall_active = False
        self.state.reasoning_active = False
        self.state.decision_active = False

        return decision

    def _recall(self, user_input: str) -> str:
        user_input = user_input.strip()

        if not user_input:
            return ""

        return self.memory.recall(user_input)

    @staticmethod
    def _reason(recalled: str) -> str:
        return recalled

    @staticmethod
    def _decide(reasoning: str) -> str:
        if not reasoning:
            return "NO_ACTION"

        return "RESPOND"
