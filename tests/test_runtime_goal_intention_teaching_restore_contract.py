import unittest

from runtime.goal import Goal
from runtime.intention import Intention
from runtime.teaching import Teaching
from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "ok"

    def snapshot(self):
        return {}


class TestRuntimeGoalIntentionTeachingRestoreContract(unittest.TestCase):
    def test_snapshot_contains_restorable_goal_intention_teaching_state(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        goal = Goal(description="learn")
        intention = Intention(
            description="inspect object",
            goal_id=goal.id,
        )
        teaching = Teaching(
            content="trees have leaves"
        )

        runtime.add_goal(goal)
        runtime.add_intention(intention)
        runtime.add_teaching(teaching)

        snapshot = runtime.snapshot()

        self.assertEqual(
            snapshot["goals"][0],
            goal,
        )
        self.assertEqual(
            snapshot["intentions"][0],
            intention,
        )
        self.assertEqual(
            snapshot["teachings"][0],
            teaching,
        )

        self.assertEqual(
            snapshot["intentions"][0].goal_id,
            snapshot["goals"][0].id,
        )


if __name__ == "__main__":
    unittest.main()
