import unittest

from runtime.runtime import TranscendingRuntime
from runtime.teaching import Teaching


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "ok"


class TestRuntimeTeachingContract(unittest.TestCase):
    def test_runtime_starts_with_no_teachings(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        self.assertEqual(runtime.teachings, [])

    def test_runtime_can_add_teaching(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        teaching = Teaching(
            content="trees have leaves"
        )

        runtime.add_teaching(teaching)

        self.assertEqual(runtime.teachings, [teaching])

    def test_runtime_rejects_invalid_teaching(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        with self.assertRaises(TypeError):
            runtime.add_teaching("invalid")


if __name__ == "__main__":
    unittest.main()
