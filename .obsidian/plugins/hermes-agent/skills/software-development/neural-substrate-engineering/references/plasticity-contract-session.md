# Plasticity Contract Session Reference

Validated pattern for a minimal deterministic plasticity layer over the existing population-chunk Synapse API.

## Compatibility facts

- `LIFNeuronVector.step(input_current)` owns membrane update and spike generation.
- `NeuronPopulation.step_chunk(chunk_index, input_current)` owns chunk stepping and lazy allocation.
- `Synapse` stores source/target populations and chunk indices, mapped source/target indices, and `float32` weights.
- `Synapse.propagate(source_spikes)` returns a fresh target current; it does not step the target population.

## Minimal rule

`Plasticity.adapt(synapse, source_spikes, target_spikes) -> updated_weights`

For each Synapse mapping:

```text
if source_spikes[source_index] and target_spikes[target_index]:
    weight += learning_rate
weight = clamp(weight, min_weight, max_weight)
```

The rule updates only `synapse.weights`; it must not change endpoints, mappings, membrane state, or spike inputs.

## Required validation

- `synapse` must be a Synapse.
- `learning_rate`, `min_weight`, and `max_weight` must be finite.
- `learning_rate >= 0`.
- `min_weight <= max_weight`.
- Source and target spike vectors must match their Synapse chunk shapes.
- Output and stored weights remain one-dimensional `float32` with unchanged mapping length.

## Focused test matrix

Cover:

1. co-active mapped pair increments by learning rate;
2. source-only and target-only activity do not update;
3. only co-active mappings update;
4. maximum and minimum bounds are enforced;
5. repeated updates are deterministic and saturate;
6. source/target shape errors are rejected;
7. invalid rule configuration is rejected;
8. spike inputs are not mutated;
9. Synapse endpoints and mappings are preserved;
10. dtype and shape remain `float32` and unchanged;
11. updated weights affect later propagation;
12. spikes produced by LIF populations can drive adaptation;
13. no MemoryGraph dependency is introduced.

Use `assert_allclose` rather than exact decimal equality for nontrivial `float32` increments such as `0.8 + 0.1`.

## Verification discipline

For implementation tasks:

1. add focused tests first and verify RED;
2. implement only `brain/plasticity.py` and its focused test file;
3. run focused tests;
4. run full regression when requested;
5. run `git diff --check`;
6. verify the changed-file list against the exact scope;
7. report exact totals and preserve unrelated untracked work.

A passing full suite proves regression compatibility, not biological equivalence or completion of Brain orchestration.