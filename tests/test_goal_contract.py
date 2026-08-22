import unittest

from runtime.goal import Goal


class TestGoalContract(unittest.TestCase):
    def test_new_goal_starts_active(self):
        goal = Goal(description="learn to identify objects")

        self.assertTrue(goal.id)
        self.assertEqual(goal.description, "learn to identify objects")
        self.assertEqual(goal.priority, 0)
        self.assertEqual(goal.status, "ACTIVE")

    def test_goal_rejects_empty_description(self):
        with self.assertRaises(ValueError):
            Goal(description="")

    def test_goal_can_complete(self):
        goal = Goal(description="learn")

        goal.complete()

        self.assertEqual(goal.status, "COMPLETED")

    def test_goal_can_pause(self):
        goal = Goal(description="learn")

        goal.pause()

        self.assertEqual(goal.status, "PAUSED")


if __name__ == "__main__":
    unittest.main()
