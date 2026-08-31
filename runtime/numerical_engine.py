from __future__ import annotations

import numpy as np

from runtime.experiment import Experiment, ExperimentResult


class NumericalEngine:

    def evaluate_model(
        self,
        proposal,
        coupling_values: list[float],
    ) -> dict[str, object]:
        if not proposal.is_supported_model():
            return {
                "status": "REJECTED",
                "error": "UNSUPPORTED_MODEL",
            }

        model = proposal.model_key()
        actual_values = self.reference_dynamics(
            qubits=1,
            coupling_values=coupling_values,
        )

        initial = actual_values[0]
        error = 0.0

        for coupling, actual in zip(coupling_values, actual_values):
            if model == "exponential":
                predicted = initial * np.exp(-coupling)
            elif model == "linear":
                predicted = initial * (1.0 - coupling)
            else:
                return {
                    "status": "REJECTED",
                    "error": "UNSUPPORTED_MODEL",
                }

            error += (actual - predicted) ** 2

        return {
            "status": "COMPLETED",
            "model": model,
            "error": float(error),
        }

    def reference_dynamics(
        self,
        qubits: int,
        coupling_values: list[float],
    ) -> list[float]:
        if qubits not in {1, 2}:
            raise ValueError("ONLY_1_OR_2_QUBITS_SUPPORTED")

        size = 2**qubits
        values = []

        for coupling in coupling_values:
            if coupling < 0.0:
                raise ValueError("COUPLING_MUST_BE_NON_NEGATIVE")

            state = np.ones(size, dtype=complex) / np.sqrt(size)

            damping = 1.0 / (1.0 + coupling)
            state *= np.sqrt(damping)

            density = np.outer(state, np.conjugate(state))
            coherence = float(
                np.sum(np.abs(density))
                - np.sum(np.abs(np.diag(density)))
            )

            values.append(coherence)

        return values

    def compare_models(self, experiment: Experiment) -> dict[str, float | str]:
        values = experiment.parameters["coupling_values"]
        qubits = int(experiment.parameters.get("qubits", 1))

        actual_values = self.reference_dynamics(
            qubits=qubits,
            coupling_values=values,
        )

        initial = actual_values[0]

        exponential_error = 0.0
        linear_error = 0.0

        for coupling, actual in zip(values, actual_values):
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

    def research_summary(self, experiment: Experiment) -> dict:
        comparison = self.compare_models(experiment)

        return {
            "hypothesis": experiment.hypothesis,
            "objective": experiment.objective,
            "best_model": comparison["best_model"],
            "exponential_error": comparison["exponential_error"],
            "linear_error": comparison["linear_error"],
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
