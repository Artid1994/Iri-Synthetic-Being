from __future__ import annotations

from runtime.audio_input import AudioChunk
from runtime.speech_recognition import SpeechRecognition


class VoiceConversation:
    def __init__(
        self,
        cognitive,
        speech_output,
        speech_recognition: SpeechRecognition | None = None,
        max_text_length: int = 120,
    ) -> None:
        if max_text_length <= 0:
            raise ValueError("max_text_length must be greater than zero")

        self.cognitive = cognitive
        self.speech_output = speech_output
        self.speech_recognition = (
            speech_recognition or SpeechRecognition()
        )
        self.max_text_length = max_text_length

    def respond(self, audio: AudioChunk) -> str:
        text = self.speech_recognition.transcribe(audio)

        if not text:
            return ""

        text = text.strip()

        if not text:
            return ""

        if len(text) > self.max_text_length:
            return ""

        response = self.cognitive.process(text)

        if not isinstance(response, str):
            raise TypeError(
                "cognitive response must be a string"
            )

        response = response.strip()

        if response:
            self.speech_output.speak(response)

        return response
