import unittest
from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestRuntime(unittest.TestCase):
    def test_runtime_initializes(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())
        self.assertIsNotNone(runtime)


if __name__ == "__main__":
    unittest.main()
