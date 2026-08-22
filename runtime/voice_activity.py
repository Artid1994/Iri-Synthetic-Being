from __future__ import annotations

import math


class VoiceActivityDetector:
    def __init__(
        self,
        sample_width: int = 2,
        threshold: float = 0.015,
        silence_duration: float = 0.8,
        frame_duration: float = 0.1,
    ) -> None:
        if sample_width <= 0:
            raise ValueError("sample_width must be greater than zero")

        if threshold < 0:
            raise ValueError("threshold must not be negative")

        if silence_duration <= 0:
            raise ValueError("silence_duration must be greater than zero")

        if frame_duration <= 0:
            raise ValueError("frame_duration must be greater than zero")

        self.sample_width = sample_width
        self.threshold = threshold
        self.silence_duration = silence_duration
        self.frame_duration = frame_duration

        self._speaking = False
        self._silent_duration = 0.0

    def energy(self, data: bytes) -> float:
        if not data:
            return 0.0

        if self.sample_width != 2:
            raise ValueError("only 16-bit PCM is supported")

        sample_count = len(data) // 2

        if sample_count == 0:
            return 0.0

        total = 0.0

        for index in range(sample_count):
            offset = index * 2
            sample = int.from_bytes(
                data[offset:offset + 2],
                byteorder="little",
                signed=True,
            )
            normalized = sample / 32768.0
            total += normalized * normalized

        return math.sqrt(total / sample_count)

    def process(self, data: bytes) -> str:
        current_energy = self.energy(data)

        if current_energy >= self.threshold:
            self._speaking = True
            self._silent_duration = 0.0
            return "speech"

        if not self._speaking:
            return "silence"

        self._silent_duration += self.frame_duration

        if self._silent_duration >= self.silence_duration:
            self._speaking = False
            self._silent_duration = 0.0
            return "speech_end"

        return "silence"

    @property
    def speaking(self) -> bool:
        return self._speaking
