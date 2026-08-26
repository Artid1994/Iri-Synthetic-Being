from __future__ import annotations

from runtime.autonomous_learning import (
    AutonomousLearning,
    AutonomousLearningResult,
)
from runtime.goal import Goal
from runtime.learning_task import LearningTask


class GoalLearning:
    def __init__(
        self,
        autonomous_learning: AutonomousLearning,
        development=None,
    ) -> None:
        self.autonomous_learning = autonomous_learning
        self.development = development

    def learn_goal(
        self,
        goal: Goal,
    ) -> AutonomousLearningResult:
        if not isinstance(goal, Goal):
            raise TypeError("goal must be a Goal")

        if goal.status != "ACTIVE":
            return AutonomousLearningResult(
                topic=goal.description,
                status=goal.status,
                reason="GOAL_NOT_ACTIVE",
                memory_updated=False,
            )

        task = LearningTask(goal.description)

        result = self.autonomous_learning.learn(task)

        if (
            result.memory_updated
            and self.development is not None
        ):
            self.development.sync()

        return result
