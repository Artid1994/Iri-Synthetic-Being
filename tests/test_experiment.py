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


if __name__ == "__main__":
    unittest.main()
