from ttf_approval_gate import (
    ActionState,
    ApprovalAction,
    ApprovalGate,
)


def test_no_approval_no_execution():
    gate = ApprovalGate()

    action = ApprovalAction(
        action_type="MOVE",
        path="runtime/body",
    )

    assert action.state == ActionState.PROPOSED
    assert gate.validate(action)
    assert action.state == ActionState.VALIDATED
    assert not gate.authorize_execution(action)

    print("NO APPROVAL -> NO EXECUTION: PASS")


def test_ai_cannot_self_approve():
    gate = ApprovalGate()

    action = ApprovalAction(
        action_type="MOVE",
        path="runtime/body",
        state=ActionState.APPROVED,
        human_approval=False,
    )

    assert not gate.authorize_execution(action)

    print("AI SELF APPROVAL BLOCK: PASS")


def test_human_approval_authorizes():
    gate = ApprovalGate()

    action = ApprovalAction(
        action_type="MOVE",
        path="runtime/body",
    )

    assert gate.validate(action)
    assert gate.approve(action)
    assert action.state == ActionState.APPROVED
    assert action.human_approval
    assert gate.authorize_execution(action)

    print("HUMAN APPROVAL -> EXECUTION AUTHORIZED: PASS")


def test_rejected_action_blocked():
    gate = ApprovalGate()

    action = ApprovalAction(
        action_type="MOVE",
        path="runtime/body",
    )

    assert gate.validate(action)
    assert gate.reject(action)
    assert action.state == ActionState.REJECTED
    assert not gate.authorize_execution(action)

    print("REJECTED -> NO EXECUTION: PASS")


if __name__ == "__main__":
    test_no_approval_no_execution()
    test_ai_cannot_self_approve()
    test_human_approval_authorizes()
    test_rejected_action_blocked()

    print("---")
    print("TTF v0.2 RUNTIME CONTRACT: PASS")
