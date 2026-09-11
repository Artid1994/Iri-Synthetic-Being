# Thai Speech Pipeline Architecture

## Re-architecture Summary (2026-09-09)

### Problem
Distorted "alien/robot" pitch in Piper-TTS speech output caused by:
- Raw PCM stdout piping with potential format mismatches
- No Thai text preprocessing (run-on phoneme distortion)
- Real-time streaming without quality verification

### Solution

#### 1. Thai Text Preprocessing
- **pythainlp integration**: Word tokenization using `word_tokenize(text, engine="newmm")`
- **Proper spacing**: Insert spaces between Thai words to create natural pauses
- **Phoneme clarity**: Prevents run-on phoneme distortion in TTS synthesis

#### 2. File-Based Synthesis Pipeline
- **Generate to disk**: Piper outputs clean WAV files to `audio_cache/`
- **Quality verification**: Check file existence and size before playback
- **Clean playback**: Use `ffplay -nodisp -autoexit` (preferred) or `aplay` from file
- **Auto-cleanup**: Remove temporary WAV files after playback

#### 3. Audio Player Priority
1. **ffplay**: Preferred (clean, no-display, auto-exit)
2. **aplay**: Fallback (direct file playback)

### Architecture

```
Thai Text Input
    ↓
pythainlp.word_tokenize() [Word boundaries + spacing]
    ↓
Piper TTS [Generate WAV to disk]
    ↓
Verify WAV file [Size + existence checks]
    ↓
ffplay/aplay [File-based playback]
    ↓
Cleanup [Remove temporary WAV]
```

### Key Components

**HybridTTS class enhancements:**
- `audio_cache/`: Temporary WAV file storage
- `_preprocess_thai_text()`: Thai word tokenization
- `speak_piper()`: File-based synthesis with preprocessing
- `_play_wav_file()`: Clean file-based playback
- `_check_command()`: Audio player availability detection

### Dependencies
- **pythainlp**: Thai NLP toolkit for word tokenization
- **ffplay** (ffmpeg): Preferred audio player
- **aplay** (alsa-utils): Fallback audio player

### Configuration
- **Sample rate**: 22050 Hz (from th_TH-tsync2-medium.onnx.json)
- **Format**: WAV with proper headers
- **Speech speed**: 0.95-1.05 length_scale (natural human range)
- **Cache location**: `04_Cerebellum/audio_cache/`

### Testing
```bash
# Direct test
./.venv/bin/python 04_Cerebellum/voice_synthesis.py "สวัสดีค่ะ" NEUTRAL

# Through Iri daemon
iri "สวัสดีไอริ ทดสอบการประมวลผลคำอ่านภาษาไทย"
```

### Results
- ✓ Natural Thai speech without distortion
- ✓ Proper word boundaries and pauses
- ✓ Clean audio playback
- ✓ Emotional state modulation preserved
- ✓ Automatic cleanup of temporary files


---

## Neural Connections

[[04_Cerebellum]] · [[Language]] · [[AI_Systems]]
