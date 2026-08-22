import unittest
from unittest.mock import Mock

from runtime.audio_input import AudioChunk
from runtime.runtime import TranscendingRuntime


class TestRuntimeVoiceRespond(unittest.TestCase):
    def test_runtime_voice_responds_to_audio(self):
        runtime = TranscendingRuntime(
            cognitive=Mock()
        )

        runtime.voice_conversation = Mock()
        runtime.voice_conversation.respond.return_value = (
            "สวัสดีครับ"
        )

        audio = AudioChunk(
            data=b"\x00\x00",
            sample_rate=16000,
            channels=1,
            sample_width=2,
        )

        result = runtime.voice_respond(audio)

        self.assertEqual(
            result,
            "สวัสดีครับ",
        )

        runtime.voice_conversation.respond.assert_called_once_with(
            audio
        )


if __name__ == "__main__":
    unittest.main()
