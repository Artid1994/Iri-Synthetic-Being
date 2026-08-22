import unittest

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "trial autonomous response"


class TestAutonomousTrialRun(unittest.TestCase):

    def test_trial_run_10_cycles(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        results = runtime.start_safe_autonomous_runtime(
            "trial observation",
            max_cycles=10,
            memory_usage=0.5,
        )

        self.assertEqual(
            len(results),
            10,
        )

        for result in results:
            self.assertEqual(
                result["status"],
                "RUNNING",
            )

        heartbeat = runtime.heartbeat.snapshot()

        self.assertEqual(
            heartbeat["cycle_count"],
            10,
        )

    def test_memory_protection_trial(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        results = runtime.start_safe_autonomous_runtime(
            "memory pressure test",
            max_cycles=1,
            memory_usage=0.99,
        )

        self.assertEqual(
            results[0]["status"],
            "PAUSED",
        )


if __name__ == "__main__":
    unittest.main()
