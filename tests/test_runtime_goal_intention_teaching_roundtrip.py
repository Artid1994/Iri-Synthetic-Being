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


class TestRuntimeGoalIntentionTeachingRoundTrip(unittest.TestCase):
    def test_serialize_restore_serialize_preserves_records(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.add_goal(
            Goal(
                id="goal-001",
                description="learn",
                priority=5,
                status="ACTIVE",
            )
        )

        runtime.add_intention(
            Intention(
                id="intention-001",
                description="inspect object",
                status="ACTIVE",
                goal_id="goal-001",
            )
        )

        runtime.add_teaching(
            Teaching(
                id="teaching-001",
                content="trees have leaves",
                status="ACCEPTED",
            )
        )

        original = runtime.serialize()

        restored = TranscendingRuntime(
            cognitive=FakeCognitive()
        )
        restored.restore(original)

        self.assertEqual(
            restored.serialize(),
            original,
        )


if __name__ == "__main__":
    unittest.main()
