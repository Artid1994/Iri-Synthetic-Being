from __future__ import annotations

from collections.abc import Callable


class GemmaCognitiveEngine:
    def __init__(self, inference: Callable[[str], str]) -> None:
        self._inference = inference

    def think(self, text: str, context: str = "") -> str:
        prompt = f"{context}\n{text}" if context else text
        return self._inference(prompt)

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
        }
