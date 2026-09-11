from __future__ import annotations

from runtime.gemma_cognitive_engine import GemmaCognitiveEngine
from runtime.brain_inference import BrainInference
from runtime.neocortex_cognition import NeocortexCognition


def create_cognitive_engine(
    model_path: str = "",
    executable: str = "",
    backend: str = "neocortex",
    model: str = "qwen3.5:0.8b",
    host: str = "http://10.74.65.85:11434",
) -> GemmaCognitiveEngine:
    if backend == "neocortex":
        inference = NeocortexCognition(model=model, host=host)
    elif backend == "brain":
        inference = BrainInference(
            model_path=model_path,
            executable=executable,
        )
    else:
        raise ValueError(f"Unsupported cognitive backend: {backend}")

    return GemmaCognitiveEngine(inference=inference)
