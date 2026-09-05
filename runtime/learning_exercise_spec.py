from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class LearningExerciseSpec:
    question: str
    expression: str

    def __post_init__(self) -> None:
        if not self.question.strip():
            raise ValueError(
                "Learning exercise question cannot be empty"
            )

        expression = self.expression.strip()

        if not expression:
            raise ValueError(
                "Learning exercise expression cannot be empty"
            )

        try:
            ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError(
                "Invalid learning exercise expression"
            ) from exc
