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


class TestRuntimeGoalIntentionTeachingSerialize(unittest.TestCase):
    def test_serialize_contains_goal_intention_teaching(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        goal = Goal(
            description="learn",
            priority=5,
            id="goal-001",
        )

        intention = Intention(
            description="inspect object",
            goal_id="goal-001",
            id="intention-001",
        )

        teaching = Teaching(
            content="trees have leaves",
            status="ACCEPTED",
            id="teaching-001",
        )

        runtime.add_goal(goal)
        runtime.add_intention(intention)
        runtime.add_teaching(teaching)

        data = runtime.serialize()

        self.assertEqual(
            data["goals"],
            [
                {
                    "id": "goal-001",
                    "description": "learn",
                    "priority": 5,
                    "status": "ACTIVE",
                }
            ],
        )

        self.assertEqual(
            data["intentions"],
            [
                {
                    "id": "intention-001",
                    "description": "inspect object",
                    "status": "PENDING",
                    "goal_id": "goal-001",
                }
            ],
        )

        self.assertEqual(
            data["teachings"],
            [
                {
                    "id": "teaching-001",
                    "content": "trees have leaves",
                    "status": "ACCEPTED",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
