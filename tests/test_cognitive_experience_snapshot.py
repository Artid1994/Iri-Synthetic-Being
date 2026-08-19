import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestCognitiveExperienceSnapshot(unittest.TestCase):
    def test_sensor_experience_survives_runtime_snapshot(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        snapshot = runtime.snapshot()

        self.assertEqual(
            snapshot["cognitive_loop"].input_text,
            "person A sees tree",
        )

        self.assertEqual(
            snapshot["memory"].experiences[0].source,
            "camera",
        )

        self.assertEqual(
            snapshot["memory"].experiences[0].modality,
            "vision",
        )


if __name__ == "__main__":
    unittest.main()
