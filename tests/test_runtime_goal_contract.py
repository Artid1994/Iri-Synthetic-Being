import unittest

from runtime.goal import Goal
from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "ok"


class TestRuntimeGoalContract(unittest.TestCase):
    def test_runtime_starts_with_no_goals(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        self.assertEqual(runtime.goals, [])

    def test_runtime_can_add_goal(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        goal = Goal(
            description="learn to identify objects"
        )

        runtime.add_goal(goal)

        self.assertEqual(runtime.goals, [goal])

    def test_runtime_rejects_invalid_goal(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        with self.assertRaises(TypeError):
            runtime.add_goal("invalid")


if __name__ == "__main__":
    unittest.main()
