from __future__ import annotations

from runtime.numerical_engine import NumericalEngine
from runtime.research_prompt import ResearchPrompt
from runtime.research_proposal import ResearchProposal


class NumericalResearch:
    def __init__(self, inference) -> None:
        self.inference = inference
        self.engine = NumericalEngine()

    def run(self, coupling_values: list[float]) -> dict[str, object]:
        summary = self.engine.research_summary(
            self._base_experiment(coupling_values)
        )

        prompt = ResearchPrompt.build(summary)
        output = self.inference(prompt)
        proposal = ResearchProposal.parse(output)

        result = self.engine.evaluate_model(
            proposal,
            coupling_values=coupling_values,
        )

        return result

    @staticmethod
    def _base_experiment(coupling_values: list[float]):
        from runtime.experiment import Experiment

        return Experiment(
            hypothesis="coherence decreases with coupling",
            parameters={
                "qubits": 1,
                "coupling_values": coupling_values,
            },
            objective="compare models",
        )
