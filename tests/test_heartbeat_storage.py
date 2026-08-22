import unittest
import tempfile
from pathlib import Path

from runtime.heartbeat_storage import HeartbeatStorage


class TestHeartbeatStorage(unittest.TestCase):

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "heartbeat.json"

            storage = HeartbeatStorage(
                str(path)
            )

            data = {
                "cycle_count": 10,
                "status": "RUNNING",
            }

            storage.save(data)

            result = storage.load()

            self.assertEqual(
                result["cycle_count"],
                10,
            )

            self.assertEqual(
                result["status"],
                "RUNNING",
            )


if __name__ == "__main__":
    unittest.main()
