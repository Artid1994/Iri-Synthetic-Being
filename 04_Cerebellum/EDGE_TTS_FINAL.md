# Edge-TTS Voice Synthesis - Final Solution

## Summary (2026-09-09)

Successfully restored **Microsoft Edge-TTS** as the primary voice synthesis engine for Iri with Limbic emotional state integration.

## Why Edge-TTS?

After extensive testing of alternatives:

1. **Piper-TTS**: Thai phoneme compatibility errors ("aɪ is not a single codepoint")
2. **MMS-TTS**: >30 seconds inference time (too slow for real-time)
3. **ThonburianTTS**: Installation interrupted, heavy dependencies
4. **espeak-ng + ffmpeg**: Fast but robotic quality even with post-processing
5. **Edge-TTS**: ✓ Natural neural quality, ✓ Fast, ✓ Limbic integration

## Implementation

**Voice**: `th-TH-PremwadeeNeural` (Microsoft Azure Thai female neural voice)

**Emotional State Modulation**:
- Directly mapped to Edge-TTS parameters (`rate`, `pitch`, `volume`)
- Real-time dynamic tone adjustment based on Limbic emotional state

| Emotional State | Rate | Pitch | Volume | Description |
|-----------------|------|-------|--------|-------------|
| FORMAL | -5% | +0Hz | +0% | สุภาพ เป็นทางการ |
| WARM | +0% | +5Hz | +5% | อบอุ่น เป็นกันเอง |
| ATTENTIVE | -3% | +0Hz | +0% | ตั้งใจฟัง ชัดเจน |
| SUPPORTIVE | +0% | +3Hz | +5% | ให้กำลังใจ |
| NEUTRAL | +0% | +0Hz | +0% | เป็นกลาง ปกติ |
| CALM | -8% | -3Hz | -5% | สงบ เยือกเย็น |

## Architecture

```
Text Input
    ↓
Limbic Emotional State
    ↓
Edge-TTS Synthesis
    (rate, pitch, volume modulation)
    ↓
MP3 Audio
    ↓
mpv / ffplay playback
    ↓
Auto-cleanup
```

## Trade-offs

**Advantages**:
- ✓ Natural human-like neural voice quality
- ✓ Fast synthesis (~1-2 seconds)
- ✓ Full Thai language support
- ✓ Dynamic emotional modulation
- ✓ No phoneme compatibility issues

**Disadvantages**:
- ✗ Requires internet connection (Azure TTS API)
- ✗ Privacy: Text sent to Microsoft servers
- ✗ Dependency on cloud service availability

## Testing

```bash
# Direct test
./.venv/bin/python 04_Cerebellum/voice_synthesis.py "สวัสดีค่ะ" NEUTRAL

# Emotional states
./.venv/bin/python 04_Cerebellum/voice_synthesis.py "ดิฉันชื่อไอริค่ะ" WARM
./.venv/bin/python 04_Cerebellum/voice_synthesis.py "เข้าใจแล้วค่ะ" FORMAL

# Through Iri daemon
iri "สวัสดีไอริ ทดสอบน้ำเสียง AI ธรรมชาติจริง"
```

## Files

- ✓ `04_Cerebellum/voice_synthesis.py` — Edge-TTS with Limbic integration
- ✓ `04_Cerebellum/voice_synthesis_espeak.py.backup` — espeak+ffmpeg version (offline)
- ✓ `04_Cerebellum/mms_tts_engine.py` — MMS-TTS (high quality, slow)
- ✓ Installed: `edge-tts`, `aiohttp`

## Future Offline Migration Path

When offline neural TTS becomes viable:

1. **GPU acceleration** available → Enable MMS-TTS for high-quality mode
2. **ThonburianTTS** matures → Test as Edge-TTS replacement
3. **Piper phoneme fix** → Re-evaluate Piper with Thai G2P improvements

For now, **Edge-TTS provides the best balance** of quality, speed, and ease of integration for AE01M's conversational AI requirements.

## Result

Iri now speaks with **natural, human-like Thai neural voice** with dynamic emotional expression controlled by the Limbic system. Voice quality is production-ready for conversational AI interactions.


---

## Neural Connections

[[04_Cerebellum]] · [[Language]] · [[AI_Systems]]
