from runtime.runtime import TranscendingRuntime
from runtime.body_command import BodyCommand
from runtime.robot_adapter import RobotAdapter


class Hardware:
    def __init__(self):
        self.calls = 0

    def execute(self, action, value):
        self.calls += 1
        return True


r = TranscendingRuntime(cognitive=None)
h = Hardware()
r.robot_adapter = RobotAdapter(h)

a = r.propose_action(BodyCommand("respond"))
assert a is not None
assert r.approve_pending_action()

first = r.execute_pending_action()
second = r.execute_pending_action()

assert first is not None
assert first[0] is True
assert second is None
assert h.calls == 1
assert r.pending_approval is None
assert r.pending_command is None

print("FIRST EXECUTION: PASS")
print("REPLAY BLOCK: PASS")
print("PENDING STATE CLEARED: PASS")
print("---")
print("TTF PENDING CLEANUP TEST: PASS")
