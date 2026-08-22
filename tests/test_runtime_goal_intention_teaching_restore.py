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


class TestRuntimeGoalIntentionTeachingRestore(unittest.TestCase):
    def test_restore_reconstructs_goal_intention_teaching(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        data = {
            "goals": [
                {
                    "id": "goal-001",
                    "description": "learn",
                    "priority": 5,
                    "status": "ACTIVE",
                }
            ],
            "intentions": [
                {
                    "id": "intention-001",
                    "description": "inspect object",
                    "status": "PENDING",
                    "goal_id": "goal-001",
                }
            ],
            "teachings": [
                {
                    "id": "teaching-001",
                    "content": "trees have leaves",
                    "status": "ACCEPTED",
                }
            ],
        }

        runtime.restore(data)

        self.assertEqual(len(runtime.goals), 1)
        self.assertEqual(runtime.goals[0].id, "goal-001")
        self.assertEqual(runtime.goals[0].description, "learn")
        self.assertEqual(runtime.goals[0].priority, 5)
        self.assertEqual(runtime.goals[0].status, "ACTIVE")

        self.assertEqual(len(runtime.intentions), 1)
        self.assertEqual(runtime.intentions[0].id, "intention-001")
        self.assertEqual(runtime.intentions[0].goal_id, "goal-001")

        self.assertEqual(len(runtime.teachings), 1)
        self.assertEqual(runtime.teachings[0].id, "teaching-001")
        self.assertEqual(
            runtime.teachings[0].content,
            "trees have leaves",
        )
        self.assertEqual(
            runtime.teachings[0].status,
            "ACCEPTED",
        )

    def test_restore_replaces_existing_runtime_records(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.add_goal(
            Goal(description="old goal")
        )
        runtime.add_intention(
            Intention(description="old intention")
        )
        runtime.add_teaching(
            Teaching(content="old teaching")
        )

        runtime.restore(
            {
                "goals": [],
                "intentions": [],
                "teachings": [],
            }
        )

        self.assertEqual(runtime.goals, [])
        self.assertEqual(runtime.intentions, [])
        self.assertEqual(runtime.teachings, [])


if __name__ == "__main__":
    unittest.main()
