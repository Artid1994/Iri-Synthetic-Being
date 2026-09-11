# TTS Engine Status - AE01M (Iri)

## Current Status (2026-09-09)

### Outcome
**Kept Piper-TTS as primary engine** due to MMS-TTS CPU performance constraints.

### Summary

Attempted to replace Piper-TTS with Facebook MMS-TTS for higher quality Thai speech, but discovered critical performance limitation:

- **MMS-TTS inference time**: >30 seconds per sentence on CPU
- **Target hardware**: Resource-constrained (per AGENTS.md)
- **Decision**: Retain optimized Piper-TTS pipeline

### What Was Accomplished

1. **Downloaded Facebook MMS-TTS Thai Model**
   - Location: `04_Cerebellum/models/mms-tts-tha/`
   - Model: `facebook/mms-tts-tha` (36.3M parameters, VITS-based)
   - Status: Available for future high-quality offline generation (non-real-time use cases)

2. **Created MMS-TTS Engine Wrapper**
   - File: `04_Cerebellum/mms_tts_engine.py`
   - Features: ONNX-compatible, 100% offline, PyTorch inference
   - Use case: High-quality batch generation (not real-time speech)

3. **Installed Dependencies**
   - `pythainlp`: Thai word tokenization (already integrated with Piper)
   - `transformers`: Hugging Face model loading
   - `torch` (CPU): PyTorch inference engine
   - `scipy`, `soundfile`: Audio processing

4. **Architecture Documentation**
   - `04_Cerebellum/SPEECH_ARCHITECTURE.md`: Piper pipeline with pythainlp preprocessing
   - Current working pipeline: Thai text → pythainlp → Piper → WAV file → ffplay/aplay

### Current Working Pipeline

```
Thai Text Input
    ↓
pythainlp.word_tokenize() [Proper word boundaries]
    ↓
Piper TTS [Fast neural synthesis, ~1-2s]
    ↓
Clean WAV file generation
    ↓
ffplay/aplay playback
    ↓
Auto-cleanup
```

### Performance Comparison

| Engine | Inference Time | Quality | Offline | Real-time |
|--------|---------------|---------|---------|-----------|
| **Piper-TTS** | ~1-2s | Good (neural) | ✓ | ✓ |
| MMS-TTS | >30s | Excellent (VITS) | ✓ | ✗ |
| espeak-ng | <1s | Basic (formant) | ✓ | ✓ |

### Recommendation

**Current configuration is optimal for AE01M's resource-constrained target hardware:**

1. **Real-time speech (daemon)**: Use Piper-TTS (current default)
   - Fast inference (~1-2s)
   - Neural quality with pythainlp preprocessing
   - Proper Thai word boundaries and natural pauses

2. **High-quality offline generation**: Use MMS-TTS (available but not integrated)
   - Manual invocation via `mms_tts_engine.py`
   - For pre-recorded messages, audiobooks, or non-interactive content
   - Not suitable for conversational AI due to latency

3. **Fallback**: espeak-ng (already integrated)
   - Ultra-fast, always available
   - Basic quality but reliable

### Testing

```bash
# Current working Piper-TTS (fast, real-time)
./.venv/bin/python 04_Cerebellum/voice_synthesis.py "สวัสดีค่ะ" NEUTRAL

# MMS-TTS (high quality, slow, offline batch)
./.venv/bin/python 04_Cerebellum/mms_tts_engine.py "สวัสดีค่ะ"

# Through Iri daemon (uses Piper by default)
iri "สวัสดีไอริ"
```

### Future Considerations

If hardware constraints change or GPU acceleration becomes available:
1. MMS-TTS can be integrated as a high-quality mode
2. Model quantization (INT8/FP16) could improve MMS inference speed
3. Hybrid mode: Piper for real-time, MMS for important/formal responses

### Files Modified/Created

- ✓ `04_Cerebellum/voice_synthesis.py` — Optimized Piper pipeline with pythainlp
- ✓ `04_Cerebellum/mms_tts_engine.py` — MMS-TTS wrapper (available for batch use)
- ✓ `04_Cerebellum/models/mms-tts-tha/` — Downloaded MMS model (36.3M params)
- ✓ `04_Cerebellum/SPEECH_ARCHITECTURE.md` — Current pipeline documentation
- ✓ Installed: `pythainlp`, `transformers`, `torch`, `scipy`, `soundfile`

### Conclusion

**Piper-TTS remains the primary engine** for AE01M's real-time speech synthesis due to its excellent balance of quality and performance on resource-constrained hardware. MMS-TTS is available as an optional high-quality engine for non-real-time use cases.


---

## Neural Connections

[[04_Cerebellum]] · [[Language]] · [[AI_Systems]]
