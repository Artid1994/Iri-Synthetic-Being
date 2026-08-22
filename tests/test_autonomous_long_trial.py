import unittest

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "long trial response"


class TestAutonomousLongTrial(unittest.TestCase):

    def test_100_cycle_trial(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        results = runtime.start_safe_autonomous_runtime(
            "long autonomous trial",
            max_cycles=100,
            memory_usage=0.5,
        )

        self.assertEqual(
            len(results),
            100,
        )

        heartbeat = runtime.heartbeat.snapshot()

        self.assertEqual(
            heartbeat["cycle_count"],
            100,
        )

        for result in results:
            self.assertEqual(
                result["status"],
                "RUNNING",
            )


if __name__ == "__main__":
    unittest.main()
