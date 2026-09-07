import pytest
from importlib.machinery import SourceFileLoader
import os

from runtime.memory import Memory
from runtime.memory_graph import MemoryGraph


def get_sleep_homeostasis_class():
    path = os.path.join(os.path.dirname(__file__), "..", "00_BrainStem", "sleep_homeostasis.py")
    mod = SourceFileLoader("sleep_homeostasis", path).load_module()
    return mod.SleepHomeostasis


def test_sleep_pressure_accumulation_and_thresholds():
    SleepHomeostasis = get_sleep_homeostasis_class()
    sh = SleepHomeostasis(drowsy_threshold=0.7, sleep_threshold=0.9, pressure_per_cycle=0.2)

    assert sh.sleep_pressure == 0.0
    assert sh.state == "ALERT"

    # Cycle 1 -> 0.2
    sh.update_cycle()
    assert sh.state == "ALERT"

    # Cycle 2 -> 0.4
    sh.update_cycle()
    assert sh.state == "ALERT"

    # Cycle 3 -> 0.6
    sh.update_cycle()
    assert sh.state == "ALERT"

    # Cycle 4 -> 0.8 -> DROWSY
    sh.update_cycle()
    assert sh.state == "DROWSY"

    # Cycle 5 -> 1.0 -> NEEDS_SLEEP
    sh.update_cycle()
    assert sh.state == "NEEDS_SLEEP"


def test_sleep_consolidation_and_reset():
    SleepHomeostasis = get_sleep_homeostasis_class()
    sh = SleepHomeostasis()
    sh.add_pressure(0.95)
    assert sh.state == "NEEDS_SLEEP"

    memory = Memory()
    memory_graph = MemoryGraph()
    memory.add_working("Recent lesson on fractions")
    memory.add_working("Chat context with เจ้านาย")

    assert len(memory.state.working) == 2

    frontal_context = ["Active goal: research physics", "Unconsolidated thought 1"]

    report = sh.consolidate_and_sleep(
        frontal_context=frontal_context,
        memory_graph=memory_graph,
        runtime_memory=memory,
    )

    # Verification of reset
    assert sh.sleep_pressure == 0.0
    assert sh.state == "ALERT"
    assert report["recipient"] == "เจ้านาย"
    assert report["current_pressure"] == 0.0
    assert report["consolidated_items"] == 2
    assert report["pruned_transient_items"] == 2
    assert len(memory.state.working) == 0

    # Ensure consolidated items exist in permanent memory graph
    assert any("SLEEP_CONSOLIDATION" in n for n in memory_graph.nodes)
