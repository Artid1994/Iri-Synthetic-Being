import unittest

from runtime.sensor import SensorReading


class TestSensorAdapter(unittest.TestCase):
    def test_camera_adapter_output_is_sensor_reading(self):
        reading = SensorReading(
            sensor="camera",
            value="frame-data",
            timestamp=1.0,
        )

        self.assertEqual(reading.sensor, "camera")
        self.assertEqual(reading.value, "frame-data")
        self.assertEqual(reading.timestamp, 1.0)

    def test_microphone_adapter_output_is_sensor_reading(self):
        reading = SensorReading(
            sensor="microphone",
            value=b"audio-data",
            timestamp=2.0,
        )

        self.assertEqual(reading.sensor, "microphone")
        self.assertEqual(reading.value, b"audio-data")
        self.assertEqual(reading.timestamp, 2.0)


if __name__ == "__main__":
    unittest.main()
