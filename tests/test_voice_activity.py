import math
import unittest

from runtime.voice_activity import VoiceActivityDetector


def pcm16(amplitude: int, samples: int = 1600) -> bytes:
    sample = int(amplitude).to_bytes(
        2,
        byteorder="little",
        signed=True,
    )
    return sample * samples


class TestVoiceActivityDetector(unittest.TestCase):
    def test_silence_is_detected(self):
        detector = VoiceActivityDetector()

        self.assertEqual(
            detector.process(pcm16(0)),
            "silence",
        )

    def test_speech_starts_when_energy_exceeds_threshold(self):
        detector = VoiceActivityDetector(
            threshold=0.01,
        )

        self.assertEqual(
            detector.process(pcm16(10000)),
            "speech",
        )

        self.assertTrue(detector.speaking)

    def test_speech_end_after_continuous_silence(self):
        detector = VoiceActivityDetector(
            threshold=0.01,
            silence_duration=0.3,
            frame_duration=0.1,
        )

        self.assertEqual(
            detector.process(pcm16(10000)),
            "speech",
        )

        self.assertEqual(
            detector.process(pcm16(0)),
            "silence",
        )

        self.assertEqual(
            detector.process(pcm16(0)),
            "silence",
        )

        self.assertEqual(
            detector.process(pcm16(0)),
            "speech_end",
        )

        self.assertFalse(detector.speaking)


if __name__ == "__main__":
    unittest.main()
