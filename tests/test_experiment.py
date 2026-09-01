import unittest
from pathlib import Path

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

    def test_research_summary_contains_key_results(self):
        from runtime.numerical_engine import NumericalEngine

        engine = NumericalEngine()

        experiment = Experiment(
            hypothesis="coherence decreases with coupling",
            parameters={
                "qubits": 1,
                "coupling_values": [0.0, 0.5, 1.0],
            },
            objective="compare models",
        )

        summary = engine.research_summary(experiment)

        self.assertEqual(
            summary["hypothesis"],
            experiment.hypothesis,
        )
        self.assertEqual(
            summary["objective"],
            experiment.objective,
        )
        self.assertEqual(
            summary["best_model"],
            "exponential",
        )
        self.assertIn("exponential_error", summary)
        self.assertIn("linear_error", summary)

    def test_reference_dynamics_produces_coherence_data(self):
        from runtime.numerical_engine import NumericalEngine

        engine = NumericalEngine()

        values = engine.reference_dynamics(
            qubits=1,
            coupling_values=[0.0, 0.5, 1.0],
        )

        self.assertEqual(len(values), 3)
        self.assertAlmostEqual(values[0], 1.0)
        self.assertGreater(values[0], values[1])
        self.assertGreater(values[1], values[2])

    def test_research_prompt_contains_summary_and_constraints(self):
        from runtime.research_prompt import ResearchPrompt

        summary = {
            "hypothesis": "coherence decreases with coupling",
            "objective": "compare models",
            "best_model": "exponential",
            "exponential_error": 0.021072,
            "linear_error": 0.277778,
        }

        prompt = ResearchPrompt.build(summary)

        self.assertIn(summary["hypothesis"], prompt)
        self.assertIn(summary["best_model"], prompt)
        self.assertIn("hypothesis", prompt.lower())
        self.assertIn("model", prompt.lower())
        self.assertIn("do not execute code", prompt.lower())

    def test_research_proposal_parses_ai_output(self):
        from runtime.research_proposal import ResearchProposal

        output = """Hypothesis: coherence decreases with coupling
Model Proposal: Exponential model"""

        proposal = ResearchProposal.parse(output)

        self.assertEqual(
            proposal.hypothesis,
            "coherence decreases with coupling",
        )
        self.assertEqual(
            proposal.model,
            "Exponential model",
        )

    def test_research_proposal_validates_allowed_model(self):
        from runtime.research_proposal import ResearchProposal

        proposal = ResearchProposal(
            hypothesis="coherence decreases with coupling",
            model="Exponential model",
        )

        self.assertTrue(proposal.is_supported_model())

        unsupported = ResearchProposal(
            hypothesis="test",
            model="Unknown model",
        )

        self.assertFalse(unsupported.is_supported_model())

    def test_research_proposal_dispatches_supported_model(self):
        from runtime.research_proposal import ResearchProposal

        exponential = ResearchProposal(
            hypothesis="test",
            model="Exponential model",
        )

        linear = ResearchProposal(
            hypothesis="test",
            model="Linear model",
        )

        unknown = ResearchProposal(
            hypothesis="test",
            model="Unknown model",
        )

        self.assertEqual(exponential.model_key(), "exponential")
        self.assertEqual(linear.model_key(), "linear")
        self.assertIsNone(unknown.model_key())

    def test_model_evaluation_rejects_unsupported_model(self):
        from runtime.numerical_engine import NumericalEngine
        from runtime.research_proposal import ResearchProposal

        engine = NumericalEngine()

        proposal = ResearchProposal(
            hypothesis="test",
            model="Unknown model",
        )

        result = engine.evaluate_model(
            proposal,
            coupling_values=[0.0, 0.5, 1.0],
        )

        self.assertEqual(result["status"], "REJECTED")

    def test_model_evaluation_calculates_selected_model_error(self):
        from runtime.numerical_engine import NumericalEngine
        from runtime.research_proposal import ResearchProposal

        engine = NumericalEngine()

        proposal = ResearchProposal(
            hypothesis="coherence decreases with coupling",
            model="Exponential model",
        )

        result = engine.evaluate_model(
            proposal,
            coupling_values=[0.0, 0.5, 1.0],
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["model"], "exponential")
        self.assertIn("error", result)

    def test_numerical_research_evaluates_ai_proposal(self):
        from runtime.numerical_research import NumericalResearch

        class FakeAI:
            def __call__(self, prompt):
                return (
                    "Hypothesis: coherence decreases with coupling\n"
                    "Model Proposal: Exponential model"
                )

        research = NumericalResearch(inference=FakeAI())

        result = research.run(
            coupling_values=[0.0, 0.5, 1.0],
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["model"], "exponential")
        self.assertIn("error", result)

    def test_experiment_history_records_completed_result(self):
        from runtime.experiment_history import ExperimentHistory

        history = ExperimentHistory()

        history.record(
            hypothesis="coherence decreases with coupling",
            model="exponential",
            parameters={"qubits": 1, "coupling": 0.5},
            metrics={"coherence": 0.857764},
            status="COMPLETED",
        )

        entries = history.entries()

        self.assertEqual(len(entries), 1)
        self.assertEqual(
            entries[0]["hypothesis"],
            "coherence decreases with coupling",
        )
        self.assertEqual(entries[0]["model"], "exponential")
        self.assertEqual(entries[0]["status"], "COMPLETED")

    def test_experiment_history_records_timestamp(self):
        from runtime.experiment_history import ExperimentHistory

        history = ExperimentHistory()

        history.record(
            hypothesis="test",
            model="exponential",
            parameters={"qubits": 1},
            metrics={"coherence": 1.0},
            status="COMPLETED",
        )

        entry = history.entries()[0]

        self.assertIn("timestamp", entry)
        self.assertIsInstance(entry["timestamp"], str)
        self.assertTrue(entry["timestamp"])

    def test_experiment_history_records_experiment_id(self):
        from runtime.experiment_history import ExperimentHistory

        history = ExperimentHistory()

        history.record(
            hypothesis="test",
            model="exponential",
            parameters={"qubits": 1},
            metrics={"coherence": 1.0},
            status="COMPLETED",
        )

        entry = history.entries()[0]

        self.assertIn("experiment_id", entry)
        self.assertIsInstance(entry["experiment_id"], str)
        self.assertTrue(entry["experiment_id"])

    def test_experiment_history_records_research_result(self):
        from runtime.experiment_history import ExperimentHistory

        history = ExperimentHistory()

        history.record_result(
            hypothesis="coherence decreases with coupling",
            model="exponential",
            parameters={"qubits": 1, "coupling_values": [0.0, 0.5, 1.0]},
            result={
                "status": "COMPLETED",
                "model": "exponential",
                "error": 0.021072181397545926,
            },
        )

        entry = history.entries()[0]

        self.assertEqual(entry["status"], "COMPLETED")
        self.assertEqual(entry["model"], "exponential")
        self.assertEqual(entry["metrics"]["error"], 0.021072181397545926)

    def test_numerical_research_records_history(self):
        from runtime.experiment_history import ExperimentHistory
        from runtime.numerical_research import NumericalResearch

        class FakeAI:
            def __call__(self, prompt):
                return (
                    "Hypothesis: coherence decreases with coupling\n"
                    "Model Proposal: Exponential model"
                )

        history = ExperimentHistory()
        research = NumericalResearch(
            inference=FakeAI(),
            history=history,
        )

        result = research.run(
            coupling_values=[0.0, 0.5, 1.0],
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(len(history.entries()), 1)
        self.assertEqual(
            history.entries()[0]["model"],
            "exponential",
        )

    def test_experiment_history_saves_and_loads(self):
        from tempfile import TemporaryDirectory
        from runtime.experiment_history import ExperimentHistory

        with TemporaryDirectory() as tmp:
            history = ExperimentHistory()

            history.record(
                hypothesis="test",
                model="exponential",
                parameters={"qubits": 1},
                metrics={"error": 0.1},
                status="COMPLETED",
            )

            path = Path(tmp) / "history.json"
            history.save(path)

            loaded = ExperimentHistory.load(path)

            self.assertEqual(len(loaded.entries()), 1)
            self.assertEqual(
                loaded.entries()[0]["model"],
                "exponential",
            )

    def test_numerical_research_history_contains_complete_cycle(self):
        from runtime.experiment_history import ExperimentHistory
        from runtime.numerical_research import NumericalResearch

        class FakeAI:
            def __call__(self, prompt):
                return (
                    "Hypothesis: coherence decreases with coupling\n"
                    "Model Proposal: Exponential model"
                )

        history = ExperimentHistory()
        research = NumericalResearch(
            inference=FakeAI(),
            history=history,
        )

        result = research.run(
            coupling_values=[0.0, 0.5, 1.0],
        )

        entry = history.entries()[0]

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(
            entry["hypothesis"],
            "coherence decreases with coupling",
        )
        self.assertEqual(entry["model"], "exponential")
        self.assertEqual(
            entry["parameters"]["coupling_values"],
            [0.0, 0.5, 1.0],
        )
        self.assertEqual(
            entry["metrics"]["error"],
            result["error"],
        )
        self.assertEqual(entry["status"], "COMPLETED")


if __name__ == "__main__":
    unittest.main()
