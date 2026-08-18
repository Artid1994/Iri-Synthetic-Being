import unittest

from runtime.runtime import TranscendingRuntime


class TestRuntimeSensorCognition(unittest.TestCase):
    def test_camera_sensor_reaches_cognitive_loop(self):
        runtime = TranscendingRuntime()

        result = runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        self.assertTrue(result)

        cycle = runtime.cognitive_loop.last_cycle

        self.assertIsNotNone(cycle)
        self.assertEqual(
            cycle.input_text,
            "person A sees tree",
        )
        self.assertTrue(cycle.experience_recorded)

    def test_microphone_sensor_reaches_cognitive_loop(self):
        runtime = TranscendingRuntime()

        result = runtime.process_sensor(
            sensor="microphone",
            value="person A hears a voice",
            timestamp=2.0,
            modality="audio",
        )

        self.assertTrue(result)

        cycle = runtime.cognitive_loop.last_cycle

        self.assertIsNotNone(cycle)
        self.assertEqual(
            cycle.input_text,
            "person A hears a voice",
        )
        self.assertTrue(cycle.experience_recorded)


if __name__ == "__main__":
    unittest.main()
