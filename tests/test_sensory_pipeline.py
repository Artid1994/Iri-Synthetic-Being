import unittest

from runtime.perception import PerceptionModule
from runtime.sensor import Sensor


class TestSensoryPipeline(unittest.TestCase):
    def test_sensor_reading_can_enter_perception(self):
        sensor = Sensor("camera")
        reading = sensor.read("person_a_frame", 1.0)

        perception = PerceptionModule()
        result = perception.process(str(reading.value))

        self.assertTrue(result.has_input)
        self.assertEqual(result.normalized_input, "person_a_frame")

    def test_empty_sensor_value_produces_empty_perception(self):
        sensor = Sensor("microphone")
        reading = sensor.read("   ", 1.0)

        perception = PerceptionModule()
        result = perception.process(str(reading.value))

        self.assertFalse(result.has_input)
        self.assertEqual(result.normalized_input, "")


if __name__ == "__main__":
    unittest.main()
