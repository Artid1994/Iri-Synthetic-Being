# Sherpa-ONNX Thai TTS Integration - Complete

## Summary (2026-09-09)

Successfully integrated **Sherpa-ONNX** with Facebook MMS Thai VITS model as a 100% offline TTS alternative to Edge-TTS.

## Installation

### Dependencies Installed
```bash
pip install sherpa-onnx pythainlp
```

- **sherpa-onnx**: 1.13.7
- **sherpa-onnx-core**: 1.13.7
- **pythainlp**: Already installed

### Model Downloaded

**Model**: `vits-mms-tha` (Facebook MMS Thai VITS)
**Source**: https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-mms-tha.tar.bz2
**Size**: 103MB compressed, 109MB uncompressed
**Location**: `04_Cerebellum/models/sherpa-vits-tha/vits-mms-tha/`

**Files**:
- `model.onnx`: 109MB VITS neural TTS model
- `tokens.txt`: 473 bytes Thai character tokens
- `config.json`: 1.9KB model configuration

**Model Type**: Character-based (no lexicon file needed)

## Implementation

### File Created

**`04_Cerebellum/sherpa_tts_engine.py`** (8.3KB)

**Features**:
- **100% offline**: No internet required
- **pythainlp preprocessing**: Word tokenization for clarity
- **VITS neural synthesis**: High-quality speech
- **Configurable speed**: Adjustable speech rate
- **Auto-cleanup**: Temporary files removed after playback

### Architecture

```
Thai Text Input
    ↓
pythainlp word tokenization
    ↓
Markdown cleanup
    ↓
Sherpa-ONNX VITS synthesis
    ↓
WAV file (16kHz)
    ↓
ffplay/aplay playback
    ↓
Auto-cleanup
```

### Key Methods

```python
class SherpaTTS:
    def __init__()           # Initialize model (one-time load)
    def synthesize()         # Generate WAV file
    def speak()              # Synthesize + play
    def _preprocess_thai_text()  # pythainlp tokenization
    def _play_wav()          # Audio playback
```

## Performance Metrics

### Synthesis Latency

**Test 1**: "สวัสดีครับ ทดสอบระบบเสียง Sherpa ONNX"
- **Time**: 9.12 seconds
- **Output**: 98,394 bytes (16kHz WAV)

**Test 2**: "สวัสดีครับเจ้านาย ทดสอบระบบเสียงออฟไลน์"
- **Time**: 11.08 seconds
- **Output**: 128,800 bytes (16kHz WAV)

### Comparison with Other Engines

| Engine | Latency | Quality | Offline | RAM |
|--------|---------|---------|---------|-----|
| **Sherpa-ONNX** | ~10-11s | Good (VITS) | ✓ | ~109MB |
| Edge-TTS | ~1-2s | Excellent (Neural) | ✗ | Minimal |
| MMS-TTS | >30s | Excellent (VITS) | ✓ | ~150MB |
| Piper-TTS | N/A | N/A | ✓ | Thai incompatible |
| espeak-ng | <1s | Basic | ✓ | Minimal |

### Configuration

- **Sample rate**: 16,000 Hz (16kHz)
- **Model type**: Character-based VITS
- **Threads**: 2 CPU threads
- **Provider**: CPU (ONNX Runtime)
- **Max sentences**: 1 at a time

## Testing

### Direct Test
```bash
cd ~/Projects/THE_TRANSCENDING_FORM
./.venv/bin/python 04_Cerebellum/sherpa_tts_engine.py "สวัสดีครับ" 1.0
```

### Test Results
```
🗣️  Sherpa-ONNX Thai TTS Test
Text: สวัสดีครับเจ้านาย ทดสอบระบบเสียงออฟไลน์
Speed: 1.0x

[Sherpa-TTS] Sample rate: 16000 Hz
[Sherpa-TTS] Model: model.onnx
[Sherpa-TTS] Lexicon: character-based
[Sherpa-TTS] Initialized with model: .../vits-mms-tha
[Sherpa-TTS] Synthesized in 11.08s (128800 bytes)
```

### Integration Test (via iri command)
```bash
iri "สวัสดีครับเจ้านาย ทดสอบระบบเสียง Sherpa ONNX VITS บนเครื่อง Local"
```

## Advantages

✓ **100% offline**: No internet connection required  
✓ **Privacy**: All processing local, no data sent to cloud  
✓ **VITS neural quality**: Better than espeak, comparable to cloud TTS  
✓ **pythainlp integration**: Clear Thai word boundaries  
✓ **Portable**: Single ONNX model file, runs anywhere  
✓ **No phoneme errors**: Unlike Piper, handles Thai correctly

## Disadvantages

✗ **Slower than Edge-TTS**: 10-11s vs 1-2s (5-10x slower)  
✗ **Higher latency**: Not suitable for real-time conversational AI  
✗ **Larger model**: 109MB vs Edge-TTS (no model download)  
✗ **CPU-only**: No GPU acceleration tested yet

## Use Cases

### Best For:
- Offline demos and testing
- Privacy-critical applications
- Environments without internet
- Batch audio generation
- Development/prototyping

### Not Ideal For:
- Real-time conversational AI (too slow)
- Low-latency voice assistants
- Resource-constrained devices (109MB model)

## Recommendation

**For Production (Iri)**:
- **Primary**: Edge-TTS (th-TH-NiwatNeural) - Fast, high quality
- **Fallback**: Sherpa-ONNX - Offline alternative when internet unavailable
- **Emergency**: espeak-ng - Always works but robotic

**Current Status**:
- ✓ Sherpa-ONNX: Installed and working
- ✓ Edge-TTS: Active in production (iri-voice.service)
- ⚠️ Sherpa-ONNX: Available but not integrated into daemon (latency too high)

## Future Optimization

To improve Sherpa-ONNX performance:
1. **GPU acceleration**: Test with CUDA/TensorRT provider
2. **Model quantization**: INT8 quantization for smaller/faster model
3. **Batch processing**: Pre-generate common phrases
4. **Streaming**: Investigate streaming VITS synthesis

## Files

- ✓ `04_Cerebellum/sherpa_tts_engine.py` - Engine implementation
- ✓ `04_Cerebellum/models/sherpa-vits-tha/` - Model directory (109MB)
- ✓ `sherpa-onnx` package installed in .venv
- ✓ Documentation: This file

## Result

Sherpa-ONNX Thai TTS is **successfully integrated** as a 100% offline alternative with:
- VITS neural quality
- pythainlp preprocessing
- 10-11 second synthesis latency
- 109MB model footprint

Suitable for offline testing and development, but Edge-TTS remains preferred for production due to superior latency (1-2s vs 10-11s).


---

## Neural Connections

[[04_Cerebellum]] · [[Language]] · [[AI_Systems]]
