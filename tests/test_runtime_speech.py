import unittest
from unittest.mock import patch

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "สวัสดีครับ ผมได้ยินคุณแล้ว"


class TestRuntimeSpeech(unittest.TestCase):
    def test_runtime_can_speak_cognitive_response(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        with patch.object(
            runtime.speech_output,
            "speak",
            return_value=True,
        ) as speak:
            response = runtime.cognitive.process(
                "สวัสดี"
            )

            result = runtime.speak(response)

        self.assertEqual(
            response,
            "สวัสดีครับ ผมได้ยินคุณแล้ว",
        )
        self.assertTrue(result)
        speak.assert_called_once_with(
            "สวัสดีครับ ผมได้ยินคุณแล้ว"
        )


if __name__ == "__main__":
    unittest.main()
