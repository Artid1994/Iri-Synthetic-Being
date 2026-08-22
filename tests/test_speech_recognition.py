import unittest

from runtime.audio_input import AudioChunk
from runtime.speech_recognition import SpeechRecognition


class TestSpeechRecognition(unittest.TestCase):
    def test_audio_chunk_can_be_transcribed(self):
        recognizer = SpeechRecognition()

        audio = AudioChunk(
            data=b"\x00\x01",
            sample_rate=16000,
            channels=1,
            sample_width=2,
        )

        result = recognizer.transcribe(audio)

        self.assertIsInstance(result, str)

    def test_invalid_audio_is_rejected(self):
        recognizer = SpeechRecognition()

        with self.assertRaises(TypeError):
            recognizer.transcribe(b"invalid")


if __name__ == "__main__":
    unittest.main()
