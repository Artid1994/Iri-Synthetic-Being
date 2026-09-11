# Brain ↔ Memory Boundary Contract

Validated architecture and boundary verification rules connecting the neural substrate to the memory subsystem.

## Core Rules

1. **Independent Ownership**:
   - `Brain` exclusively owns neural populations, LIF neuron vectors, synaptic projection cycles, and the latest `NeuralState` snapshot.
   - `Memory` exclusively owns `MemoryState` (working, episodic, semantic) and `MemoryGraph`.
   - `MemoryGraph` exclusively owns memory nodes, co-activation edges, and edge weights.
   - Synapse weights remain owned by `Synapse` and updated only by `Plasticity`.

2. **No Semantic Neural Encoding Claim**:
   - Memory items stored via artificial current injection (e.g. `current[0] = 1.0` in hippocampus) do not constitute semantic neural encoding.
   - Never map `MemoryEdge` weights to `Synapse` weights or memory strength to synaptic plasticity.
   - Never claim memory content is represented meaningfully by the neural substrate without a verified encoding/decoding mechanism.

3. **Narrow Read-Only Inspection Bridge**:
   - `BrainMemoryBridge(brain: Brain, memory: Memory)`
   - Crosses boundaries strictly via detached copies/snapshots.
   - No live NumPy arrays or mutable internal references cross the boundary.
   - `bridge.neural_state_snapshot()` returns copied arrays.
   - `bridge.memory_activity_snapshot()` returns copied node/edge lists without consuming pending activity.
   - Reading snapshots never mutates underlying neural membrane states or memory graph edges.

4. **Phase 5 Audit & Verification Protocol**:
   - When verifying Phase 5 completion criteria, verify each criterion explicitly against both real code call paths and deterministic unit tests:
     1. Memory enters brain pipeline via explicit sync methods (`Brain.store_memory()`, `Brain.sync_memory()`, `runtime.sync_brain_memory()`).
     2. Brain state does not become memory storage (neural dynamics vs. symbolic index storage).
     3. MemoryGraph and neural connections remain separate (Synapse propagation vs. graph edge traversal).
     4. Synchronization is deterministic and idempotent.
   - Exclude known long-running autonomous stress tests (`test_stress_long_runtime`, `test_full_autonomous_validation`, `test_autonomous_long_trial`, `test_learning_loop`) during full regression runs to avoid execution timeouts while auditing core subsystems.
