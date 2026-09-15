#!/usr/bin/env python3
"""
Voice Playback Serializer for AE01M
Ensures only one voice output plays at a time, preventing overlap and duplication.
"""
import threading
import queue
import time
import os
import subprocess
from typing import Optional, Callable


class VoiceSerializer:
    """
    Serializes voice playback to prevent concurrent/overlapping TTS output.
    Implements a single-worker queue pattern with cancellation support.
    """
    
    def __init__(self):
        self._queue = queue.Queue()
        self._active_process = None
        self._active_file = None
        self._worker_thread = None
        self._shutdown = False
        self._lock = threading.Lock()
        self._start_worker()
    
    def _start_worker(self):
        """Start the background worker thread."""
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
    
    def _worker_loop(self):
        """Background worker that processes voice playback requests serially."""
        while not self._shutdown:
            try:
                # Get next playback request (blocking with timeout)
                try:
                    request = self._queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                if request is None:  # Shutdown signal
                    break
                
                # Unpack request
                audio_file, env, cleanup_callback = request
                
                # Play the audio (blocking)
                with self._lock:
                    try:
                        # Note: We try to play even if file doesn't exist 
                        # (for testing with mocks that may not check file existence)
                        # Execute playback (this blocks until audio finishes)
                        self._active_file = audio_file
                        cmd = ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", audio_file]
                        self._active_process = subprocess.Popen(
                            cmd,
                            env=env,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        
                        # Wait for playback to complete
                        self._active_process.wait()
                        
                        # Cleanup
                        if cleanup_callback:
                            cleanup_callback(audio_file)
                        
                    except Exception:
                        pass
                    finally:
                        self._active_process = None
                        self._active_file = None
                
                # Mark task complete
                self._queue.task_done()
                
            except Exception:
                continue
    
    def _cancel_current(self):
        """Cancel currently playing audio if any."""
        with self._lock:
            if self._active_process:
                try:
                    self._active_process.terminate()
                    self._active_process.wait(timeout=1.0)
                except Exception:
                    try:
                        self._active_process.kill()
                    except Exception:
                        pass
                self._active_process = None
    
    def play(self, audio_file: str, env: dict, cleanup_callback: Optional[Callable] = None):
        """
        Queue audio file for playback.
        Cancels any currently playing audio and plays this one instead.
        
        Args:
            audio_file: Path to audio file
            env: Environment variables for playback process
            cleanup_callback: Optional function to call after playback for cleanup
        """
        if self._shutdown:
            return
        
        # Cancel any currently playing audio immediately
        self._cancel_current()
        
        # Clear any pending items in queue (we only want the latest)
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
                self._queue.task_done()
            except queue.Empty:
                break
        
        # Add new request
        self._queue.put((audio_file, env, cleanup_callback))
    
    def shutdown(self):
        """Shutdown the voice serializer and stop any active playback."""
        self._shutdown = True
        self._cancel_current()
        
        # Signal worker to stop
        self._queue.put(None)
        
        # Wait for worker to finish
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=2.0)


# Global singleton instance
_voice_serializer = None
_serializer_lock = threading.Lock()


def get_voice_serializer() -> VoiceSerializer:
    """Get or create the global voice serializer instance."""
    global _voice_serializer
    with _serializer_lock:
        if _voice_serializer is None:
            _voice_serializer = VoiceSerializer()
        return _voice_serializer


if __name__ == "__main__":
    # Test voice serialization
    serializer = VoiceSerializer()
    
    print("Testing voice serialization...")
    print("This would normally queue audio files for sequential playback")
    
    time.sleep(1)
    serializer.shutdown()
    print("Shutdown complete")
