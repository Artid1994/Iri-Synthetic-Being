import unittest
from unittest.mock import Mock

from runtime.audio_input import AudioChunk
from runtime.voice_conversation import VoiceConversation


class TestVoicePipeline(unittest.TestCase):
    def test_voice_pipeline_transcribes_thinks_and_speaks(self):
        recognition = Mock()
        recognition.transcribe.return_value = "สวัสดี"

        cognitive = Mock()
        cognitive.process.return_value = "สวัสดีครับ ผมพร้อมทำงาน"

        speech_output = Mock()
        speech_output.speak.return_value = True

        conversation = VoiceConversation(
            cognitive=cognitive,
            speech_output=speech_output,
            speech_recognition=recognition,
        )

        audio = AudioChunk(
            data=b"\x00\x00" * 1600,
            sample_rate=16000,
            channels=1,
            sample_width=2,
        )

        result = conversation.respond(audio)

        self.assertEqual(
            result,
            "สวัสดีครับ ผมพร้อมทำงาน",
        )

        recognition.transcribe.assert_called_once_with(audio)
        cognitive.process.assert_called_once_with("สวัสดี")
        speech_output.speak.assert_called_once_with(
            "สวัสดีครับ ผมพร้อมทำงาน"
        )


if __name__ == "__main__":
    unittest.main()
