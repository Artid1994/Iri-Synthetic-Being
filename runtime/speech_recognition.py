from __future__ import annotations

from io import BytesIO
import wave

from runtime.audio_input import AudioChunk


class SpeechRecognition:
    def __init__(
        self,
        model_size: str = "tiny",
        device: str = "cpu",
        compute_type: str = "int8",
    ) -> None:
        from faster_whisper import WhisperModel

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, audio: AudioChunk) -> str:
        if not isinstance(audio, AudioChunk):
            raise TypeError("audio must be an AudioChunk")

        if not audio.data:
            return ""

        buffer = BytesIO()

        with wave.open(buffer, "wb") as wav:
            wav.setnchannels(audio.channels)
            wav.setsampwidth(audio.sample_width)
            wav.setframerate(audio.sample_rate)
            wav.writeframes(audio.data)

        buffer.seek(0)

        segments, _ = self.model.transcribe(
            buffer,
            language="th",
            beam_size=1,
        )

        return " ".join(
            segment.text.strip()
            for segment in segments
            if segment.text.strip()
        ).strip()
