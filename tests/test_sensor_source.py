import unittest

from runtime.sensor import SensorReading


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


if __name__ == "__main__":
    unittest.main()
