from __future__ import annotations


class ResearchPrompt:

    @staticmethod
    def build(summary: dict) -> str:
        return (
            "Analyze the research result and propose the next "
            "testable hypothesis and candidate model.\n\n"
            f"Hypothesis: {summary.get('hypothesis', '')}\n"
            f"Objective: {summary.get('objective', '')}\n"
            f"Best model: {summary.get('best_model', '')}\n"
            f"Exponential error: {summary.get('exponential_error', '')}\n"
            f"Linear error: {summary.get('linear_error', '')}\n\n"
            "Return a hypothesis and model proposal only.\n"
            "Do not execute code.\n"
            "Do not claim the result is a physical discovery."
        )
