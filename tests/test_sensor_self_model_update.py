import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestSensorSelfModelUpdate(unittest.TestCase):
    def test_camera_experience_updates_person_a_self_model(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        initial = runtime.self_model.snapshot()

        runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        current = runtime.self_model.snapshot()

        self.assertGreater(
            current.self_awareness,
            initial.self_awareness,
        )

        self.assertGreater(
            current.self_knowledge,
            initial.self_knowledge,
        )

        self.assertIn(
            "person A sees tree",
            current.self_history,
        )


if __name__ == "__main__":
    unittest.main()
