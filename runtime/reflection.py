from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReflectionResult:
    outcome: str
    lesson: str
    next_task: str | None


class Reflection:
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    MISSING_KNOWLEDGE = "MISSING_KNOWLEDGE"

    def reflect(
        self,
        outcome: str,
        observation: str = "",
        task_topic: str = "",
    ) -> ReflectionResult:
        outcome = outcome.strip().upper()
        observation = observation.strip()
        task_topic = task_topic.strip()

        if outcome == self.SUCCESS:
            lesson = observation or f"Task completed: {task_topic}"
            return ReflectionResult(
                outcome=self.SUCCESS,
                lesson=lesson,
                next_task=None,
            )

        if outcome == self.MISSING_KNOWLEDGE:
            next_task = (
                f"Research missing knowledge for: {task_topic}"
                if task_topic
                else "Research missing knowledge"
            )
            return ReflectionResult(
                outcome=self.MISSING_KNOWLEDGE,
                lesson=observation or "Knowledge was insufficient",
                next_task=next_task,
            )

        return ReflectionResult(
            outcome=self.FAILURE,
            lesson=observation or f"Task failed: {task_topic}",
            next_task=(
                f"Investigate failure of: {task_topic}"
                if task_topic
                else "Investigate previous failure"
            ),
        )
