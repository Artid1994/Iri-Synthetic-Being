from ttf_approval_gate import ActionState, ApprovalAction, ApprovalGate
from ttf_execution_adapter import ExecutionAdapter


gate = ApprovalGate()
adapter = ExecutionAdapter(gate)


def executor(action):
    return f"EXECUTED:{action.action_type}"


action = ApprovalAction("MOVE", "runtime/body")

ok, _ = adapter.execute(action, executor)
assert not ok
assert action.state == ActionState.PROPOSED

assert gate.validate(action)

ok, _ = adapter.execute(action, executor)
assert not ok
assert action.state == ActionState.VALIDATED

assert gate.approve(action)

ok, result = adapter.execute(action, executor)
assert ok
assert result == "EXECUTED:MOVE"
assert action.state == ActionState.EXECUTED

print("NO APPROVAL BLOCK: PASS")
print("VALIDATED BLOCK: PASS")
print("APPROVED EXECUTION: PASS")
print("STATE EXECUTED: PASS")
print("---")
print("TTF EXECUTION ADAPTER TEST: PASS")


def failing_executor(action):
    raise RuntimeError("test failure")


failed_action = ApprovalAction("MOVE", "runtime/body")

assert gate.validate(failed_action)
assert gate.approve(failed_action)

ok, error = adapter.execute(
    failed_action,
    failing_executor,
)

assert not ok
assert failed_action.state == ActionState.FAILED
assert "EXECUTION FAILED" in error

print("EXECUTOR FAILURE -> FAILED: PASS")
print("---")
print("TTF EXECUTION ADAPTER FAILURE TEST: PASS")
