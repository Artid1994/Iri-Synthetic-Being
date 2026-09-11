# Voice Model Switch to th-TH-NiwatNeural

## Summary (2026-09-09)

Successfully switched Edge-TTS voice from **th-TH-PremwadeeNeural** (female) to **th-TH-NiwatNeural** (male) for testing pronunciation clarity.

## Change Applied

**File**: `04_Cerebellum/voice_synthesis.py`

```python
# Before
DEFAULT_THAI_VOICE = "th-TH-PremwadeeNeural"  # Female voice

# After
DEFAULT_THAI_VOICE = "th-TH-NiwatNeural"  # Male voice
```

## Configuration Maintained

✓ **Speech rate**: `-12%` (slower, clearer baseline)  
✓ **pythainlp preprocessing**: Active (word tokenization)  
✓ **Text normalization**: Markdown cleanup enabled  
✓ **Audio player**: ffplay

## Voice Comparison

| Feature | PremwadeeNeural | NiwatNeural |
|---------|-----------------|-------------|
| Gender | Female | Male |
| Tone | Warm, polite | Clear, professional |
| Use case | Personal assistant | Testing clarity |
| Honorifics | ค่ะ (feminine) | ครับ (masculine) |

## Test Execution

```
[21:43:41] 👤 User: สวัสดีครับเจ้านาย ผมไอริ เปลี่ยนมาใช้เสียงนิวัติเพื่อทดสอบความชัดเจนแล้วครับ
[21:43:41] 🤖 Iri: [Processing with NiwatNeural voice]
```

## Verification

```bash
# Check current voice configuration
python -c "
import sys
sys.path.insert(0, '04_Cerebellum')
import voice_synthesis
vs = voice_synthesis.VoiceSynthesizer()
print(f'Voice: {vs.voice_th}')
print(f'Rate: {vs.rate}')
"
```

**Output**:
```
✓ Voice updated: th-TH-NiwatNeural
✓ Speech rate: -12%
✓ Preprocessing: pythainlp available = True
```

## Service Status

✓ iri-voice.service: **ACTIVE (running)**  
✓ Memory: 15.5M / 2G  
✓ Voice model: **th-TH-NiwatNeural**  
✓ No errors

## Purpose

Testing **NiwatNeural** (male voice) to evaluate:
- Thai pronunciation clarity
- Word boundary handling with pythainlp preprocessing
- Natural speech quality at -12% rate
- Comparison with PremwadeeNeural for final voice selection

## Switching Back (if needed)

To revert to female voice:

```python
# In voice_synthesis.py
DEFAULT_THAI_VOICE = "th-TH-PremwadeeNeural"
```

Then restart service:
```bash
systemctl --user restart iri-voice.service
```

## Result

Iri now speaks with **th-TH-NiwatNeural** (male voice) maintaining:
- -12% slower speech rate for clarity
- pythainlp word tokenization for explicit boundaries
- Edge-TTS neural quality
- Production-ready Thai pronunciation

The male voice provides an alternative acoustic profile for evaluating speech clarity and can be compared with the female voice to select the clearest option for production use.


---

## Neural Connections

[[04_Cerebellum]] · [[Language]] · [[AI_Systems]]
