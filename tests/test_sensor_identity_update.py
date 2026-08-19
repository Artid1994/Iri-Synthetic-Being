import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestSensorIdentityUpdate(unittest.TestCase):
    def test_camera_experience_updates_person_a_state(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        initial_identity = runtime.identity.snapshot()
        initial_personality = runtime.personality.snapshot()
        initial_self_model = runtime.self_model.snapshot()

        runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        identity = runtime.identity.snapshot()
        personality = runtime.personality.snapshot()
        self_model = runtime.self_model.snapshot()

        self.assertGreater(
            identity.experience,
            initial_identity.experience,
        )

        self.assertNotEqual(
            personality,
            initial_personality,
        )

        self.assertNotEqual(
            self_model,
            initial_self_model,
        )


if __name__ == "__main__":
    unittest.main()
