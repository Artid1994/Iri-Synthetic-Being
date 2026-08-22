import unittest

from runtime.goal import Goal
from runtime.intention import Intention
from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "ok"


class TestRuntimeIntentionContract(unittest.TestCase):
    def test_runtime_starts_with_no_intentions(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        self.assertEqual(runtime.intentions, [])

    def test_runtime_can_add_intention(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        goal = Goal(description="learn")
        runtime.add_goal(goal)

        intention = Intention(
            description="inspect object",
            goal_id=goal.id,
        )

        runtime.add_intention(intention)

        self.assertEqual(runtime.intentions, [intention])

    def test_runtime_rejects_invalid_intention(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        with self.assertRaises(TypeError):
            runtime.add_intention("invalid")


if __name__ == "__main__":
    unittest.main()
