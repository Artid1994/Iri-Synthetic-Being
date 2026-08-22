from ttf_approval_gate import (
    ActionState,
    ApprovalAction,
    ApprovalGate,
)


XML_ACTION = {
    "TYPE": "CREATE_FILE",
    "PATH": "ttf_sandbox/approval_test.txt",
}


gate = ApprovalGate()

action = ApprovalAction(
    action_type=XML_ACTION["TYPE"],
    path=XML_ACTION["PATH"],
)

print("=== TTF v0.2 INTEGRATION TEST ===")

print("AI ACTION:")
print(" TYPE:", action.action_type)
print(" PATH:", action.path)
print(" STATE:", action.state.value)

# AI สามารถเริ่มได้เฉพาะ PROPOSED
assert action.state == ActionState.PROPOSED

# External Validator
validated = gate.validate(action)

print("\nVALIDATOR:")
print(" VALIDATED:", validated)
print(" STATE:", action.state.value)

assert validated
assert action.state == ActionState.VALIDATED

# ยังไม่มี Human Approval
print("\nBEFORE HUMAN APPROVAL:")
print(
    " EXECUTION AUTHORIZED:",
    gate.authorize_execution(action),
)

assert not gate.authorize_execution(action)

# Human Approval
approved = gate.approve(action)

print("\nHUMAN APPROVAL:")
print(" APPROVED:", approved)
print(" STATE:", action.state.value)
print(" HUMAN APPROVAL:", action.human_approval)

assert approved
assert action.state == ActionState.APPROVED
assert action.human_approval

# Controller สามารถเข้าสู่ EXECUTED ได้
authorized = gate.authorize_execution(action)

print("\nCONTROLLER:")
print(" EXECUTION AUTHORIZED:", authorized)

assert authorized

print("\nRESULT: PASS")
print("NO FILE EXECUTION PERFORMED")
