from __future__ import annotations

from runtime.gemma_cognitive_engine import GemmaCognitiveEngine
from runtime.llama_cpp_inference import LlamaCppInference


def create_cognitive_engine(
    model_path: str,
    executable: str,
) -> GemmaCognitiveEngine:
    inference = LlamaCppInference(
        model_path=model_path,
        executable=executable,
    )
    return GemmaCognitiveEngine(inference=inference)
