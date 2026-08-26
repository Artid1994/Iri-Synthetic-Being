import json
import unittest
from unittest.mock import patch

from runtime.ollama_inference import OllamaInference


class TestOllamaInference(unittest.TestCase):
    @patch("runtime.ollama_inference.urllib.request.urlopen")
    def test_chat_returns_message_content(self, mock_urlopen):
        response = mock_urlopen.return_value.__enter__.return_value
        response.read.return_value = json.dumps({
            "model": "qwen3.5:0.8b",
            "message": {
                "role": "assistant",
                "content": "4",
            },
            "done": True,
        }).encode("utf-8")

        inference = OllamaInference(
            model="qwen3.5:0.8b",
        )

        result = inference("What is 2+2?")

        self.assertEqual(result, "4")

    @patch("runtime.ollama_inference.urllib.request.urlopen")
    def test_request_disables_thinking(self, mock_urlopen):
        response = mock_urlopen.return_value.__enter__.return_value
        response.read.return_value = json.dumps({
            "message": {
                "role": "assistant",
                "content": "4",
            },
        }).encode("utf-8")

        inference = OllamaInference(
            model="qwen3.5:0.8b",
        )

        inference("What is 2+2?")

        request = mock_urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))

        self.assertEqual(
            payload["model"],
            "qwen3.5:0.8b",
        )
        self.assertFalse(payload["think"])
        self.assertFalse(payload["stream"])

    @patch("runtime.ollama_inference.urllib.request.urlopen")
    def test_request_uses_low_memory_parameters(self, mock_urlopen):
        response = mock_urlopen.return_value.__enter__.return_value
        response.read.return_value = json.dumps({
            "message": {
                "role": "assistant",
                "content": "4",
            },
        }).encode("utf-8")

        inference = OllamaInference(
            model="qwen3.5:0.8b",
        )

        inference("What is 2+2?")

        request = mock_urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))

        self.assertEqual(payload["options"]["num_ctx"], 1024)
        self.assertEqual(payload["options"]["num_predict"], 16)
        self.assertEqual(payload["options"]["temperature"], 0.2)
        self.assertEqual(payload["options"]["top_p"], 0.7)


if __name__ == "__main__":
    unittest.main()
