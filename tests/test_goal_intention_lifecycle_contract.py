import unittest

from runtime.goal import Goal
from runtime.intention import Intention


class TestGoalIntentionLifecycleContract(unittest.TestCase):
    def test_goal_can_complete(self):
        goal = Goal(description="learn")

        goal.complete()

        self.assertEqual(goal.status, "COMPLETED")

    def test_goal_can_pause(self):
        goal = Goal(description="learn")

        goal.pause()

        self.assertEqual(goal.status, "PAUSED")

    def test_intention_can_activate(self):
        intention = Intention(description="learn")

        intention.activate()

        self.assertEqual(intention.status, "ACTIVE")

    def test_intention_can_complete(self):
        intention = Intention(description="learn")

        intention.activate()
        intention.complete()

        self.assertEqual(intention.status, "COMPLETED")

    def test_goal_completion_does_not_change_intention(self):
        goal = Goal(description="learn")
        intention = Intention(
            description="perform learning",
            goal_id=goal.id,
        )

        intention.activate()
        goal.complete()

        self.assertEqual(goal.status, "COMPLETED")
        self.assertEqual(intention.status, "ACTIVE")


if __name__ == "__main__":
    unittest.main()
