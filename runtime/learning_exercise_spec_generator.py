from __future__ import annotations

from dataclasses import dataclass

from runtime.learning_exercise_spec import LearningExerciseSpec


@dataclass(frozen=True)
class LearningExerciseSpecProposal:
    question: str
    expression: str

    @classmethod
    def parse(cls, output: str) -> "LearningExerciseSpecProposal":
        question = ""
        expression = ""

        for line in output.splitlines():
            key, separator, value = line.partition(":")

            if not separator:
                continue

            key = key.strip().lower()
            value = value.strip()

            if key == "question":
                question = value
            elif key == "expression":
                expression = value

        if not question or not expression:
            raise ValueError("INVALID_LEARNING_EXERCISE_SPEC")

        return cls(
            question=question,
            expression=expression,
        )


class LearningExerciseSpecGenerator:
    def __init__(self, inference) -> None:
        self.inference = inference

    def generate(self, knowledge: str) -> LearningExerciseSpec:
        knowledge = knowledge.strip()

        if not knowledge:
            raise ValueError("KNOWLEDGE_CANNOT_BE_EMPTY")

        prompt = (
            "Create one simple mathematical learning exercise "
            "from the knowledge below.\n"
            f"Knowledge: {knowledge}\n"
            "\n"
            "The exercise must use a simple mathematical expression "
            "that the system can verify.\n"
            "Do not provide the answer.\n"
            "Do not provide explanations.\n"
            "\n"
            "Return exactly two lines:\n"
            "Question: <question>\n"
            "Expression: <mathematical expression>"
        )

        output = self.inference(prompt)

        proposal = LearningExerciseSpecProposal.parse(output)

        return LearningExerciseSpec(
            question=proposal.question,
            expression=proposal.expression,
        )
