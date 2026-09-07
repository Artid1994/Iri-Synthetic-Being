# Phase 11 Autonomous Cognitive Loop Contract & Audit Reference

## Core Invariant
Autonomous cognitive execution is a deterministic closed-loop software controller:
`Observe → Interpret → Recall → Think → Decide → Act → Observe Result → Learn → Update State`

It must never claim consciousness, agency, free will, or subjective experience.

## Architectural Boundaries
1. **Safety Boundary Authority**:
   - `AutonomousPolicyGate` and `CognitiveSafetyGate` hold absolute override authority.
   - If autonomous mode is disabled or an action fails safety checks, embodiment execution is blocked before command dispatch.
2. **Decoupled Subsystems**:
   - `Goal` (objective state) and `Intention` (executable action referencing a goal) remain independent.
   - `Learning` and `Research` process feedback and explore without modifying Brain substrate internals.
   - `Brain` and `Memory` communicate only via explicit snapshot or synchronization contracts.
   - `Identity` and `SelfModel` record metrics without collapsing into cognitive engine prompts.

## Key Test Suite
- Closed-loop lifecycle: `tests/test_autonomous_cycle.py`, `tests/test_runtime_closed_autonomous_cycle.py`, `tests/test_runtime_autonomous_cycle.py`
- Policy gate enforcement: `tests/test_autonomous_policy_gate.py`, `tests/test_runtime_autonomous_policy_mode.py`, `tests/test_runtime_autonomous_policy_execution.py`
- Safety override: `tests/test_safe_runtime_control.py`, `tests/test_safe_runtime_integration.py`, `tests/test_safety_policy.py`
