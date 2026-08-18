import unittest
from runtime.runtime import TranscendingRuntime


class TestRuntime(unittest.TestCase):
    def test_runtime_initializes(self):
        runtime = TranscendingRuntime()
        self.assertIsNotNone(runtime)


if __name__ == "__main__":
    unittest.main()
