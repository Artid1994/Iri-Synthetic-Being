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

    def test_numerical_research_records_multiple_cycles(self):
        from runtime.experiment_history import ExperimentHistory
        from runtime.numerical_research import NumericalResearch

        class FakeAI:
            def __init__(self):
                self.calls = 0

            def __call__(self, prompt):
                self.calls += 1
                model = "Exponential model" if self.calls == 1 else "Linear model"
                return (
                    "Hypothesis: coherence decreases with coupling\n"
                    f"Model Proposal: {model}"
                )

        history = ExperimentHistory()
        research = NumericalResearch(
            inference=FakeAI(),
            history=history,
        )

        research.run(coupling_values=[0.0, 0.5, 1.0])
        research.run(coupling_values=[0.0, 0.25, 0.5])

        entries = history.entries()

        self.assertEqual(len(entries), 2)
        self.assertNotEqual(
            entries[0]["experiment_id"],
            entries[1]["experiment_id"],
        )
        self.assertEqual(entries[0]["model"], "exponential")
        self.assertEqual(entries[1]["model"], "linear")

    def test_experiment_history_preserves_multiple_cycles_after_load(self):
        from tempfile import TemporaryDirectory
        from runtime.experiment_history import ExperimentHistory

        with TemporaryDirectory() as tmp:
            history = ExperimentHistory()

            history.record(
                hypothesis="test one",
                model="exponential",
                parameters={"coupling": [0.0, 0.5]},
                metrics={"error": 0.1},
                status="COMPLETED",
            )
            history.record(
                hypothesis="test two",
                model="linear",
                parameters={"coupling": [0.0, 1.0]},
                metrics={"error": 0.2},
                status="COMPLETED",
            )

            path = Path(tmp) / "history.json"
            history.save(path)

            loaded = ExperimentHistory.load(path)
            entries = loaded.entries()

            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0]["hypothesis"], "test one")
            self.assertEqual(entries[1]["hypothesis"], "test two")
            self.assertEqual(entries[0]["model"], "exponential")
            self.assertEqual(entries[1]["model"], "linear")
            self.assertEqual(entries[0]["metrics"]["error"], 0.1)
            self.assertEqual(entries[1]["metrics"]["error"], 0.2)
            self.assertNotEqual(
                entries[0]["experiment_id"],
                entries[1]["experiment_id"],
            )

    def test_numerical_research_does_not_record_failed_proposal(self):
        from runtime.experiment_history import ExperimentHistory
        from runtime.numerical_research import NumericalResearch

        class FakeAI:
            def __call__(self, prompt):
                return "invalid AI output"

        history = ExperimentHistory()
        research = NumericalResearch(
            inference=FakeAI(),
            history=history,
        )

        with self.assertRaises(ValueError):
            research.run(
                coupling_values=[0.0, 0.5, 1.0],
            )

        self.assertEqual(history.entries(), [])

    def test_ollama_inference_raises_on_network_failure(self):
        from unittest.mock import patch
        from urllib.error import URLError
        from runtime.ollama_inference import OllamaInference

        ai = OllamaInference(
            model="qwen2.5:0.5b",
            host="http://10.74.65.85:11434",
            timeout=1,
        )

        with patch(
            "urllib.request.urlopen",
            side_effect=URLError("network unavailable"),
        ):
            with self.assertRaises(URLError):
                ai("test")

    def test_ollama_inference_raises_on_timeout(self):
        from unittest.mock import patch
        from runtime.ollama_inference import OllamaInference

        ai = OllamaInference(
            model="qwen2.5:0.5b",
            host="http://10.74.65.85:11434",
            timeout=1,
        )

        with patch(
            "urllib.request.urlopen",
            side_effect=TimeoutError("request timed out"),
        ):
            with self.assertRaises(TimeoutError):
                ai("test")

    def test_ollama_inference_handles_malformed_response(self):
        from unittest.mock import patch
        from runtime.ollama_inference import OllamaInference

        ai = OllamaInference(
            model="qwen2.5:0.5b",
            host="http://10.74.65.85:11434",
        )

        class FakeResponse:
            def read(self):
                return b'{"unexpected": "response"}'

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        with patch(
            "urllib.request.urlopen",
            return_value=FakeResponse(),
        ):
            result = ai("test")

        self.assertEqual(result, "")

    def test_autonomous_runner_pauses_after_failure_limit(self):
        from runtime.autonomous_runner import AutonomousRunner

        class FailingLoop:
            def __init__(self):
                self.calls = 0

            def step(self, observation, memory_usage):
                self.calls += 1
                return {"status": "FAILED", "error": "test"}

        loop = FailingLoop()
        runner = AutonomousRunner(
            loop_controller=loop,
            interval=0.0,
            failure_limit=3,
        )

        results = runner.run(
            observation="test-task",
            max_cycles=10,
        )

        self.assertEqual(len(results), 3)
        self.assertEqual(results[-1]["status"], "TASK_PAUSED")
        self.assertEqual(results[-1]["reason"], "CIRCUIT_BREAKER")
        self.assertEqual(results[-1]["failures"], 3)
        self.assertEqual(loop.calls, 3)
        self.assertIn("test-task", runner.paused_tasks())

    def test_autonomous_research_loop_runs_multiple_cycles(self):
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

        results = [
            research.run([0.0, 0.5, 1.0]),
            research.run([0.0, 0.5, 1.0]),
        ]

        self.assertEqual(len(results), 2)
        self.assertTrue(
            all(result["status"] == "COMPLETED" for result in results)
        )
        self.assertEqual(len(history.entries()), 2)

    def test_research_loop_controller_runs_requested_cycles(self):
        from runtime.experiment_history import ExperimentHistory
        from runtime.numerical_research import NumericalResearch
        from runtime.research_loop import ResearchLoop

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

        loop = ResearchLoop(research)

        results = loop.run(
            coupling_values=[0.0, 0.5, 1.0],
            max_cycles=2,
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(len(history.entries()), 2)
        self.assertTrue(
            all(result["status"] == "COMPLETED" for result in results)
        )

    def test_research_loop_stops_after_failed_cycle(self):
        from runtime.research_loop import ResearchLoop

        class FakeResearch:
            def __init__(self):
                self.calls = 0

            def run(self, coupling_values, previous_result=None):
                self.calls += 1
                if self.calls == 1:
                    return {"status": "FAILED", "error": "test"}
                return {"status": "COMPLETED"}

        research = FakeResearch()
        loop = ResearchLoop(research)

        results = loop.run(
            coupling_values=[0.0, 0.5, 1.0],
            max_cycles=5,
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "FAILED")
        self.assertEqual(research.calls, 1)

    def test_research_loop_passes_previous_result_to_next_cycle(self):
        from runtime.research_loop import ResearchLoop

        class FakeResearch:
            def __init__(self):
                self.calls = []

            def run(self, coupling_values, previous_result=None):
                self.calls.append(previous_result)

                if len(self.calls) == 1:
                    return {
                        "status": "COMPLETED",
                        "model": "exponential",
                        "error": 0.1,
                    }

                return {
                    "status": "COMPLETED",
                    "model": "linear",
                    "error": 0.05,
                }

        research = FakeResearch()
        loop = ResearchLoop(research)

        results = loop.run(
            coupling_values=[0.0, 0.5, 1.0],
            max_cycles=2,
        )

        self.assertEqual(len(results), 2)
        self.assertIsNone(research.calls[0])
        self.assertEqual(research.calls[1]["model"], "exponential")
        self.assertEqual(research.calls[1]["error"], 0.1)

    def test_numerical_research_prompt_contains_previous_result(self):
        from runtime.numerical_research import NumericalResearch

        prompts = []

        class FakeAI:
            def __call__(self, prompt):
                prompts.append(prompt)
                return (
                    "Hypothesis: next hypothesis\n"
                    "Model Proposal: Linear model"
                )

        research = NumericalResearch(
            inference=FakeAI(),
        )

        previous = {
            "status": "COMPLETED",
            "model": "exponential",
            "error": 0.021,
        }

        research.run(
            coupling_values=[0.0, 0.5, 1.0],
            previous_result=previous,
        )

        self.assertIn("0.021", prompts[0])
        self.assertIn("exponential", prompts[0])


if __name__ == "__main__":
    unittest.main()


class TestExponentialRateSearch(unittest.TestCase):

    def test_search_exponential_rate_finds_best_rate(self):
        from runtime.numerical_engine import NumericalEngine

        engine = NumericalEngine()

        result = engine.search_exponential_rate(
            coupling_values=[0.0, 0.5, 1.0],
            rates=[0.5, 0.75, 1.0, 1.25, 1.5],
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["model"], "exponential")
        self.assertEqual(result["rate"], 0.75)
        self.assertLess(result["error"], 1.0)

    def test_search_exponential_rate_rejects_invalid_rates(self):
        from runtime.numerical_engine import NumericalEngine

        engine = NumericalEngine()

        result = engine.search_exponential_rate(
            coupling_values=[0.0, 0.5, 1.0],
            rates=[0.0, -1.0],
        )

        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(result["error"], "NO_VALID_RATES")

    def test_search_exponential_rate_ignores_invalid_rates(self):
        from runtime.numerical_engine import NumericalEngine

        engine = NumericalEngine()

        result = engine.search_exponential_rate(
            coupling_values=[0.0, 0.5, 1.0],
            rates=[-1.0, 0.0, 0.75],
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["model"], "exponential")
        self.assertEqual(result["rate"], 0.75)
