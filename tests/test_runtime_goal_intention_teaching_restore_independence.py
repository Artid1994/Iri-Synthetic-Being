import unittest

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "ok"

    def snapshot(self):
        return {}


class TestRuntimeGoalIntentionTeachingRestoreIndependence(unittest.TestCase):
    def test_restore_creates_independent_records(self):
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

        data["goals"][0]["description"] = "changed"
        data["intentions"][0]["description"] = "changed"
        data["teachings"][0]["content"] = "changed"

        self.assertEqual(
            runtime.goals[0].description,
            "learn",
        )
        self.assertEqual(
            runtime.intentions[0].description,
            "inspect object",
        )
        self.assertEqual(
            runtime.teachings[0].content,
            "trees have leaves",
        )


if __name__ == "__main__":
    unittest.main()
