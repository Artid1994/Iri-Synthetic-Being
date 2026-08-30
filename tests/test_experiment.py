import unittest

from runtime.experiment import Experiment, ExperimentResult


class TestExperiment(unittest.TestCase):

    def test_experiment_contract(self):
        experiment = Experiment(
            hypothesis="decoherence increases with coupling",
            parameters={"coupling": 0.5},
            objective="measure coherence loss",
        )

        self.assertEqual(
            experiment.hypothesis,
            "decoherence increases with coupling",
        )
        self.assertEqual(
            experiment.parameters["coupling"],
            0.5,
        )
        self.assertEqual(
            experiment.objective,
            "measure coherence loss",
        )

    def test_experiment_result_contract(self):
        result = ExperimentResult(
            metrics={"coherence": 0.25},
            status="COMPLETED",
        )

        self.assertEqual(result.metrics["coherence"], 0.25)
        self.assertEqual(result.status, "COMPLETED")
        self.assertIsNone(result.error)

    def test_decoherence_reduces_coherence(self):
        from runtime.numerical_engine import NumericalEngine

        engine = NumericalEngine()

        low = engine.run(
            Experiment(
                hypothesis="test",
                parameters={"qubits": 1, "coupling": 0.0},
                objective="measure coherence",
            )
        )

        high = engine.run(
            Experiment(
                hypothesis="test",
                parameters={"qubits": 1, "coupling": 1.0},
                objective="measure coherence",
            )
        )

        self.assertGreater(
            low.metrics["coherence"],
            high.metrics["coherence"],
        )

    def test_model_comparison_returns_errors(self):
        from runtime.numerical_engine import NumericalEngine

        engine = NumericalEngine()

        result = engine.compare_models(
            Experiment(
                hypothesis="coherence decreases with coupling",
                parameters={
                    "qubits": 1,
                    "coupling_values": [0.0, 0.5, 1.0],
                },
                objective="compare models",
            )
        )

        self.assertIn("exponential_error", result)
        self.assertIn("linear_error", result)
        self.assertEqual(result["best_model"], "exponential")


if __name__ == "__main__":
    unittest.main()
