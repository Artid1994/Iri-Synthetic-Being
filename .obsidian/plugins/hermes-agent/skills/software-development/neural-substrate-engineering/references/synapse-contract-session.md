# Synapse Contract Reference

Validated compatibility facts for a vectorized LIF substrate:

- `LIFNeuronVector.step(input_current)` requires an array matching its membrane shape and returns a spike array.
- `NeuronPopulation.step_chunk(chunk_index, input_current)` lazily allocates a chunk and delegates to LIF state.
- `NeuronPopulation._chunk_length(chunk_index)` gives the valid size for a logical chunk, including a final partial chunk.
- Regions such as hippocampus and motor cortex expose their population through `.population`.
- Existing tests cover LIF threshold/reset, lazy population allocation, region allocation, and Brain-level cognitive signaling; they do not establish synaptic connectivity.

Minimal deterministic propagation matrix:

1. weighted source spikes map to target indices
2. no spikes produce zero current
3. multiple source contributions sum at one target
4. output shape and dtype match the target chunk
5. source spike input remains unchanged
6. source shape mismatch is rejected
7. mapping lengths must match
8. source/target indices must be in range
9. produced current can drive the target LIF population
10. hippocampus-to-motor-cortex chunk endpoints are compatible
11. identical endpoints are rejected for the minimal contract
12. synapse has no MemoryGraph integration

Required verification sequence:

- focused test file: pass
- full regression: wait for process exit and final result
- `git diff --check`: clean
- changed files: inside `brain/` and `tests/` only
