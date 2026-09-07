"""Sleep Homeostasis and Autonomous Sleep Drive Module.

Tracks sleep pressure, fatigue accumulation, and sleep consolidation for Iri (AE01M).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional
import time


@dataclass
class SleepState:
    sleep_pressure: float
    state: str  # "ALERT", "DROWSY", "NEEDS_SLEEP"
    cycle_count: int
    working_memory_count: int
    last_consolidation_time: float


class SleepHomeostasis:
    def __init__(
        self,
        drowsy_threshold: float = 0.7,
        sleep_threshold: float = 0.9,
        pressure_per_cycle: float = 0.05,
        pressure_per_wm_item: float = 0.02,
    ) -> None:
        self.drowsy_threshold = drowsy_threshold
        self.sleep_threshold = sleep_threshold
        self.pressure_per_cycle = pressure_per_cycle
        self.pressure_per_wm_item = pressure_per_wm_item

        self.sleep_pressure: float = 0.0
        self.cycle_count: int = 0
        self.working_memory_count: int = 0
        self.last_consolidation_time: float = time.time()
        self.sleep_history: List[dict] = []

    @property
    def state(self) -> str:
        if self.sleep_pressure >= self.sleep_threshold:
            return "NEEDS_SLEEP"
        elif self.sleep_pressure >= self.drowsy_threshold:
            return "DROWSY"
        return "ALERT"

    def update_cycle(self, working_memory_count: int = 0) -> str:
        """Increment fatigue based on interaction cycles and working memory load."""
        self.cycle_count += 1
        self.working_memory_count = working_memory_count

        delta = self.pressure_per_cycle + (working_memory_count * self.pressure_per_wm_item)
        self.sleep_pressure = min(1.0, self.sleep_pressure + delta)
        return self.state

    def add_pressure(self, amount: float) -> str:
        """Directly add sleep pressure (useful for simulation or heavy cognitive load)."""
        self.sleep_pressure = min(1.0, max(0.0, self.sleep_pressure + amount))
        return self.state

    def consolidate_and_sleep(
        self,
        frontal_context: Optional[List[Any]] = None,
        memory_graph: Optional[Any] = None,
        runtime_memory: Optional[Any] = None,
    ) -> dict:
        """Execute sleep consolidation:

        1. Consolidate frontal context/working items into permanent semantic/episodic memory.
        2. Apply synaptic pruning / clear transient working memory.
        3. Reset sleep pressure to 0.0.
        4. Generate Wakeup Report for 'เจ้านาย'.
        """
        consolidated_items_count = 0
        pruned_items_count = 0

        # Consolidate working items into permanent memory
        if frontal_context and memory_graph is not None:
            for item in frontal_context:
                content = str(item)
                try:
                    memory_graph.add_node(f"SEMANTIC:SLEEP_CONSOLIDATION:{content[:30]}", "SEMANTIC")
                    consolidated_items_count += 1
                except Exception:
                    pass

        # Clear working memory buffer if accessible
        if runtime_memory is not None:
            if hasattr(runtime_memory, "state") and hasattr(runtime_memory.state, "working"):
                pruned_items_count = len(runtime_memory.state.working)
                runtime_memory.state.working.clear()
            elif hasattr(runtime_memory, "working"):
                pruned_items_count = len(runtime_memory.working)
                if hasattr(runtime_memory, "clear_working"):
                    runtime_memory.clear_working()
                elif isinstance(runtime_memory.working, list):
                    runtime_memory.working.clear()

        # Reset homeostasis state
        old_pressure = self.sleep_pressure
        self.sleep_pressure = 0.0
        self.working_memory_count = 0
        self.last_consolidation_time = time.time()

        wakeup_report = {
            "recipient": "เจ้านาย",
            "entity": "Iri (AE01M)",
            "status": "REFRESHED",
            "previous_pressure": old_pressure,
            "current_pressure": 0.0,
            "consolidated_items": consolidated_items_count,
            "pruned_transient_items": pruned_items_count,
            "message": (
                "ไอริตื่นนอนและประมวลผลความจำระยะยาวเรียบร้อยแล้วค่ะเจ้านาย! "
                "สมองของไอริกลับมาสดชื่น 100% พร้อมลุยงานต่อแล้วค่ะ"
            ),
        }

        self.sleep_history.append(wakeup_report)
        return wakeup_report

    def snapshot(self) -> SleepState:
        return SleepState(
            sleep_pressure=self.sleep_pressure,
            state=self.state,
            cycle_count=self.cycle_count,
            working_memory_count=self.working_memory_count,
            last_consolidation_time=self.last_consolidation_time,
        )


default_sleep_homeostasis = SleepHomeostasis()
