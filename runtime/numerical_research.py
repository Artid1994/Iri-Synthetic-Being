from __future__ import annotations

from runtime.experiment_history import ExperimentHistory
from runtime.numerical_engine import NumericalEngine
from runtime.research_prompt import ResearchPrompt
from runtime.research_proposal import ResearchProposal


class NumericalResearch:
    def __init__(self, history: ExperimentHistory | None = None) -> None:
        self.engine = NumericalEngine()
        self.history = history

    def run(
        self,
        coupling_values: list[float],
        previous_result: dict[str, object] | None = None,
    ) -> dict[str, object]:
        # Systematic model search without LLM
        # Try exponential model (most common for decay/coherence)

        result = self.engine.search_exponential_rate(
            coupling_values=coupling_values,
            rates=[0.5, 0.75, 1.0, 1.25, 1.5],
        )

        # Default hypothesis for history recording
        hypothesis = "coherence decreases with coupling"
        model = "exponential"

        if self.history is not None and result["status"] == "COMPLETED":
            self.history.record_result(
                hypothesis=hypothesis,
                model=model,
                parameters={
                    "qubits": 1,
                    "coupling_values": list(coupling_values),
                    **(
                        {"rate": result["rate"]}
                        if "rate" in result
                        else {}
                    ),
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
