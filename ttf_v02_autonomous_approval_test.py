from runtime.body_command import BodyCommand
from runtime.robot_adapter import RobotAdapter
from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "autonomous reasoning"


class FakeHardware:
    def __init__(self):
        self.calls = []

    def execute(self, action, value):
        self.calls.append((action, value))
        return True


runtime = TranscendingRuntime(
    cognitive=FakeCognitive()
)

hardware = FakeHardware()
runtime.robot_adapter = RobotAdapter(hardware)
runtime.autonomous_controller.enable()

command = BodyCommand(
    action="respond",
    value=None,
)

action = runtime.propose_action(command)

assert action is not None
assert action.state.value == "VALIDATED"

assert runtime.execute_pending_action() is None
assert hardware.calls == []

assert runtime.approve_pending_action()

result = runtime.execute_pending_action()

assert result is not None
assert result[0] is True
assert hardware.calls == [("respond", None)]

print("AUTONOMOUS APPROVAL REQUIRED: PASS")
print("HUMAN APPROVAL -> EXECUTION: PASS")
print("---")
print("TTF AUTONOMOUS APPROVAL CONTRACT: PASS")
