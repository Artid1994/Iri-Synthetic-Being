from __future__ import annotations

from dataclasses import dataclass

from runtime.goal import Goal
from runtime.learning_task import LearningTask
from runtime.reflection import Reflection, ReflectionResult


@dataclass(frozen=True)
class AutonomousStepResult:
    goal: Goal
    learning_task: LearningTask
    learning_result: object
    reflection: ReflectionResult
    next_task: LearningTask | None


class AutonomousStep:
    def __init__(
        self,
        goal_learning,
        reflection: Reflection | None = None,
    ) -> None:
        self.goal_learning = goal_learning
        self.reflection = reflection or Reflection()

    def run(self, goal: Goal) -> AutonomousStepResult:
        if not isinstance(goal, Goal):
            raise TypeError("goal must be a Goal")

        task = LearningTask(goal.description)

        result = self.goal_learning.autonomous_learning.learn(task)

        if result.memory_updated:
            task.status = "COMPLETED"
            outcome = Reflection.SUCCESS
        elif result.reason in {
            "EMPTY_RESEARCH_CONTENT",
            "INVALID_RESEARCH_RESULT",
            "CONFIDENCE_TOO_LOW",
            "NO_CANDIDATE",
        }:
            outcome = Reflection.MISSING_KNOWLEDGE
        else:
            outcome = Reflection.FAILURE

        reflection = self.reflection.reflect(
            outcome=outcome,
            observation=result.reason,
            task_topic=task.topic,
        )

        next_task = None

        if reflection.next_task:
            next_task = LearningTask(reflection.next_task)

        return AutonomousStepResult(
            goal=goal,
            learning_task=task,
            learning_result=result,
            reflection=reflection,
            next_task=next_task,
        )
