import unittest
import json

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "autonomous response"


class TestFullAutonomousValidation(unittest.TestCase):

    def test_full_autonomous_cycle(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        results = runtime.start_autonomous_runner(
            "observe environment",
            max_cycles=3,
            memory_usage=0.5,
        )

        self.assertEqual(
            len(results),
            3,
        )

        for result in results:
            self.assertEqual(
                result["status"],
                "RUNNING",
            )

        heartbeat = runtime.heartbeat.snapshot()

        self.assertEqual(
            heartbeat["cycle_count"],
            3,
        )

    def test_resource_protection(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        results = runtime.start_autonomous_runner(
            "observe environment",
            max_cycles=1,
            memory_usage=0.99,
        )

        self.assertEqual(
            results[0]["status"],
            "PAUSED",
        )


if __name__ == "__main__":
    unittest.main()
