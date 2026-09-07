"""Voice Synthesis Module for AE01M (04_Cerebellum).

Integrates local Text-to-Speech synthesis and audio playback.
Supports high-quality multilingual Thai & English voices via edge-tts with
lightweight local offline fallbacks (espeak-ng) and local audio players (ffplay, paplay, aplay).
"""

from __future__ import annotations

import asyncio
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


class VoiceSynthesizer:
    """Voice synthesis controller for AE01M motor/cerebellar speech action."""

    # Default natural Thai female voice for Iri (ไอริ)
    DEFAULT_THAI_VOICE = "th-TH-PremwadeeNeural"
    DEFAULT_ENGLISH_VOICE = "en-US-JennyNeural"
    PERSONA_GREETING_PREFIX = "เจ้านายคะ"

    def __init__(
        self,
        voice_th: str = DEFAULT_THAI_VOICE,
        voice_en: str = DEFAULT_ENGLISH_VOICE,
        rate: str = "+0%",
        volume: str = "+0%",
        player_cmd: Optional[str] = None,
        enabled: bool = True,
    ) -> None:
        self.voice_th = voice_th
        self.voice_en = voice_en
        self.rate = rate
        self.volume = volume
        self.enabled = enabled
        self._player = player_cmd or self._detect_player()

    def _detect_player(self) -> Optional[str]:
        """Detect available system audio player."""
        for candidate in ["ffplay", "paplay", "pw-play", "aplay", "mpg123"]:
            if shutil.which(candidate):
                return candidate
        return None

    def _contains_thai(self, text: str) -> bool:
        """Check if string contains Thai unicode characters."""
        return any("\u0e00" <= char <= "\u0e7f" for char in text)

    def select_voice(self, text: str) -> str:
        """Select appropriate voice based on language detection."""
        if self._contains_thai(text):
            return self.voice_th
        return self.voice_en

    def synthesize(self, text: str, output_path: Optional[str] = None) -> Optional[str]:
        """Synthesize text to audio file (mp3 or wav)."""
        if not text or not text.strip():
            return None

        clean_text = text.strip()
        voice = self.select_voice(clean_text)

        if output_path is None:
            fd, output_path = tempfile.mkstemp(suffix=".mp3")
            os.close(fd)

        # Attempt 1: edge-tts CLI (built-in fast neural engine)
        edge_tts_bin = shutil.which("edge-tts") or "/usr/local/bin/edge-tts"
        if os.path.exists(edge_tts_bin):
            cmd = [
                edge_tts_bin,
                "-t",
                clean_text,
                "-v",
                voice,
                "--rate",
                self.rate,
                "--volume",
                self.volume,
                "--write-media",
                output_path,
            ]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return output_path
            except Exception:
                pass

        # Attempt 2: Python edge_tts library if available
        try:
            import edge_tts

            async def _async_gen():
                communicate = edge_tts.Communicate(clean_text, voice, rate=self.rate, volume=self.volume)
                await communicate.save(output_path)

            asyncio.run(_async_gen())

            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path
        except Exception:
            pass

        # Attempt 3: Local offline fallback via espeak-ng
        espeak_bin = shutil.which("espeak-ng") or shutil.which("espeak")
        if espeak_bin:
            wav_path = output_path.replace(".mp3", ".wav")
            lang = "th" if self._contains_thai(clean_text) else "en"
            cmd = [espeak_bin, f"-v{lang}", "-w", wav_path, clean_text]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if res.returncode == 0 and os.path.exists(wav_path) and os.path.getsize(wav_path) > 0:
                    return wav_path
            except Exception:
                pass

        return None

    def play(self, audio_path: str, block: bool = True) -> bool:
        """Play generated audio via detected system player."""
        if not audio_path or not os.path.exists(audio_path):
            return False

        player = self._player or self._detect_player()
        if not player:
            return False

        if player == "ffplay":
            cmd = [player, "-nodisp", "-autoexit", "-loglevel", "error", audio_path]
        elif player in ("paplay", "pw-play", "aplay"):
            cmd = [player, audio_path]
        else:
            cmd = [player, audio_path]

        try:
            if block:
                # Give generous timeout for longer sentences
                res = subprocess.run(cmd, capture_output=True, timeout=60)
                return res.returncode == 0
            else:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
        except Exception:
            return False

    def speak(self, text: str, block: bool = True) -> bool:
        """Synthesize and speak text aloud."""
        if not self.enabled or not text or not text.strip():
            return False

        audio_file = self.synthesize(text)
        if not audio_file:
            return False

        try:
            return self.play(audio_file, block=block)
        finally:
            # Cleanup temp file after playback
            if os.path.exists(audio_file) and "/tmp" in audio_file:
                try:
                    os.remove(audio_file)
                except OSError:
                    pass


# Global singleton instance for easy import across runtime
default_synthesizer = VoiceSynthesizer()


def speak_aloud(text: str, block: bool = True) -> bool:
    """Convenience helper to speak text using Cerebellum voice synthesis."""
    return default_synthesizer.speak(text, block=block)
