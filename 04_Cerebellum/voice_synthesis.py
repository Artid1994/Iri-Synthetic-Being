"""Voice Synthesis Module for AE01M (04_Cerebellum).

Integrates local Text-to-Speech synthesis and audio playback.
Hybrid architecture: Edge-TTS (primary, online) with Sherpa-ONNX fallback (offline).
"""

from __future__ import annotations

import asyncio
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

# Thai text processing
try:
    from pythainlp.tokenize import word_tokenize
    PYTHAINLP_AVAILABLE = True
except ImportError:
    PYTHAINLP_AVAILABLE = False

# Sherpa-ONNX fallback engine
SHERPA_AVAILABLE = False
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from sherpa_tts_engine import SherpaTTS
    SHERPA_AVAILABLE = True
except ImportError:
    pass


class VoiceSynthesizer:
    """Voice synthesis controller for AE01M motor/cerebellar speech action."""

    # Default natural Thai male voice for Iri (ไอริ)
    DEFAULT_THAI_VOICE = "th-TH-NiwatNeural"
    DEFAULT_ENGLISH_VOICE = "en-US-JennyNeural"
    PERSONA_GREETING_PREFIX = "เจ้านายคะ"

    def __init__(
        self,
        voice_th: str = DEFAULT_THAI_VOICE,
        voice_en: str = DEFAULT_ENGLISH_VOICE,
        rate: str = "+5%",  # Natural Thai conversational pace
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
        
        # Initialize Sherpa-ONNX fallback engine (lazy loaded)
        self._sherpa_engine = None
        self._sherpa_initialized = False
        
        print(f"[Voice] Primary: Edge-TTS ({voice_th})")
        print(f"[Voice] Fallback: Sherpa-ONNX (available: {SHERPA_AVAILABLE})")

    def _detect_player(self) -> Optional[str]:
        """Detect available system audio player."""
        for candidate in ["ffplay", "paplay", "pw-play", "aplay", "mpg123"]:
            if shutil.which(candidate):
                return candidate
        return None

    def _contains_thai(self, text: str) -> bool:
        """Check if string contains Thai unicode characters."""
        return any("\u0e00" <= char <= "\u0e7f" for char in text)
    
    def _preprocess_thai_text(self, text: str) -> str:
        """
        Preprocess Thai text for clearer Edge-TTS pronunciation.
        
        - Tokenizes Thai words with pythainlp for explicit word boundaries
        - Removes markdown formatting characters
        - Normalizes punctuation for natural pauses
        - Adds micro-pauses at sentence boundaries
        """
        if not text or not text.strip():
            return text
        
        # Clean markdown and formatting characters
        text = re.sub(r'[*#`_~]', '', text)
        
        # Normalize multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Add natural pauses at Thai sentence boundaries
        # Insert slight pause markers for major punctuation
        text = text.replace('។', '។ ')  # Thai full stop
        text = text.replace('?', '? ')  # Question mark
        text = text.replace('!', '! ')  # Exclamation
        text = text.replace(',', ', ')  # Comma (shorter pause)
        text = text.replace('  ', ' ')  # Clean up double spaces
        
        # Apply Thai word tokenization for clear boundaries
        if self._contains_thai(text) and PYTHAINLP_AVAILABLE:
            words = word_tokenize(text, engine="newmm")
            text = " ".join(words)
        
        return text.strip()

    def select_voice(self, text: str) -> str:
        """Select appropriate voice based on language detection."""
        if self._contains_thai(text):
            return self.voice_th
        return self.voice_en

    def synthesize(self, text: str, output_path: Optional[str] = None, rate: Optional[str] = None, volume: Optional[str] = None) -> Optional[str]:
        """
        Synthesize text to audio file with auto-fallback.
        
        Primary: Edge-TTS (online, fast)
        Fallback: Sherpa-ONNX (offline, slower)
        """
        if not text or not text.strip():
            return None

        # Preprocess Thai text for clarity
        clean_text = self._preprocess_thai_text(text.strip())
        
        # Try Edge-TTS first (online)
        try:
            audio_file = self._synthesize_edge_tts(clean_text, output_path, rate, volume)
            if audio_file:
                print("[Voice] Using Edge-TTS (Online)")
                return audio_file
        except Exception as e:
            print(f"[Voice] Edge-TTS failed: {e}")
        
        # Fallback to Sherpa-ONNX (offline)
        if SHERPA_AVAILABLE:
            try:
                audio_file = self._synthesize_sherpa(clean_text, output_path)
                if audio_file:
                    print("[Voice] Falling back to Sherpa-ONNX (Offline)")
                    return audio_file
            except Exception as e:
                print(f"[Voice] Sherpa-ONNX failed: {e}")
        
        # Final fallback to espeak-ng
        return self._synthesize_espeak(clean_text, output_path)
    
    def _synthesize_edge_tts(self, clean_text: str, output_path: Optional[str], rate: Optional[str], volume: Optional[str]) -> Optional[str]:
        """Synthesize with Edge-TTS (primary, online)."""
        voice = self.select_voice(clean_text)
        
        # Use instance defaults or override
        synthesis_rate = rate if rate is not None else self.rate
        synthesis_volume = volume if volume is not None else self.volume

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
                synthesis_rate,
                "--volume",
                synthesis_volume,
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
                communicate = edge_tts.Communicate(clean_text, voice, rate=synthesis_rate, volume=synthesis_volume)
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
        """Synthesize and speak text aloud with voice-matched honorifics."""
        if not self.enabled or not text or not text.strip():
            return False
        
        # Format text to match voice gender
        try:
            from voice_formatter import format_output
            text = format_output(text, include_master=None)  # Auto-detect context
        except ImportError:
            pass  # Skip formatting if module not available

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


def speak(text: str, emotional_state=None) -> bool:
    """
    Module-level speak function for daemon compatibility.
    Wrapper around speak_aloud for voice_interactive_loop.py
    """
    return speak_aloud(text, block=True)
