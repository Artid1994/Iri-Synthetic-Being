import unittest

from runtime.sensor import Sensor, SensorReading


class TestSensor(unittest.TestCase):
    def test_sensor_initializes_without_reading(self):
        sensor = Sensor("camera")

        self.assertEqual(sensor.name, "camera")
        self.assertIsNone(sensor.snapshot())

    def test_empty_sensor_name_is_rejected(self):
        with self.assertRaises(ValueError):
            Sensor("   ")

    def test_read_creates_sensor_reading(self):
        sensor = Sensor("camera")

        reading = sensor.read(
            value=b"frame",
            timestamp=1.25,
        )

        self.assertIsInstance(reading, SensorReading)
        self.assertEqual(reading.sensor, "camera")
        self.assertEqual(reading.value, b"frame")
        self.assertEqual(reading.timestamp, 1.25)

    def test_latest_reading_is_preserved(self):
        sensor = Sensor("microphone")

        first = sensor.read(b"audio-1", 1.0)
        second = sensor.read(b"audio-2", 2.0)

        self.assertEqual(sensor.snapshot(), second)
        self.assertNotEqual(sensor.snapshot(), first)


if __name__ == "__main__":
    unittest.main()
