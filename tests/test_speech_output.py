import unittest
from unittest.mock import patch

from runtime.speech_output import SpeechOutput


class TestSpeechOutput(unittest.TestCase):
    def test_empty_text_is_not_spoken(self):
        output = SpeechOutput()

        self.assertFalse(
            output.speak("")
        )

    def test_text_is_sent_to_espeak(self):
        output = SpeechOutput()

        with patch(
            "runtime.speech_output.subprocess.run"
        ) as run:
            run.return_value.returncode = 0

            result = output.speak(
                "สวัสดี"
            )

        self.assertTrue(result)
        run.assert_called_once()

        command = run.call_args.args[0]

        self.assertEqual(
            command[0],
            "espeak-ng",
        )
        self.assertEqual(
            command[-1],
            "สวัสดี",
        )


if __name__ == "__main__":
    unittest.main()
