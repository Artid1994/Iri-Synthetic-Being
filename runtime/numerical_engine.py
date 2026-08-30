from __future__ import annotations

import numpy as np

from runtime.experiment import Experiment, ExperimentResult


class NumericalEngine:

    def compare_models(self, experiment: Experiment) -> dict[str, float | str]:
        values = experiment.parameters["coupling_values"]

        initial = self.run(
            Experiment(
                hypothesis=experiment.hypothesis,
                parameters={
                    "qubits": experiment.parameters.get("qubits", 1),
                    "coupling": 0.0,
                },
                objective=experiment.objective,
            )
        ).metrics["coherence"]

        exponential_error = 0.0
        linear_error = 0.0

        for coupling in values:
            actual = self.run(
                Experiment(
                    hypothesis=experiment.hypothesis,
                    parameters={
                        "qubits": experiment.parameters.get("qubits", 1),
                        "coupling": coupling,
                    },
                    objective=experiment.objective,
                )
            ).metrics["coherence"]

            exponential = initial * np.exp(-coupling)
            linear = initial * (1.0 - coupling)

            exponential_error += (actual - exponential) ** 2
            linear_error += (actual - linear) ** 2

        return {
            "exponential_error": float(exponential_error),
            "linear_error": float(linear_error),
            "best_model": (
                "exponential"
                if exponential_error <= linear_error
                else "linear"
            ),
        }

    def run(self, experiment: Experiment) -> ExperimentResult:
        try:
            qubits = int(experiment.parameters.get("qubits", 1))

            if qubits not in {1, 2}:
                return ExperimentResult(
                    metrics={},
                    status="REJECTED",
                    error="ONLY_1_OR_2_QUBITS_SUPPORTED",
                )

            size = 2**qubits
            coupling = float(experiment.parameters.get("coupling", 0.0))

            if coupling < 0.0:
                return ExperimentResult(
                    metrics={},
                    status="REJECTED",
                    error="COUPLING_MUST_BE_NON_NEGATIVE",
                )

            state = np.ones(size, dtype=complex) / np.sqrt(size)

            probabilities = np.abs(state) ** 2
            coherence = float(np.sum(np.abs(state)))
            coherence *= float(np.exp(-coupling))

            return ExperimentResult(
                metrics={
                    "state_size": float(size),
                    "probability_sum": float(np.sum(probabilities)),
                    "coherence": coherence,
                },
                status="COMPLETED",
            )

        except Exception as exc:
            return ExperimentResult(
                metrics={},
                status="ERROR",
                error=str(exc),
            )
