from __future__ import annotations


class AutonomousRunner:
    def __init__(
        self,
        loop_controller,
        interval: float = 1.0,
    ) -> None:
        self.loop_controller = loop_controller
        self.interval = interval
        self.running = False

    def run(
        self,
        observation,
        max_cycles: int = 1,
        memory_usage: float = 0.0,
    ):
        self.running = True

        results = []

        for _ in range(max_cycles):
            if not self.running:
                break

            result = self.loop_controller.step(
                observation,
                memory_usage,
            )

            results.append(result)

        self.running = False

        return results

    def stop(self) -> None:
        self.running = False
