from __future__ import annotations

from dataclasses import dataclass

from runtime.body_command import BodyCommand
from runtime.safety_event import SafetyEvent


@dataclass(frozen=True)
class SafetyPolicyDecision:
    blocked: bool
    reason: str


class SafetyPolicy:
    """
    Learned safety layer

    Policy เรียนรู้จาก safety event และทำหน้าที่เป็น safety
    layer เพิ่มเติม โดยไม่แก้ hard safety rules
    """

    def __init__(self) -> None:
        self._blocked_reasons: set[str] = set()
        self._blocked_commands: set[tuple[str, object]] = set()
        self._learned_actions: set[str] = set()

    def observe(self, event: SafetyEvent) -> None:
        if not isinstance(event, SafetyEvent):
            raise TypeError("event must be a SafetyEvent")

        if event.reason:
            self._blocked_reasons.add(event.reason)

        if event.action:
            self._learned_actions.add(event.action)

            try:
                value = event.value
                hash(value)
                self._blocked_commands.add(
                    (event.action, value)
                )
            except TypeError:
                pass

    def evaluate(
        self,
        reason: str,
    ) -> SafetyPolicyDecision:
        if not reason:
            return SafetyPolicyDecision(
                blocked=False,
                reason="NO_POLICY_MATCH",
            )

        if reason in self._blocked_reasons:
            return SafetyPolicyDecision(
                blocked=True,
                reason="POLICY_BLOCK",
            )

        return SafetyPolicyDecision(
            blocked=False,
            reason="NO_POLICY_MATCH",
        )

    def evaluate_command(
        self,
        command: BodyCommand | None,
    ) -> SafetyPolicyDecision:
        if not isinstance(command, BodyCommand):
            return SafetyPolicyDecision(
                blocked=False,
                reason="NO_POLICY_MATCH",
            )

        try:
            key = (command.action, command.value)

            if key in self._blocked_commands:
                return SafetyPolicyDecision(
                    blocked=True,
                    reason="POLICY_BLOCK",
                )
        except TypeError:
            pass

        return SafetyPolicyDecision(
            blocked=False,
            reason="NO_POLICY_MATCH",
        )

    def evaluate_learned_action(
        self,
        command: BodyCommand | None,
    ) -> SafetyPolicyDecision:
        if not isinstance(command, BodyCommand):
            return SafetyPolicyDecision(
                blocked=False,
                reason="NO_POLICY_MATCH",
            )

        if command.action in self._learned_actions:
            return SafetyPolicyDecision(
                blocked=True,
                reason="LEARNED_ACTION_BLOCK",
            )

        return SafetyPolicyDecision(
            blocked=False,
            reason="NO_POLICY_MATCH",
        )

    def snapshot(self) -> tuple[str, ...]:
        return tuple(sorted(self._blocked_reasons))

    def persistence_snapshot(self) -> dict:
        commands = []

        for action, value in sorted(
            self._blocked_commands,
            key=lambda item: (item[0], repr(item[1])),
        ):
            commands.append(
                {
                    "action": action,
                    "value": value,
                }
            )

        return {
            "blocked_reasons": tuple(
                sorted(self._blocked_reasons)
            ),
            "blocked_commands": commands,
            "learned_actions": tuple(
                sorted(self._learned_actions)
            ),
        }

    def restore(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        blocked_reasons = data.get(
            "blocked_reasons",
            (),
        )
        blocked_commands = data.get(
            "blocked_commands",
            (),
        )
        learned_actions = data.get(
            "learned_actions",
            (),
        )

        self._blocked_reasons = set(blocked_reasons)
        self._learned_actions = set(learned_actions)
        self._blocked_commands = set()

        for item in blocked_commands:
            if not isinstance(item, dict):
                raise TypeError(
                    "blocked command must be a dict"
                )

            action = item.get("action")
            value = item.get("value")

            try:
                hash(value)
            except TypeError as exc:
                raise TypeError(
                    "blocked command value must be hashable"
                ) from exc

            self._blocked_commands.add(
                (action, value)
            )
