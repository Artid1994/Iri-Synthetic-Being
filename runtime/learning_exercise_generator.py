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
    def __init__(self) -> None:
        pass

    def generate(self, knowledge: str) -> LearningExercise:
        knowledge = knowledge.strip()

        if not knowledge:
            raise ValueError("KNOWLEDGE_CANNOT_BE_EMPTY")

        # Template-based exercise generation from knowledge
        # Extract key concepts and generate deterministic exercises

        # Simple heuristic: if knowledge contains numbers, create numerical exercise
        import re
        numbers = re.findall(r'\b\d+\b', knowledge)

        if numbers and len(numbers) >= 2:
            # Numerical exercise
            question = f"What is the sum mentioned in: {knowledge[:50]}?"
            expected_answer = str(sum(int(n) for n in numbers[:2]))
            verification_type = "NUMERICAL"
        else:
            # Exact match exercise based on key terms
            words = knowledge.split()
            if len(words) > 3:
                question = f"Complete the phrase from the knowledge: {' '.join(words[:3])} ___?"
                expected_answer = words[3] if len(words) > 3 else "unknown"
            else:
                question = f"What is the key concept in: {knowledge}?"
                expected_answer = knowledge.split()[0] if knowledge.split() else "unknown"
            verification_type = "EXACT"

        return LearningExercise(
            question=question,
            expected_answer=expected_answer,
            verification_type=verification_type,
        )
