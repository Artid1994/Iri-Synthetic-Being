import unittest

from runtime.runtime import TranscendingRuntime


class TestRuntimeSensors(unittest.TestCase):
    def test_runtime_creates_person_a_sensors(self):
        runtime = TranscendingRuntime()

        self.assertEqual(runtime.camera.name, "camera")
        self.assertEqual(runtime.microphone.name, "microphone")

    def test_runtime_camera_can_produce_reading(self):
        runtime = TranscendingRuntime()

        runtime.camera.value = "person A sees tree"
        reading = runtime.camera.read(1.0)

        self.assertEqual(reading.sensor, "camera")
        self.assertEqual(reading.value, "person A sees tree")
        self.assertEqual(reading.timestamp, 1.0)

    def test_runtime_microphone_can_produce_reading(self):
        runtime = TranscendingRuntime()

        runtime.microphone.value = "person A hears a voice"
        reading = runtime.microphone.read(2.0)

        self.assertEqual(reading.sensor, "microphone")
        self.assertEqual(reading.value, "person A hears a voice")
        self.assertEqual(reading.timestamp, 2.0)


if __name__ == "__main__":
    unittest.main()
