import unittest

from runtime.audio_input import AudioChunk, AudioInput


class TestAudioInput(unittest.TestCase):
    def test_audio_chunk_contains_audio_metadata(self):
        chunk = AudioChunk(
            data=b"\x00\x01",
            sample_rate=16000,
            channels=1,
            sample_width=2,
        )

        self.assertEqual(chunk.sample_rate, 16000)
        self.assertEqual(chunk.channels, 1)
        self.assertEqual(chunk.sample_width, 2)
        self.assertEqual(chunk.data, b"\x00\x01")

    def test_invalid_duration_is_rejected(self):
        audio = AudioInput()

        with self.assertRaises(ValueError):
            audio.record(0)


if __name__ == "__main__":
    unittest.main()
