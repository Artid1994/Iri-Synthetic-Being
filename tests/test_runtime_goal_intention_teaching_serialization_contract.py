import unittest

from runtime.goal import Goal
from runtime.intention import Intention
from runtime.teaching import Teaching


class TestRuntimeGoalIntentionTeachingSerializationContract(unittest.TestCase):
    def test_goal_serialization_shape(self):
        goal = Goal(
            description="learn",
            priority=5,
            status="ACTIVE",
            id="goal-001",
        )

        data = {
            "id": goal.id,
            "description": goal.description,
            "priority": goal.priority,
            "status": goal.status,
        }

        self.assertEqual(
            data,
            {
                "id": "goal-001",
                "description": "learn",
                "priority": 5,
                "status": "ACTIVE",
            },
        )

    def test_intention_serialization_preserves_goal_reference(self):
        intention = Intention(
            description="inspect object",
            status="ACTIVE",
            goal_id="goal-001",
            id="intention-001",
        )

        data = {
            "id": intention.id,
            "description": intention.description,
            "status": intention.status,
            "goal_id": intention.goal_id,
        }

        self.assertEqual(data["goal_id"], "goal-001")

    def test_teaching_serialization_shape(self):
        teaching = Teaching(
            content="trees have leaves",
            status="ACCEPTED",
            id="teaching-001",
        )

        data = {
            "id": teaching.id,
            "content": teaching.content,
            "status": teaching.status,
        }

        self.assertEqual(
            data,
            {
                "id": "teaching-001",
                "content": "trees have leaves",
                "status": "ACCEPTED",
            },
        )


if __name__ == "__main__":
    unittest.main()
