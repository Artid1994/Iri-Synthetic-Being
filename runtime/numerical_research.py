from __future__ import annotations

from runtime.experiment_history import ExperimentHistory
from runtime.numerical_engine import NumericalEngine
from runtime.research_prompt import ResearchPrompt
from runtime.research_proposal import ResearchProposal


class NumericalResearch:
    def __init__(self, inference, history: ExperimentHistory | None = None) -> None:
        self.inference = inference
        self.engine = NumericalEngine()
        self.history = history

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

        if self.history is not None and result["status"] == "COMPLETED":
            self.history.record_result(
                hypothesis=proposal.hypothesis,
                model=proposal.model_key() or "",
                parameters={
                    "qubits": 1,
                    "coupling_values": list(coupling_values),
                },
                result=result,
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
