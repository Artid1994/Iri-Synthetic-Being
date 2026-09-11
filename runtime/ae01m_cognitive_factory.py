from __future__ import annotations

from runtime.ae01m_cognitive_core import AE01MCognitiveCore
from runtime.brain_inference import BrainInference
from runtime.neocortex_cognition import NeocortexCognition


def create_cognitive_engine(
    model_path: str = "",
    executable: str = "",
    backend: str = "neocortex",
    host: str = "http://localhost:11434",
) -> AE01MCognitiveCore:
    if backend == "neocortex":
        inference = NeocortexCognition(host=host)
    elif backend == "brain":
        inference = BrainInference(
            model_path=model_path,
            executable=executable,
        )
    else:
        raise ValueError(f"Unsupported cognitive backend: {backend}")

    return AE01MCognitiveCore(inference=inference)
