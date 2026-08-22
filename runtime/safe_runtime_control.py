from __future__ import annotations


class SafeRuntimeControl:
    def __init__(
        self,
        runner,
    ) -> None:
        self.runner = runner
        self.running = False

    def start(
        self,
        observation,
        max_cycles=1,
        memory_usage=0.0,
    ):
        self.running = True

        if not self.running:
            return []

        result = self.runner.run(
            observation,
            max_cycles=max_cycles,
            memory_usage=memory_usage,
        )

        self.running = False

        return result

    def stop(self) -> None:
        self.running = False

    def is_running(self) -> bool:
        return self.running
