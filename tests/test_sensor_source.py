import unittest

from runtime.sensor import SensorReading
from runtime.sensor_source import (
    CameraSensorSource,
    MicrophoneSensorSource,
    SensorSource,
)


class TestSensorSource(unittest.TestCase):
    def test_source_exposes_read(self):
        class MockSource:
            def read(self, timestamp: float) -> SensorReading:
                return SensorReading(
                    sensor="mock",
                    value="test",
                    timestamp=timestamp,
                )

        source = MockSource()
        reading = source.read(1.0)

        self.assertIsInstance(reading, SensorReading)
        self.assertEqual(reading.sensor, "mock")
        self.assertEqual(reading.value, "test")
        self.assertEqual(reading.timestamp, 1.0)

    def test_camera_source_adapts_a_frame_reader(self):
        captured = []

        def read_frame():
            captured.append(True)
            return b"frame-data"

        source = CameraSensorSource(read_frame)
        reading = source.read(1.0)

        self.assertIsInstance(source, SensorSource)
        self.assertEqual(captured, [True])
        self.assertEqual(reading.sensor, "camera")
        self.assertEqual(reading.value, b"frame-data")
        self.assertEqual(reading.timestamp, 1.0)

    def test_microphone_source_adapts_an_audio_reader(self):
        captured = []

        def read_audio():
            captured.append(True)
            return b"audio-data"

        source = MicrophoneSensorSource(read_audio)
        reading = source.read(2.0)

        self.assertIsInstance(source, SensorSource)
        self.assertEqual(captured, [True])
        self.assertEqual(reading.sensor, "microphone")
        self.assertEqual(reading.value, b"audio-data")
        self.assertEqual(reading.timestamp, 2.0)


if __name__ == "__main__":
    unittest.main()
