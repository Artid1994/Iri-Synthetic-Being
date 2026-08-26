from __future__ import annotations

from runtime.learning_task import LearningTask


class SelfDirectedLearning:
    def __init__(self) -> None:
        self._tasks: list[LearningTask] = []

    def create_task(
        self,
        need: str,
    ) -> LearningTask | None:
        need = need.strip()

        if not need:
            return None

        for task in self._tasks:
            if task.topic == need and task.status in {
                "PENDING",
                "ACTIVE",
            }:
                return None

        task = LearningTask(need)
        self._tasks.append(task)

        return task

    def from_reflection(self, reflection):
        if reflection is None:
            return None

        next_task = getattr(reflection, "next_task", None)

        if not next_task:
            return None

        return self.create_task(next_task)

    def next_task(self) -> LearningTask | None:
        for task in self._tasks:
            if task.status == "PENDING":
                task.start()
                return task

        return None
