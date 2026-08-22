from __future__ import annotations

from dataclasses import dataclass
import subprocess


@dataclass(frozen=True)
class AudioChunk:
    data: bytes
    sample_rate: int
    channels: int
    sample_width: int


class AudioInput:
    def __init__(
        self,
        device: str = "default",
        sample_rate: int = 16000,
        channels: int = 1,
        sample_width: int = 2,
    ) -> None:
        self.device = device
        self.sample_rate = sample_rate
        self.channels = channels
        self.sample_width = sample_width

    def record(self, duration: float) -> AudioChunk:
        if duration <= 0:
            raise ValueError("duration must be greater than zero")

        command = [
            "arecord",
            "-D",
            self.device,
            "-f",
            "S16_LE",
            "-r",
            str(self.sample_rate),
            "-c",
            str(self.channels),
            "-d",
            str(duration),
            "-t",
            "raw",
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if result.returncode != 0:
            error = result.stderr.decode(
                "utf-8",
                errors="replace",
            ).strip()

            raise RuntimeError(
                error or "audio recording failed"
            )

        return AudioChunk(
            data=result.stdout,
            sample_rate=self.sample_rate,
            channels=self.channels,
            sample_width=self.sample_width,
        )
