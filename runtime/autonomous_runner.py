from __future__ import annotations

import threading
import time


class AutonomousRunner:
    def __init__(
        self,
        loop_controller,
        interval: float = 1.0,
        failure_limit: int = 3,
    ) -> None:
        self.loop_controller = loop_controller
        self.interval = max(0.0, interval)
        self.failure_limit = max(1, failure_limit)

        self.running = False
        self.cycle_count = 0
        self.last_result = None

        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._failure_counts: dict[str, int] = {}
        self._paused_tasks: set[str] = set()

    @staticmethod
    def _task_key(observation) -> str:
        return str(observation)

    @staticmethod
    def _is_failure(result) -> bool:
        if not isinstance(result, dict):
            return False

        return result.get("status") in {
            "FAILED",
            "ERROR",
        }

    def _step(self, observation, memory_usage: float = 0.0):
        result = self.loop_controller.step(
            observation,
            memory_usage,
        )

        self.cycle_count += 1
        self.last_result = result

        key = self._task_key(observation)

        if self._is_failure(result):
            failures = self._failure_counts.get(key, 0) + 1
            self._failure_counts[key] = failures

            if failures >= self.failure_limit:
                self._paused_tasks.add(key)
                return {
                    **result,
                    "status": "TASK_PAUSED",
                    "reason": "CIRCUIT_BREAKER",
                    "failures": failures,
                }
        else:
            self._failure_counts.pop(key, None)

        return result

    def run(
        self,
        observation,
        max_cycles: int = 1,
        memory_usage: float = 0.0,
    ):
        self.running = True
        self._stop_event.clear()

        results = []

        for _ in range(max_cycles):
            if not self.running or self._stop_event.is_set():
                break

            key = self._task_key(observation)

            if key in self._paused_tasks:
                break

            result = self._step(
                observation,
                memory_usage,
            )

            results.append(result)

            if result.get("status") == "TASK_PAUSED":
                break

            if self.interval:
                time.sleep(self.interval)

        self.running = False
        return results

    def run_goals(
        self,
        runtime,
        max_cycles: int = 50,
        auto_chain: bool = True,
        safety_stop_callback=None,
    ) -> list:
        self.running = True
        self._stop_event.clear()

        results = []
        executed_counts: dict[str, int] = {}

        for _ in range(max_cycles):
            if not self.running or self._stop_event.is_set():
                break

            if safety_stop_callback and safety_stop_callback():
                break

            active_goals = [g for g in getattr(runtime, "goals", []) if g.status == "ACTIVE"]
            if not active_goals:
                break

            # Deterministic selection: highest priority, FIFO tie-breaking
            selected_goal = max(active_goals, key=lambda g: g.priority)

            # Circuit breaker against infinite execution loops without progress
            key = selected_goal.id
            if key in self._paused_tasks:
                break

            current_failures = self._failure_counts.get(key, 0)
            if current_failures >= self.failure_limit:
                self._paused_tasks.add(key)
                selected_goal.pause()
                results.append({
                    "status": "TASK_PAUSED",
                    "reason": "CIRCUIT_BREAKER",
                    "goal": selected_goal,
                })
                break

            result = runtime.run_goal_learning_step(selected_goal, auto_chain=auto_chain)
            self.cycle_count += 1
            self.last_result = result

            # Evaluate success / failure for circuit breaker and completion
            is_success = False
            learning_res = getattr(result, "learning_result", None)
            if learning_res and getattr(learning_res, "memory_updated", False):
                is_success = True
            elif getattr(result, "reflection", None) and getattr(result.reflection, "outcome", None) == "SUCCESS":
                is_success = True

            if is_success:
                selected_goal.complete()
                self._failure_counts.pop(key, None)
                # Auto-resume parent goal if this was a chained child
                if hasattr(runtime, "_resume_parent_goal_if_any"):
                    runtime._resume_parent_goal_if_any(selected_goal)
            else:
                # If outcome is missing knowledge and generated a chained child goal, pause parent goal
                if getattr(result, "reflection", None) and getattr(result.reflection, "outcome", None) == "MISSING_KNOWLEDGE":
                    selected_goal.pause()
                else:
                    failures = current_failures + 1
                    self._failure_counts[key] = failures
                    if failures >= self.failure_limit:
                        self._paused_tasks.add(key)
                        selected_goal.pause()
                        results.append(result)
                        results.append({
                            "status": "TASK_PAUSED",
                            "reason": "CIRCUIT_BREAKER",
                            "goal": selected_goal,
                        })
                        break


            results.append(result)

            if self.interval:
                time.sleep(self.interval)

        self.running = False
        return results

    def start(
        self,
        observation,
        max_cycles: int = 0,
        memory_usage: float = 0.0,
    ) -> None:
        if self.running:
            return

        self._thread = threading.Thread(
            target=self.run,
            args=(observation, max_cycles or 2**63 - 1, memory_usage),
            daemon=True,
        )
        self._thread.start()

    def join(self, timeout: float | None = None) -> None:
        if self._thread is not None:
            self._thread.join(timeout)

    def stop(self) -> None:
        self.running = False
        self._stop_event.set()

    def paused_tasks(self) -> set[str]:
        return set(self._paused_tasks)