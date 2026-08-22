from __future__ import annotations

import subprocess

from runtime.audio_input import AudioChunk
from runtime.voice_activity import VoiceActivityDetector


class VoiceCapture:
    def __init__(
        self,
        device: str = "default",
        sample_rate: int = 16000,
        channels: int = 1,
        sample_width: int = 2,
        frame_duration: float = 0.1,
        silence_duration: float = 0.8,
        threshold: float = 0.015,
    ) -> None:
        self.device = device
        self.sample_rate = sample_rate
        self.channels = channels
        self.sample_width = sample_width
        self.frame_duration = frame_duration

        self.detector = VoiceActivityDetector(
            sample_width=sample_width,
            threshold=threshold,
            silence_duration=silence_duration,
            frame_duration=frame_duration,
        )

    def listen(self) -> AudioChunk:
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
            "-t",
            "raw",
            "-q",
        ]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=0,
        )

        frame_size = int(
            self.sample_rate
            * self.channels
            * self.sample_width
            * self.frame_duration
        )

        frames: list[bytes] = []
        speaking = False

        try:
            while True:
                data = process.stdout.read(frame_size)

                if not data:
                    break

                if len(data) < frame_size:
                    continue

                state = self.detector.process(data)

                if state == "speech":
                    if not speaking:
                        print(
                            "เริ่มรับเสียง...",
                            flush=True,
                        )
                        speaking = True

                    frames.append(data)

                elif speaking:
                    frames.append(data)

                    if state == "speech_end":
                        print(
                            "หยุดพูด → จบการรับเสียง",
                            flush=True,
                        )

                        return AudioChunk(
                            data=b"".join(frames),
                            sample_rate=self.sample_rate,
                            channels=self.channels,
                            sample_width=self.sample_width,
                        )

        except KeyboardInterrupt:
            raise

        finally:
            process.terminate()

            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

        return AudioChunk(
            data=b"".join(frames),
            sample_rate=self.sample_rate,
            channels=self.channels,
            sample_width=self.sample_width,
        )
