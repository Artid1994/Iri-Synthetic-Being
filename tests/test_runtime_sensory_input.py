import unittest

from runtime.runtime import TranscendingRuntime


class TestRuntimeSensoryInput(unittest.TestCase):
    def test_camera_input_reaches_memory(self):
        runtime = TranscendingRuntime()

        result = runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        self.assertTrue(result)
        self.assertIn(
            "person A sees tree",
            runtime.memory.state.episodic,
        )

    def test_microphone_input_reaches_memory(self):
        runtime = TranscendingRuntime()

        result = runtime.process_sensor(
            sensor="microphone",
            value="person A hears a voice",
            timestamp=2.0,
            modality="audio",
        )

        self.assertTrue(result)
        self.assertIn(
            "person A hears a voice",
            runtime.memory.state.episodic,
        )


if __name__ == "__main__":
    unittest.main()
