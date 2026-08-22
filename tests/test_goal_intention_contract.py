import unittest

from runtime.goal import Goal
from runtime.intention import Intention


class TestGoalIntentionContract(unittest.TestCase):
    def test_intention_can_reference_goal(self):
        goal = Goal(description="learn to identify objects")
        intention = Intention(
            description="inspect the object",
            goal_id=goal.id,
        )

        self.assertEqual(intention.goal_id, goal.id)

    def test_intention_without_goal_is_allowed(self):
        intention = Intention(description="explore")

        self.assertIsNone(intention.goal_id)


if __name__ == "__main__":
    unittest.main()
