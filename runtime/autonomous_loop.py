from __future__ import annotations


class AutonomousLoopController:
    def __init__(
        self,
        runtime,
        resource_guard,
        cooling,
        heartbeat,
        error_recovery=None,
        heartbeat_storage=None,
    ) -> None:
        self.runtime = runtime
        self.resource_guard = resource_guard
        self.cooling = cooling
        self.heartbeat = heartbeat
        self.error_recovery = error_recovery
        self.heartbeat_storage = heartbeat_storage

        self.cycle_count = 0

    def _save_heartbeat(self):
        if self.heartbeat_storage is None:
            return

        self.heartbeat_storage.save(
            self.heartbeat.snapshot()
        )

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

            self._save_heartbeat()

            return {
                "status": "PAUSED",
                "reason": resource.reason,
            }

        try:
            result = self.runtime.autonomous_step(
                observation
            )

        except Exception as exc:
            if self.error_recovery is None:
                raise

            decision = self.error_recovery.handle(
                str(exc)
            )

            self.heartbeat.record_cycle(
                resource.level,
                decision.action,
            )

            self._save_heartbeat()

            return {
                "status": decision.action,
                "attempt": decision.attempt,
                "error": decision.reason,
            }

        memory = getattr(self.runtime, "memory", None)
        if memory is not None:
            memory.prune()

        self.cycle_count += 1

        self.heartbeat.record_cycle(
            resource.level,
            "RUNNING",
        )

        self._save_heartbeat()

        return {
            "status": "RUNNING",
            "cycle": self.cycle_count,
            "result": result,
        }
