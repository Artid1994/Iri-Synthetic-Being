import unittest

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "memory stress response"


class TestStressMemoryPressure(unittest.TestCase):

    def test_memory_pressure_pause(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        result = runtime.start_safe_autonomous_runtime(
            "memory pressure",
            max_cycles=1,
            memory_usage=0.99,
        )

        self.assertEqual(
            result[0]["status"],
            "PAUSED",
        )


if __name__ == "__main__":
    unittest.main()
