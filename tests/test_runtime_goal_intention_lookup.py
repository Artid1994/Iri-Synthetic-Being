import unittest

from runtime.goal import Goal
from runtime.intention import Intention
from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "ok"


class TestRuntimeGoalIntentionLookup(unittest.TestCase):
    def test_runtime_can_find_intention_goal(self):
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

        self.assertIs(
            runtime.get_goal_for_intention(intention),
            goal,
        )

    def test_intention_without_goal_returns_none(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        intention = Intention(
            description="inspect object"
        )
        runtime.add_intention(intention)

        self.assertIsNone(
            runtime.get_goal_for_intention(intention)
        )

    def test_unknown_goal_returns_none(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        intention = Intention(
            description="inspect object",
            goal_id="missing-goal",
        )
        runtime.add_intention(intention)

        self.assertIsNone(
            runtime.get_goal_for_intention(intention)
        )


if __name__ == "__main__":
    unittest.main()
