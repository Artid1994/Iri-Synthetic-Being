from __future__ import annotations

from collections.abc import Callable


class LlamaCppInference:
    def __init__(
        self,
        model_path: str,
        executable: str,
        runner: Callable[[list[str]], str],
    ) -> None:
        self.model_path = model_path
        self.executable = executable
        self._runner = runner

    def __call__(self, prompt: str) -> str:
        command = [
            self.executable,
            "-m",
            self.model_path,
            "-t",
            "1",
            "-c",
            "256",
            "-n",
            "32",
            "-no-cnv",
            "-p",
            prompt,
        ]
        return self._runner(command)
