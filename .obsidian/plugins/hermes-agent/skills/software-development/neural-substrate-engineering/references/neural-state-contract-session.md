# Neural State Contract: Validated Session Detail

## Repository evidence

- `LIFNeuronVector.membrane` is the only mutable neuron state currently exposed.
- `NeuronPopulation` owns lazy `LIFNeuronVector` chunks and steps them with `step_chunk()`.
- `Synapse.propagate()` consumes source spikes and returns target current; it does not step the target.
- `Plasticity.adapt()` consumes explicit source and target spikes and updates only `Synapse.weights`.
- `Brain` owns hippocampus and motor cortex regions but no broad neural-state registry.

## Validated minimal design

`NeuralState` is a copied snapshot of one projection cycle, owned by `Brain` as `brain.neural_state`. It contains source/target chunk indices, source/target membrane vectors, source spikes, target current, and target spikes. It deliberately excludes Synapse, weights, memory, identity, cognition, learning, and history/persistence.

Create it after source stepping, propagation, target stepping, and plasticity. Keep the existing cycle return dictionary unchanged. Validate one-dimensional arrays, exact `float32` membrane/current dtypes, exact `bool` spike dtypes, and matching source/target shapes. Copy arrays in the snapshot constructor; frozen dataclass metadata alone does not make NumPy arrays immutable.

## Focused validation matrix

- cycle snapshot reflects actual source/target membrane and activity
- source/target chunk indices are explicit
- state has no weights or Synapse reference
- repeated fresh runs produce identical snapshots
- mutating snapshot arrays does not mutate population membrane
- projection and Plasticity remain functional
- memory behavior remains unchanged
- only requested chunks are allocated
- invalid state array shape/dtype fails deterministically

## Boundary warning

This is an inspectable one-cycle snapshot, not complete Brain state, persistence, activity history, or biological equivalence. Do not broaden it into a state registry without a separate architecture decision.
