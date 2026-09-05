from __future__ import annotations

from dataclasses import dataclass

from runtime.learning_exercise import LearningExercise


@dataclass(frozen=True)
class LearningExerciseProposal:
    question: str
    expected_answer: str
    verification_type: str

    SUPPORTED_VERIFICATION_TYPES = {
        "EXACT",
        "NUMERICAL",
    }

    @classmethod
    def parse(cls, output: str) -> "LearningExerciseProposal":
        question = ""
        expected_answer = ""
        verification_type = ""

        for line in output.splitlines():
            key, separator, value = line.partition(":")

            if not separator:
                continue

            key = key.strip().lower()
            value = value.strip()

            if key == "question":
                question = value
            elif key == "expected answer":
                expected_answer = value
            elif key == "verification type":
                verification_type = value.upper()

        if not question or not expected_answer:
            raise ValueError("INVALID_LEARNING_EXERCISE")

        if verification_type not in cls.SUPPORTED_VERIFICATION_TYPES:
            raise ValueError(
                "INVALID_VERIFICATION_TYPE"
            )

        return cls(
            question=question,
            expected_answer=expected_answer,
            verification_type=verification_type,
        )


class LearningExerciseGenerator:
    def __init__(self, inference) -> None:
        self.inference = inference

    def generate(self, knowledge: str) -> LearningExercise:
        knowledge = knowledge.strip()

        if not knowledge:
            raise ValueError("KNOWLEDGE_CANNOT_BE_EMPTY")

        prompt = (
            "Create one learning exercise from the knowledge below.\n"
            f"Knowledge: {knowledge}\n"
            "\n"
            "The exercise must have an objectively verifiable answer.\n"
            "Use EXACT for exact text answers.\n"
            "Use NUMERICAL for numerical answers.\n"
            "\n"
            "Return exactly three lines:\n"
            "Question: <question>\n"
            "Expected Answer: <answer>\n"
            "Verification Type: EXACT or NUMERICAL\n"
            "Do not execute code."
        )

        output = self.inference(prompt)

        proposal = LearningExerciseProposal.parse(output)

        return LearningExercise(
            question=proposal.question,
            expected_answer=proposal.expected_answer,
            verification_type=proposal.verification_type,
        )
