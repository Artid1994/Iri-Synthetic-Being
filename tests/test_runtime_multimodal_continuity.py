import unittest

from runtime.runtime import TranscendingRuntime


class TestRuntimeMultimodalContinuity(unittest.TestCase):
    def test_vision_and_audio_belong_to_same_person_a_memory(self):
        runtime = TranscendingRuntime()

        runtime.process_sensor(
            sensor="camera",
            value="person A sees a tree",
            timestamp=1.0,
            modality="vision",
        )

        runtime.process_sensor(
            sensor="microphone",
            value="person A hears a voice",
            timestamp=2.0,
            modality="audio",
        )

        experiences = runtime.memory.state.experiences

        self.assertEqual(len(experiences), 2)

        self.assertEqual(experiences[0].modality, "vision")
        self.assertEqual(experiences[1].modality, "audio")

        self.assertEqual(
            experiences[0].content,
            "person A sees a tree",
        )
        self.assertEqual(
            experiences[1].content,
            "person A hears a voice",
        )

        self.assertEqual(
            runtime.memory.state.episodic,
            [
                "person A sees a tree",
                "person A hears a voice",
            ],
        )


if __name__ == "__main__":
    unittest.main()
