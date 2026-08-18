from __future__ import annotations

from collections.abc import Callable


class GemmaCognitiveEngine:
    def __init__(self, inference: Callable[[str], str]) -> None:
        self._inference = inference

    def think(self, text: str, context: str = "") -> str:
        prompt = f"{context}\n{text}" if context else text
        return self._inference(prompt)
