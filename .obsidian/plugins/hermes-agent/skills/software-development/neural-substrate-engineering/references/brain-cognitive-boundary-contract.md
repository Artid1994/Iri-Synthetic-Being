# Phase 8: Brain ↔ Cognitive Core Boundary Contract

This document captures the verified boundary architecture between the Brain neural substrate and Cognitive Core for AE01M.

## Architecture & Boundary Principles

Keep responsibilities strictly partitioned:

```text
Experience
→ Memory / Brain State
→ Cognitive Trigger
→ Cognitive Engine (LLM / Inference)
→ Thought / Prediction / Intention
→ Decision / Action
→ Experience
```

Strict architectural invariants:
- `Brain != Cognitive Engine`: The neural substrate (LIF neurons, regions, synapses) is distinct from inference engines.
- `Brain != LLM`: The LLM is an inference component producing reasoning text, not the neural substrate.
- `NeuralState != Thought`: NeuralState models continuous voltages, threshold crossings, and boolean spikes; thoughts are textual reasoning outputs.
- `CognitiveContext != Brain State`: CognitiveContext is an immutable frozen dataclass aggregating text snapshots (identity stage, memory strings, self-model metrics) rendered to prompts.
- `Inference Isolation`: The Cognitive Core only exposes rendered prompt text to cognitive engines, completely detached from live substrate objects.

## Data Flow Contract

1. **State Ingestion (Read-only)**:
   - `CognitiveLoop.build_context()` aggregates snapshots from `Identity`, `SelfModel`, and `Memory` into a frozen `CognitiveContext`.
   - `BrainMemoryBridge` provides isolated read-only copies (`neural_state_snapshot()`, `memory_activity_snapshot()`).
   - No mutable internal state crosses into the cognitive engine.

2. **Stimulation & Action Dispatch (Write-only / Event pulses)**:
   - Attention/salience checks trigger fixed-strength stimulus pulses (`current[0] = 1.0`) into region populations (`Hippocampus.step_chunk`, `MotorCortex.step_chunk`).
   - Decisions dispatch actions via `ActionModule`.
   - Accepted candidate experiences consolidate into `Memory` and record symbolic strings into `Brain.hippocampus`.

3. **Substrate Immutability**:
   - Cognitive processing never mutates `Synapse.weights`, connection mappings, or population membrane vectors.
   - Bridge snapshots remain detached copies; subsequent cognitive cycles do not mutate prior snapshots.

## Test Matrix

Verified in `tests/test_brain_cognitive_boundary.py`:
1. `test_cognitive_context_immutability_and_field_isolation`: validates frozen dataclass behavior and section rendering.
2. `test_cognitive_loop_reads_state_and_delivers_to_memory_and_brain`: verifies read of foundation state and delivery into episodic memory, hippocampus, and motor cortex.
3. `test_cognitive_processing_does_not_mutate_synapse_weights_or_neural_arrays`: verifies synapse weights and neural arrays are untouched by cognitive cycles.
4. `test_bridge_snapshot_remains_isolated_from_cognitive_loop`: verifies bridge snapshots remain unaffected by subsequent cognitive loops.
