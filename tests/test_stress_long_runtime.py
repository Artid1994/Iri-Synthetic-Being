import unittest

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "long stress response"


class TestStressLongRuntime(unittest.TestCase):

    def test_500_cycle_runtime(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        results = runtime.start_safe_autonomous_runtime(
            "500 cycle stress",
            max_cycles=500,
            memory_usage=0.5,
        )

        self.assertEqual(
            len(results),
            500,
        )

        heartbeat = runtime.heartbeat.snapshot()

        self.assertEqual(
            heartbeat["cycle_count"],
            500,
        )


if __name__ == "__main__":
    unittest.main()
