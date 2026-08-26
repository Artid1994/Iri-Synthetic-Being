from __future__ import annotations

from dataclasses import dataclass

from runtime.learning_task import LearningTask
from runtime.research_learning import ResearchLearning
from runtime.research_safety import ResearchSafetyGate
from runtime.web_research import ResearchResult


@dataclass(frozen=True)
class AutonomousLearningResult:
    topic: str
    status: str
    reason: str
    memory_updated: bool


class AutonomousLearning:
    def __init__(
        self,
        research,
        research_learning: ResearchLearning,
        safety_gate: ResearchSafetyGate | None = None,
    ) -> None:
        self.research = research
        self.research_learning = research_learning
        self.safety_gate = safety_gate or ResearchSafetyGate()

    def learn(
        self,
        task: LearningTask,
        category: str = "GENERAL",
    ) -> AutonomousLearningResult:
        if not isinstance(task, LearningTask):
            raise TypeError("task must be a LearningTask")

        if task.status != "PENDING":
            return AutonomousLearningResult(
                topic=task.topic,
                status=task.status,
                reason="TASK_NOT_PENDING",
                memory_updated=False,
            )

        task.start()

        try:
            result = self.research.search(task.topic)

            if not isinstance(result, ResearchResult):
                task.status = "PENDING"
                return AutonomousLearningResult(
                    topic=task.topic,
                    status="PENDING",
                    reason="INVALID_RESEARCH_RESULT",
                    memory_updated=False,
                )

            safety = self.safety_gate.evaluate(
                result,
                category=category,
            )

            if not safety.accepted:
                task.status = "PENDING"
                return AutonomousLearningResult(
                    topic=task.topic,
                    status="PENDING",
                    reason=safety.reason,
                    memory_updated=False,
                )

            evaluation = self.research_learning.evaluate(result)

            if not evaluation.accepted:
                task.status = "PENDING"
                return AutonomousLearningResult(
                    topic=task.topic,
                    status="PENDING",
                    reason=evaluation.reason,
                    memory_updated=False,
                )

            task.complete()

            return AutonomousLearningResult(
                topic=task.topic,
                status=task.status,
                reason=evaluation.reason,
                memory_updated=True,
            )

        except Exception:
            task.status = "PENDING"
            raise
