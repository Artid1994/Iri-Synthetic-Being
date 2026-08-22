import unittest
import tempfile
from pathlib import Path

from runtime.process_guard import ProcessGuard
from runtime.heartbeat_storage import HeartbeatStorage


class FakeHeartbeat:
    def snapshot(self):
        return {
            "cycle_count": 10
        }


class TestProcessGuard(unittest.TestCase):

    def test_shutdown_saves_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "heartbeat.json"

            storage = HeartbeatStorage(
                str(path)
            )

            guard = ProcessGuard(
                heartbeat_storage=storage,
                heartbeat=FakeHeartbeat(),
            )

            guard.request_shutdown(
                "TEST"
            )

            self.assertTrue(
                guard.is_shutdown_requested()
            )

            data = storage.load()

            self.assertEqual(
                data["status"],
                "SHUTDOWN",
            )

            self.assertEqual(
                data["reason"],
                "TEST",
            )


if __name__ == "__main__":
    unittest.main()
