#!/usr/bin/env python3
"""
MMS-TTS Engine: Facebook's Massively Multilingual Speech (MMS) Thai TTS
Replaces Piper-TTS with a high-quality local VITS model.
"""
import os
import torch
import scipy.io.wavfile
from pathlib import Path
from transformers import VitsModel, VitsTokenizer


class MMSTTSEngine:
    """
    Facebook MMS-TTS Thai speech synthesis engine.
    100% offline, VITS-based neural TTS with 36.3M parameters.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize MMS-TTS engine.
        
        Args:
            model_path: Path to local MMS-TTS model directory
        """
        if model_path is None:
            project_root = Path(__file__).parent.parent
            model_path = project_root / "04_Cerebellum" / "models" / "mms-tts-tha"
        
        self.model_path = Path(model_path)
        
        if not self.model_path.exists():
            raise FileNotFoundError(f"MMS-TTS model not found at: {self.model_path}")
        
        print(f"[MMS-TTS] Loading model from: {self.model_path}")
        
        # Load model and tokenizer
        self.tokenizer = VitsTokenizer.from_pretrained(str(self.model_path))
        self.model = VitsModel.from_pretrained(str(self.model_path))
        
        # Set to eval mode for inference
        self.model.eval()
        
        # Use CPU for inference (resource-constrained target)
        self.device = "cpu"
        self.model.to(self.device)
        
        print(f"[MMS-TTS] Model loaded successfully (36.3M params)")
    
    def synthesize(
        self, 
        text: str, 
        output_path: str,
        speaking_rate: float = 1.0,
        noise_scale: float = 0.667
    ) -> bool:
        """
        Synthesize Thai text to WAV file.
        
        Args:
            text: Thai text to synthesize
            output_path: Output WAV file path
            speaking_rate: Speech speed (1.0 = normal, <1.0 = slower, >1.0 = faster)
            noise_scale: Variability in speech (0.667 default, lower = more monotone)
        
        Returns:
            True if synthesis succeeded, False otherwise
        """
        if not text or not text.strip():
            return False
        
        try:
            # Tokenize input text
            inputs = self.tokenizer(text, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate speech
            with torch.no_grad():
                outputs = self.model(
                    **inputs,
                    speaking_rate=speaking_rate,
                    noise_scale=noise_scale
                )
            
            # Get waveform
            waveform = outputs.waveform[0].cpu().numpy()
            
            # MMS-TTS outputs at 16kHz
            sample_rate = 16000
            
            # Save to WAV file
            scipy.io.wavfile.write(output_path, sample_rate, waveform)
            
            # Verify file was written
            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                return False
            
            return True
            
        except Exception as e:
            print(f"[MMS-TTS ERROR] Synthesis failed: {e}")
            return False
    
    def __del__(self):
        """Cleanup on deletion."""
        # Clear CUDA cache if used (though we use CPU)
        if hasattr(self, 'model'):
            del self.model
        if hasattr(self, 'tokenizer'):
            del self.tokenizer


# Global engine instance
_mms_engine = None


def get_engine():
    """Get or create global MMS-TTS engine instance."""
    global _mms_engine
    if _mms_engine is None:
        _mms_engine = MMSTTSEngine()
    return _mms_engine


if __name__ == "__main__":
    import sys
    
    # Test synthesis
    if len(sys.argv) > 1:
        test_text = sys.argv[1]
        output_file = "test_mms_output.wav"
        
        print(f"🗣️  Synthesizing: {test_text}")
        
        engine = get_engine()
        success = engine.synthesize(test_text, output_file)
        
        if success:
            print(f"✓ WAV file saved: {output_file}")
            print(f"  Play with: ffplay -nodisp -autoexit {output_file}")
        else:
            print("✗ Synthesis failed")
            sys.exit(1)
    else:
        print("Usage: python mms_tts_engine.py <thai_text>")
