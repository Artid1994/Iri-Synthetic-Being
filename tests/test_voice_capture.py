import unittest
from unittest.mock import Mock, patch

from runtime.voice_capture import VoiceCapture


class TestVoiceCapture(unittest.TestCase):
    @patch("runtime.voice_capture.subprocess.Popen")
    def test_capture_returns_audio_chunk(self, popen):
        process = Mock()

        process.stdout.read.side_effect = [
            b"\x00\x00" * 1600,
            b"",
        ]

        popen.return_value = process

        capture = VoiceCapture()

        result = capture.listen()

        self.assertEqual(
            result.sample_rate,
            16000,
        )

        self.assertEqual(
            result.channels,
            1,
        )

        self.assertEqual(
            result.sample_width,
            2,
        )

        process.terminate.assert_called_once()
        process.wait.assert_called_once()


if __name__ == "__main__":
    unittest.main()
