import unittest

from runtime.auto_cooling import AutoCoolingController


class TestAutoCooling(unittest.TestCase):

    def test_normal_no_delay(self):
        controller = AutoCoolingController()

        result = controller.handle("NORMAL")

        self.assertEqual(
            result.action,
            "NORMAL",
        )

    def test_cooling_adds_delay(self):
        controller = AutoCoolingController()

        result = controller.handle("COOLING")

        self.assertEqual(
            result.action,
            "COOLING",
        )

        self.assertGreater(
            result.delay,
            0,
        )

    def test_critical_pause(self):
        controller = AutoCoolingController()

        result = controller.handle("CRITICAL")

        self.assertEqual(
            result.action,
            "PAUSE",
        )


if __name__ == "__main__":
    unittest.main()
