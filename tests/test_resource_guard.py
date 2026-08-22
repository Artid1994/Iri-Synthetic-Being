import unittest

from runtime.resource_guard import ResourceGuard


class TestResourceGuard(unittest.TestCase):

    def test_normal_memory(self):
        guard = ResourceGuard()

        result = guard.evaluate(0.50)

        self.assertEqual(
            result.level,
            "NORMAL",
        )

    def test_cooling_memory(self):
        guard = ResourceGuard()

        result = guard.evaluate(0.85)

        self.assertEqual(
            result.level,
            "COOLING",
        )

    def test_critical_memory(self):
        guard = ResourceGuard()

        result = guard.evaluate(0.96)

        self.assertEqual(
            result.level,
            "CRITICAL",
        )


if __name__ == "__main__":
    unittest.main()
