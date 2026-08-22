from __future__ import annotations


class AutonomousLoopController:
    def __init__(
        self,
        runtime,
        resource_guard,
        cooling,
        heartbeat,
    ) -> None:
        self.runtime = runtime
        self.resource_guard = resource_guard
        self.cooling = cooling
        self.heartbeat = heartbeat

        self.cycle_count = 0

    def step(self, observation, memory_usage=0.0):
        resource = self.resource_guard.evaluate(
            memory_usage
        )

        cooling = self.cooling.handle(
            resource.level
        )

        if cooling.action == "PAUSE":
            self.heartbeat.record_cycle(
                resource.level,
                "PAUSED",
            )

            return {
                "status": "PAUSED",
                "reason": resource.reason,
            }

        result = self.runtime.autonomous_step(
            observation
        )

        self.cycle_count += 1

        self.heartbeat.record_cycle(
            resource.level,
            "RUNNING",
        )

        return {
            "status": "RUNNING",
            "cycle": self.cycle_count,
            "result": result,
        }
