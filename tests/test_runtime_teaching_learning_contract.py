import unittest

from runtime.runtime import TranscendingRuntime
from runtime.teaching import Teaching


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "ok"


class TestRuntimeTeachingLearningContract(unittest.TestCase):
    def test_runtime_can_learn_teaching(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        teaching = Teaching(
            content="trees have leaves"
        )

        runtime.add_teaching(teaching)

        evaluation = runtime.learn_teaching(teaching)

        self.assertTrue(evaluation.accepted)
        self.assertEqual(teaching.status, "ACCEPTED")

    def test_accepted_teaching_enters_runtime_memory(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        teaching = Teaching(
            content="trees have leaves"
        )

        runtime.add_teaching(teaching)
        runtime.learn_teaching(teaching)

        self.assertTrue(
            runtime.memory.semantic_contains(
                "trees have leaves"
            )
        )

    def test_runtime_rejects_unregistered_teaching(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        teaching = Teaching(
            content="trees have leaves"
        )

        with self.assertRaises(ValueError):
            runtime.learn_teaching(teaching)


if __name__ == "__main__":
    unittest.main()
