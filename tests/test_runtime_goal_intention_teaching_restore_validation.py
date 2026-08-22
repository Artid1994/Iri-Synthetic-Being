import unittest

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "ok"

    def snapshot(self):
        return {}


class TestRuntimeGoalIntentionTeachingRestoreValidation(unittest.TestCase):
    def test_restore_rejects_non_dict(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        with self.assertRaises(TypeError):
            runtime.restore(None)

    def test_restore_rejects_invalid_goal_record(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        with self.assertRaises((KeyError, TypeError, ValueError)):
            runtime.restore(
                {
                    "goals": [
                        {
                            "id": "goal-001",
                            "description": "",
                            "priority": 5,
                            "status": "ACTIVE",
                        }
                    ]
                }
            )

    def test_restore_rejects_invalid_intention_record(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        with self.assertRaises((KeyError, TypeError, ValueError)):
            runtime.restore(
                {
                    "intentions": [
                        {
                            "id": "intention-001",
                            "description": "",
                            "status": "PENDING",
                            "goal_id": None,
                        }
                    ]
                }
            )

    def test_restore_rejects_invalid_teaching_record(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        with self.assertRaises((KeyError, TypeError, ValueError)):
            runtime.restore(
                {
                    "teachings": [
                        {
                            "id": "teaching-001",
                            "content": "",
                            "status": "ACCEPTED",
                        }
                    ]
                }
            )


if __name__ == "__main__":
    unittest.main()
