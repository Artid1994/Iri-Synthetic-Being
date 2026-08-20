from __future__ import annotations

from collections.abc import Callable


class GemmaCognitiveEngine:
    def __init__(self, inference: Callable[[str], str]) -> None:
        self._inference = inference
        self.last_thought = ""

    def think(self, text: str, context: str = "") -> str:
        prompt = f"{context}\n{text}" if context else text
        thought = self._inference(prompt)
        self.last_thought = thought
        return thought

    def process(
        self,
        user_input: str,
        record_experience: bool = True,
    ) -> str:
        thought = self.think(user_input)

        if not thought:
            return "NO_ACTION"

        return "RESPOND"

    def snapshot(self) -> dict:
        return {
            "engine": "GemmaCognitiveEngine",
            "last_thought": self.last_thought,
        }
