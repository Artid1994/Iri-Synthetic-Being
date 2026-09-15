#!/usr/bin/env python3
"""
Sherpa-ONNX Thai TTS Engine
100% offline VITS-based neural TTS using Facebook MMS Thai model.
"""
import os
import sys
import time
import subprocess
from pathlib import Path
from enum import Enum

# Thai text processing
try:
    from pythainlp.tokenize import word_tokenize
    PYTHAINLP_AVAILABLE = True
except ImportError:
    PYTHAINLP_AVAILABLE = False
    print("[WARN] pythainlp not available, word tokenization disabled", file=sys.stderr)

# Sherpa-ONNX
try:
    import sherpa_onnx
    SHERPA_AVAILABLE = True
except ImportError:
    SHERPA_AVAILABLE = False
    # Silent import failure - availability is checked via SHERPA_AVAILABLE flag


class EmotionalState(Enum):
    """Fallback emotional states if not imported from Limbic."""
    FORMAL = "formal"
    WARM = "warm"
    ATTENTIVE = "attentive"
    SUPPORTIVE = "supportive"
    NEUTRAL = "neutral"
    CALM = "calm"


class SherpaTTS:
    """
    Sherpa-ONNX Thai TTS engine with pythainlp preprocessing.
    100% offline, VITS-based neural synthesis.
    """
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.model_dir = self.project_root / "04_Cerebellum" / "models" / "sherpa-vits-tha" / "vits-mms-tha"
        self.audio_cache = self.project_root / "04_Cerebellum" / "audio_cache"
        
        # Create audio cache
        self.audio_cache.mkdir(parents=True, exist_ok=True)
        
        # Check availability
        if not SHERPA_AVAILABLE:
            raise ImportError("sherpa-onnx not installed")
        
        if not self.model_dir.exists():
            raise FileNotFoundError(f"Model directory not found: {self.model_dir}")
        
        # Check for audio players
        self.ffplay_available = self._check_command("ffplay")
        self.aplay_available = self._check_command("aplay")
        
        # Initialize Sherpa-ONNX TTS
        self._init_tts()
        
        print(f"[Sherpa-TTS] Initialized with model: {self.model_dir}")
    
    def _check_command(self, command: str) -> bool:
        """Check if a command is available."""
        try:
            subprocess.run(["which", command], capture_output=True, check=True, timeout=2)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _init_tts(self):
        """Initialize Sherpa-ONNX TTS engine."""
        # Check what files exist
        model_file = self.model_dir / "model.onnx"
        tokens_file = self.model_dir / "tokens.txt"
        lexicon_file = self.model_dir / "lexicon.txt"
        
        # MMS models don't typically have lexicon files
        if not lexicon_file.exists():
            lexicon_file = ""  # Empty string for character-based models
        
        config = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                    model=str(model_file),
                    lexicon=str(lexicon_file) if lexicon_file else "",
                    tokens=str(tokens_file),
                ),
                num_threads=2,
                debug=False,
                provider="cpu",
            ),
            max_num_sentences=1,
        )
        
        self.tts = sherpa_onnx.OfflineTts(config)
        self.sample_rate = self.tts.sample_rate
        
        print(f"[Sherpa-TTS] Sample rate: {self.sample_rate} Hz")
        print(f"[Sherpa-TTS] Model: {model_file.name}")
        print(f"[Sherpa-TTS] Lexicon: {'character-based' if not lexicon_file else 'phoneme-based'}")
    
    def _preprocess_thai_text(self, text: str) -> str:
        """
        Preprocess Thai text with pythainlp word tokenization.
        Provides explicit word boundaries for better pronunciation.
        """
        if not text or not text.strip():
            return text
        
        # Remove markdown formatting
        import re
        text = re.sub(r'[*#`_~]', '', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Apply Thai word tokenization
        if PYTHAINLP_AVAILABLE and any("\u0e00" <= char <= "\u0e7f" for char in text):
            words = word_tokenize(text, engine="newmm")
            text = " ".join(words)
        
        return text.strip()
    
    def synthesize(
        self,
        text: str,
        output_path: str = None,
        speed: float = 1.0
    ) -> str:
        """
        Synthesize Thai text to WAV file.
        
        Args:
            text: Thai text to synthesize
            output_path: Output WAV file path (auto-generated if None)
            speed: Speech speed multiplier (1.0 = normal, <1.0 = slower, >1.0 = faster)
        
        Returns:
            Path to generated WAV file
        """
        if not text or not text.strip():
            return None
        
        # Preprocess text
        processed_text = self._preprocess_thai_text(text)
        
        # Generate output path if not provided
        if output_path is None:
            import tempfile
            fd, output_path = tempfile.mkstemp(suffix=".wav", dir=self.audio_cache)
            os.close(fd)
        
        # Measure synthesis time
        start_time = time.time()
        
        # Generate audio
        audio = self.tts.generate(
            processed_text,
            sid=0,  # Speaker ID (MMS models typically have single speaker)
            speed=speed
        )
        
        # Write WAV file
        sherpa_onnx.write_wave(
            output_path,
            audio.samples,
            audio.sample_rate
        )
        
        synthesis_time = time.time() - start_time
        
        # Verify output
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            print(f"[ERROR] Failed to generate audio file", file=sys.stderr)
            return None
        
        file_size = os.path.getsize(output_path)
        print(f"[Sherpa-TTS] Synthesized in {synthesis_time:.2f}s ({file_size} bytes)")
        
        return output_path
    
    def speak(
        self,
        text: str,
        speed: float = 1.0,
        blocking: bool = True
    ) -> bool:
        """
        Synthesize and speak Thai text.
        
        Args:
            text: Text to speak
            speed: Speech speed (1.0 = normal)
            blocking: Wait for playback to complete
        
        Returns:
            True if successful, False otherwise
        """
        # Synthesize audio
        audio_path = self.synthesize(text, speed=speed)
        
        if not audio_path:
            return False
        
        try:
            # Play audio
            success = self._play_wav(audio_path, blocking)
            return success
        finally:
            # Cleanup
            try:
                if os.path.exists(audio_path):
                    os.unlink(audio_path)
            except:
                pass
    
    def _play_wav(self, wav_path: str, blocking: bool = True) -> bool:
        """Play WAV file using available player."""
        try:
            if self.ffplay_available:
                cmd = ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", wav_path]
            elif self.aplay_available:
                cmd = ["aplay", "-q", wav_path]
            else:
                print("[ERROR] No audio player found (ffplay/aplay)", file=sys.stderr)
                return False
            
            if blocking:
                result = subprocess.run(cmd, timeout=30, capture_output=True)
                return result.returncode == 0
            else:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
                
        except Exception as e:
            print(f"[ERROR] Playback failed: {e}", file=sys.stderr)
            return False


# Global instance
_tts_instance = None


def get_tts():
    """Get or create global Sherpa-TTS instance."""
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = SherpaTTS()
    return _tts_instance


def speak(text: str, speed: float = 1.0):
    """Convenience function to speak text."""
    tts = get_tts()
    return tts.speak(text, speed=speed, blocking=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_text = sys.argv[1]
        speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
        
        print(f"🗣️  Sherpa-ONNX Thai TTS Test")
        print(f"Text: {test_text}")
        print(f"Speed: {speed}x")
        print()
        
        success = speak(test_text, speed=speed)
        sys.exit(0 if success else 1)
    else:
        print("Usage: python sherpa_tts_engine.py <thai_text> [speed]")
        print("Example: python sherpa_tts_engine.py 'สวัสดีครับ' 1.0")
