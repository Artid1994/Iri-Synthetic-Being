import unittest
from unittest.mock import Mock

from runtime.audio_input import AudioChunk
from runtime.voice_conversation import VoiceConversation


class TestVoiceConversation(unittest.TestCase):
    def make_audio(self):
        return AudioChunk(
            data=b"\x00\x00",
            sample_rate=16000,
            channels=1,
            sample_width=2,
        )

    def test_audio_can_flow_through_cognition_to_speech(self):
        cognitive = Mock()
        cognitive.process.return_value = "สวัสดีครับ"

        recognition = Mock()
        recognition.transcribe.return_value = "สวัสดี"

        speech_output = Mock()
        speech_output.speak.return_value = True

        conversation = VoiceConversation(
            cognitive=cognitive,
            speech_output=speech_output,
            speech_recognition=recognition,
        )

        result = conversation.respond(self.make_audio())

        self.assertEqual(result, "สวัสดีครับ")

        recognition.transcribe.assert_called_once()
        cognitive.process.assert_called_once_with("สวัสดี")
        speech_output.speak.assert_called_once_with("สวัสดีครับ")

    def test_empty_transcription_does_not_call_cognitive_or_speech(self):
        cognitive = Mock()

        recognition = Mock()
        recognition.transcribe.return_value = ""

        speech_output = Mock()

        conversation = VoiceConversation(
            cognitive=cognitive,
            speech_output=speech_output,
            speech_recognition=recognition,
        )

        result = conversation.respond(self.make_audio())

        self.assertEqual(result, "")
        cognitive.process.assert_not_called()
        speech_output.speak.assert_not_called()

    def test_long_transcription_does_not_reach_cognitive(self):
        cognitive = Mock()

        recognition = Mock()
        recognition.transcribe.return_value = "ก" * 121

        speech_output = Mock()

        conversation = VoiceConversation(
            cognitive=cognitive,
            speech_output=speech_output,
            speech_recognition=recognition,
            max_text_length=120,
        )

        result = conversation.respond(self.make_audio())

        self.assertEqual(result, "")
        cognitive.process.assert_not_called()
        speech_output.speak.assert_not_called()


if __name__ == "__main__":
    unittest.main()
