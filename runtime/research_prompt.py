from __future__ import annotations


class ResearchPrompt:

    @staticmethod
    def build(summary: dict, previous_result: dict | None = None) -> str:
        previous_text = ""
        if previous_result is not None:
            previous_text = (
                "\nPrevious result:\n"
                f"Model: {previous_result.get('model', '')}\n"
                f"Error: {previous_result.get('error', '')}\n"
                f"Status: {previous_result.get('status', '')}\n"
            )
        return (
            "Analyze the research result and propose the next "
            "testable hypothesis and candidate model.\n\n"
            f"Hypothesis: {summary.get('hypothesis', '')}\n"
            f"Objective: {summary.get('objective', '')}\n"
            f"Best model: {summary.get('best_model', '')}\n"
            f"Exponential error: {summary.get('exponential_error', '')}\n"
            f"Linear error: {summary.get('linear_error', '')}\n\n"
            f"{previous_text}\n"
            "Return EXACTLY two lines and nothing else:\n"
            "Hypothesis: <testable hypothesis>\n"
            "Model Proposal: Exponential model OR Linear model\n"
            "Do not add explanations, analysis, or markdown.\n"
            "Do not execute code.\n"
            "Do not claim the result is a physical discovery."
        )
