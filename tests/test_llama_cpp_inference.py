import unittest
from unittest.mock import patch

from runtime.llama_cpp_inference import LlamaCppInference


class TestLlamaCppInference(unittest.TestCase):
    def test_inference_builds_command_with_prompt(self):
        calls = []

        def fake_runner(command):
            calls.append(command)
            return "internal thought"

        inference = LlamaCppInference(
            model_path="/models/gemma.gguf",
            executable="/bin/llama-completion",
            runner=fake_runner,
        )

        result = inference("person A sees tree")

        self.assertEqual(result, "internal thought")
        self.assertEqual(
            calls,
            [[
                "/bin/llama-completion",
                "-m", "/models/gemma.gguf",
                "-t", "1",
                "-c", "256",
                "-n", "32",
                "-no-cnv",
                "-p", "person A sees tree",
            ]],
        )


    @patch("runtime.llama_cpp_inference.subprocess.run")
    def test_subprocess_runner_returns_stdout(self, mock_run):
        mock_run.return_value.stdout = "model output\n"

        inference = LlamaCppInference(
            model_path="/models/gemma.gguf",
            executable="/bin/llama-completion",
        )

        result = inference("hello")

        self.assertEqual(result, "model output")
        mock_run.assert_called_once()

        _, kwargs = mock_run.call_args
        self.assertEqual(kwargs["capture_output"], True)
        self.assertEqual(kwargs["text"], True)
        self.assertEqual(kwargs["check"], True)
        self.assertEqual(kwargs["timeout"], 60)


if __name__ == "__main__":
    unittest.main()

    @patch("runtime.llama_cpp_inference.subprocess.run")
    def test_subprocess_runner_returns_stdout(self, mock_run):
        mock_run.return_value.stdout = "model output\n"

        inference = LlamaCppInference(
            model_path="/models/gemma.gguf",
            executable="/bin/llama-completion",
        )

        result = inference("hello")

        self.assertEqual(result, "model output")
        mock_run.assert_called_once()

        _, kwargs = mock_run.call_args
        self.assertEqual(kwargs["capture_output"], True)
        self.assertEqual(kwargs["text"], True)
        self.assertEqual(kwargs["check"], True)
        self.assertEqual(kwargs["timeout"], 60)
