import unittest

from runtime.autonomous_loop import AutonomousLoopController
from runtime.resource_guard import ResourceGuard
from runtime.auto_cooling import AutoCoolingController
from runtime.heartbeat import Heartbeat


class FakeRuntime:

    def autonomous_step(self, observation):
        return {
            "observation": observation
        }


class TestAutonomousLoopController(unittest.TestCase):

    def test_normal_cycle(self):
        loop = AutonomousLoopController(
            FakeRuntime(),
            ResourceGuard(),
            AutoCoolingController(),
            Heartbeat(),
        )

        result = loop.step(
            "observe tree",
            0.5,
        )

        self.assertEqual(
            result["status"],
            "RUNNING",
        )

    def test_memory_critical_pause(self):
        loop = AutonomousLoopController(
            FakeRuntime(),
            ResourceGuard(),
            AutoCoolingController(),
            Heartbeat(),
        )

        result = loop.step(
            "observe tree",
            0.99,
        )

        self.assertEqual(
            result["status"],
            "PAUSED",
        )


if __name__ == "__main__":
    unittest.main()
