import unittest

from runtime.memory import Memory
from runtime.safety_event import SafetyEvent


class TestSafetyEventMemory(unittest.TestCase):
    def test_safety_event_is_stored(self):
        memory = Memory()

        event = SafetyEvent(
            action="move",
            value=(2.0, 0.0),
            reason="move_limit_exceeded",
        )

        memory.add_safety_event(event)

        self.assertEqual(
            memory.state.safety_events,
            [event],
        )

    def test_invalid_safety_event_is_rejected(self):
        memory = Memory()

        with self.assertRaises(TypeError):
            memory.add_safety_event("invalid")

    def test_snapshot_copies_safety_events(self):
        memory = Memory()

        event = SafetyEvent(
            action="move",
            value=(2.0, 0.0),
            reason="move_limit_exceeded",
        )

        memory.add_safety_event(event)

        snapshot = memory.snapshot()
        snapshot.safety_events.clear()

        self.assertEqual(
            memory.state.safety_events,
            [event],
        )


if __name__ == "__main__":
    unittest.main()
