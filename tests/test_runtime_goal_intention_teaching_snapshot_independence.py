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


class TestRuntimeGoalIntentionTeachingSnapshotIndependence(unittest.TestCase):
    def test_snapshot_lists_do_not_modify_runtime_state(self):
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

        snapshot["goals"].clear()
        snapshot["intentions"].clear()
        snapshot["teachings"].clear()

        self.assertEqual(runtime.goals, [goal])
        self.assertEqual(runtime.intentions, [intention])
        self.assertEqual(runtime.teachings, [teaching])


if __name__ == "__main__":
    unittest.main()
