from __future__ import annotations

from runtime.gemma_cognitive_engine import GemmaCognitiveEngine
from runtime.llama_cpp_inference import LlamaCppInference
from runtime.ollama_inference import OllamaInference


def create_cognitive_engine(
    model_path: str = "",
    executable: str = "",
    backend: str = "ollama",
    model: str = "qwen3.5:0.8b",
) -> GemmaCognitiveEngine:
    if backend == "ollama":
        inference = OllamaInference(model=model)
    elif backend == "llama":
        inference = LlamaCppInference(
            model_path=model_path,
            executable=executable,
        )
    else:
        raise ValueError(f"Unsupported cognitive backend: {backend}")

    return GemmaCognitiveEngine(inference=inference)
