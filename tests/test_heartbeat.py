import unittest

from runtime.heartbeat import Heartbeat


class TestHeartbeat(unittest.TestCase):

    def test_record_cycle(self):
        heartbeat = Heartbeat()

        heartbeat.record_cycle(
            "NORMAL",
            "RUNNING",
        )

        state = heartbeat.snapshot()

        self.assertEqual(
            state["cycle_count"],
            1,
        )

        self.assertEqual(
            state["memory_level"],
            "NORMAL",
        )

    def test_record_block(self):
        heartbeat = Heartbeat()

        heartbeat.record_block()

        state = heartbeat.snapshot()

        self.assertEqual(
            state["blocked_count"],
            1,
        )


if __name__ == "__main__":
    unittest.main()
