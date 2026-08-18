from __future__ import annotations

from collections.abc import Callable
import subprocess


class LlamaCppInference:
    def __init__(
        self,
        model_path: str,
        executable: str,
        runner: Callable[[list[str]], str] | None = None,
    ) -> None:
        self.model_path = model_path
        self.executable = executable
        self._runner = runner or self._run_subprocess

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
            "8",
            "-no-cnv",
            "-st",
            "-p",
            prompt,
        ]
        return self._runner(command)

    @staticmethod
    def _run_subprocess(command: list[str]) -> str:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        )
        return result.stdout.strip()
