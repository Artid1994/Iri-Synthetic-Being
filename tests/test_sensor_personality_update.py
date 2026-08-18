import unittest

from runtime.runtime import TranscendingRuntime


class TestSensorPersonalityUpdate(unittest.TestCase):
    def test_camera_experience_updates_person_a_personality(self):
        runtime = TranscendingRuntime()

        initial = runtime.personality.snapshot()

        runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        current = runtime.personality.snapshot()

        self.assertGreater(
            current.openness,
            initial.openness,
        )

        self.assertGreater(
            current.conscientiousness,
            initial.conscientiousness,
        )


if __name__ == "__main__":
    unittest.main()
