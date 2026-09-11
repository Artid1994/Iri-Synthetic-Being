"""
Chat Voice Bridge - TTS integration for chat interface
Connects voice synthesis to interactive chat for natural spoken conversation.
"""

import sys
import threading
from pathlib import Path
from typing import Optional

# Add Cerebellum to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))

try:
    from voice_synthesis import speak_aloud
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


class ChatVoiceBridge:
    """Bridge between chat interface and TTS voice synthesis."""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled and VOICE_AVAILABLE
        self.voice_threads = []
        self.max_concurrent_voices = 2  # Limit concurrent playback
    
    def speak(self, text: str, block: bool = False):
        """
        Speak text using TTS (non-blocking by default).
        Plays audio in background thread.
        """
        if not self.enabled:
            return
        
        # Clean up finished threads
        self.voice_threads = [t for t in self.voice_threads if t.is_alive()]
        
        # Limit concurrent voices
        if len(self.voice_threads) >= self.max_concurrent_voices:
            # Wait for oldest thread to finish
            if self.voice_threads:
                self.voice_threads[0].join(timeout=1.0)
        
        if block:
            # Blocking mode
            try:
                speak_aloud(text, block=True)
            except Exception:
                pass
        else:
            # Non-blocking mode (default)
            def speak_thread():
                try:
                    speak_aloud(text, block=False)
                except Exception:
                    pass
            
            thread = threading.Thread(target=speak_thread, daemon=True)
            thread.start()
            self.voice_threads.append(thread)
    
    def speak_bilingual(self, text: str, language_hint: str = None):
        """
        Speak with language detection for Thai/English mixing.
        Language hint: 'th', 'en', or None (auto-detect).
        """
        if not self.enabled:
            return
        
        # Auto-detect if primarily Thai
        if language_hint is None:
            thai_chars = sum(1 for c in text if '\u0e00' <= c <= '\u0e7f')
            total_chars = len(text.replace(' ', ''))
            language_hint = 'th' if total_chars > 0 and (thai_chars / total_chars) > 0.3 else 'en'
        
        # Speak with detected language
        self.speak(text, block=False)
    
    def is_available(self) -> bool:
        """Check if voice synthesis is available."""
        return self.enabled
    
    def wait_for_completion(self, timeout: float = 5.0):
        """Wait for all active voice threads to complete."""
        for thread in self.voice_threads:
            if thread.is_alive():
                thread.join(timeout=timeout)
        
        self.voice_threads = []
