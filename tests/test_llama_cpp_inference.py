import unittest

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
                "-m",
                "/models/gemma.gguf",
                "-t",
                "1",
                "-c",
                "256",
                "-n",
                "32",
                "-no-cnv",
                "-p",
                "person A sees tree",
            ]],
        )


if __name__ == "__main__":
    unittest.main()
