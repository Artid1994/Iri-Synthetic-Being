from runtime.body_command import BodyCommand
from runtime.runtime import TranscendingRuntime


class FakeHardware:
    def __init__(self):
        self.calls = []

    def execute(self, action, value):
        self.calls.append((action, value))
        return True


runtime = TranscendingRuntime(cognitive=None)
hardware = FakeHardware()
runtime.robot_adapter.hardware = hardware

command = BodyCommand(
    action="respond",
    value=None,
)

action = runtime.propose_action(command)

assert action is not None
assert action.state.value == "VALIDATED"

result = runtime.execute_pending_action()

assert result is None
assert hardware.calls == []

assert runtime.approve_pending_action()

result = runtime.execute_pending_action()

assert result is not None
assert result[0] is True
assert len(hardware.calls) == 1

print("NO APPROVAL -> NO EXECUTION: PASS")
print("HUMAN APPROVAL -> EXECUTION: PASS")
print("HARDWARE EXECUTED:", hardware.calls)
print("---")
print("TTF v0.2 RUNTIME APPROVAL INTEGRATION: PASS")
