from __future__ import annotations


class ResearchPrompt:

    @staticmethod
    def build(summary: dict, previous_result: dict | None = None) -> str:
        previous_text = ""
        if previous_result is not None:
            previous_text = (
                "\nPrevious:\n"
                f"Model: {previous_result.get('model', '')}\n"
                f"Error: {previous_result.get('error', '')}\n"
            )

        return (
            "Propose the next testable research hypothesis and model.\n"
            f"Hypothesis: {summary.get('hypothesis', '')}\n"
            f"Best model: {summary.get('best_model', '')}\n"
            f"Exponential error: {summary.get('exponential_error', '')}\n"
            f"Linear error: {summary.get('linear_error', '')}\n"
            f"{previous_text}\n"
            "Return exactly two lines:\n"
            "Hypothesis: <testable hypothesis>\n"
            "Model Proposal: Exponential model OR Linear model\n"
            "Do not execute code."
        )
