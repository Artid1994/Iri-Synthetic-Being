from __future__ import annotations

import subprocess


class SpeechOutput:
    def __init__(
        self,
        voice: str = "th",
        speed: int = 150,
    ) -> None:
        self.voice = voice
        self.speed = speed

    def speak(self, text: str) -> bool:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        text = text.strip()

        if not text:
            return False

        result = subprocess.run(
            [
                "espeak-ng",
                "-v",
                self.voice,
                "-s",
                str(self.speed),
                text,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
        )

        return result.returncode == 0
