import unittest
import tempfile
from pathlib import Path

from runtime.runtime import TranscendingRuntime
from runtime.heartbeat_storage import HeartbeatStorage


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "shutdown test"


class TestRuntimeShutdown(unittest.TestCase):

    def test_runtime_shutdown(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.shutdown(
            "TEST_SIGNAL"
        )

        self.assertTrue(
            runtime.process_guard.is_shutdown_requested()
        )

        self.assertEqual(
            runtime.process_guard.shutdown_reason,
            "TEST_SIGNAL",
        )


if __name__ == "__main__":
    unittest.main()
