import unittest

from runtime.runtime import TranscendingRuntime
from runtime.safety_event import SafetyEvent
from runtime.body_command import BodyCommand


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"

    def snapshot(self):
        return {}


class TestRuntimeSafetyPolicyPersistence(unittest.TestCase):
    def test_snapshot_restore_preserves_learned_safety_state(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.memory.add_safety_event(
            SafetyEvent(
                action="move",
                value=(2.0, 0.0),
                reason="move_limit_exceeded",
            )
        )

        runtime._sync_safety_policy()

        snapshot = runtime.snapshot()

        restored = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        restored.restore(snapshot)

        self.assertTrue(
            restored.safety_policy.evaluate(
                "move_limit_exceeded"
            ).blocked
        )

        self.assertTrue(
            restored.safety_policy.evaluate_command(
                BodyCommand(
                    action="move",
                    value=(2.0, 0.0),
                )
            ).blocked
        )

        self.assertTrue(
            restored.safety_policy.evaluate_learned_action(
                BodyCommand(
                    action="move",
                    value=(1.0, 0.0),
                )
            ).blocked
        )


if __name__ == "__main__":
    unittest.main()
