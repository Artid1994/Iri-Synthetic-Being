import unittest

from runtime.goal import Goal
from runtime.intention import Intention
from runtime.learning import Learning
from runtime.memory import Memory
from runtime.teaching import Teaching


class TestGoalIntentionTeachingIntegration(unittest.TestCase):
    def test_goal_to_intention_to_teaching_to_memory(self):
        goal = Goal(description="learn to identify objects")

        intention = Intention(
            description="inspect the object",
            goal_id=goal.id,
        )
        intention.activate()

        teaching = Teaching(
            content="trees have leaves",
        )

        memory = Memory()
        learning = Learning(memory)

        evaluation = learning.evaluate_teaching(teaching)

        self.assertEqual(intention.goal_id, goal.id)
        self.assertEqual(intention.status, "ACTIVE")

        self.assertTrue(evaluation.accepted)
        self.assertEqual(teaching.status, "ACCEPTED")

        self.assertTrue(
            memory.semantic_contains("trees have leaves")
        )

    def test_goal_completion_does_not_implicitly_complete_intention(self):
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
