from __future__ import annotations


class ResearchLoop:
    def __init__(self, research) -> None:
        self.research = research

    def run(
        self,
        coupling_values: list[float],
        max_cycles: int = 1,
    ) -> list[dict[str, object]]:
        results = []
        previous_result = None

        for _ in range(max(0, max_cycles)):
            result = self.research.run(
                coupling_values,
                previous_result=previous_result,
            )
            results.append(result)

            if result.get("status") in {"FAILED", "ERROR", "REJECTED"}:
                break

            previous_result = result

        return results
