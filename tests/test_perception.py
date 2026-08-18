import unittest

from runtime.perception import Perception, PerceptionModule


class TestPerception(unittest.TestCase):
    def setUp(self):
        self.perception = PerceptionModule()

    def test_empty_input_has_no_perception(self):
        result = self.perception.process("   ")

        self.assertIsInstance(result, Perception)
        self.assertEqual(result.raw_input, "   ")
        self.assertEqual(result.normalized_input, "")
        self.assertFalse(result.has_input)

    def test_input_is_normalized(self):
        result = self.perception.process("  hello world  ")

        self.assertEqual(result.raw_input, "  hello world  ")
        self.assertEqual(result.normalized_input, "hello world")
        self.assertTrue(result.has_input)

    def test_snapshot_is_independent(self):
        result = self.perception.process("hello")
        snapshot = self.perception.snapshot(result)

        self.assertEqual(snapshot, result)
        self.assertIsNot(snapshot, result)

    def test_none_snapshot_returns_none(self):
        self.assertIsNone(self.perception.snapshot(None))


if __name__ == "__main__":
    unittest.main()
