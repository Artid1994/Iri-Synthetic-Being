import unittest

from runtime.runtime import TranscendingRuntime


class TestRuntimeSensorMemoryContract(unittest.TestCase):
    def test_sensor_experience_is_recorded_once(self):
        runtime = TranscendingRuntime()

        result = runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        self.assertTrue(result)

        self.assertEqual(
            runtime.memory.state.episodic.count(
                "person A sees tree"
            ),
            1,
        )

        self.assertEqual(
            runtime.memory.state.semantic.count(
                "person A sees tree"
            ),
            1,
        )


if __name__ == "__main__":
    unittest.main()
