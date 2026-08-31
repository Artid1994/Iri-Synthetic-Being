from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchProposal:
    hypothesis: str
    model: str

    SUPPORTED_MODELS = {
        "exponential model",
        "linear model",
    }

    def is_supported_model(self) -> bool:
        return self.model.strip().lower() in self.SUPPORTED_MODELS

    def model_key(self) -> str | None:
        return {
            "exponential model": "exponential",
            "linear model": "linear",
        }.get(self.model.strip().lower())

    @classmethod
    def parse(cls, output: str) -> "ResearchProposal":
        hypothesis = ""
        model = ""

        for line in output.splitlines():
            key, separator, value = line.partition(":")

            if not separator:
                continue

            key = key.strip().lower()
            value = value.strip()

            if key == "hypothesis":
                hypothesis = value
            elif key == "model proposal":
                model = value

        if not hypothesis or not model:
            raise ValueError("INVALID_RESEARCH_PROPOSAL")

        return cls(
            hypothesis=hypothesis,
            model=model,
        )
