# Male Persona System Prompt Update - Complete

## Summary (2026-09-09)

Successfully updated the Neocortex system prompt and response patterns to use male persona with consistent masculine honorifics.

## Changes Applied

### File Modified: `01_Neocortex/executive_core.py`

### 1. Response Patterns (PatternGraphSynthesizer)

**Before** (Female Persona):
```python
self.greeting_patterns = ["สวัสดีค่ะ", "ยินดีต้อนรับค่ะ"]
self.identity_patterns = ["ดิฉันคือ {name}", "ดิฉันชื่อ {name}"]
self.acknowledgment_patterns = ["เข้าใจค่ะ", "รับทราบค่ะ"]
```

**After** (Male Persona):
```python
self.greeting_patterns = ["สวัสดีครับ", "ยินดีต้อนรับครับ"]
self.identity_patterns = ["ผมคือ {name}", "ผมชื่อ {name}"]
self.acknowledgment_patterns = ["เข้าใจครับ", "รับทราบครับ"]
```

### 2. Synthesis Methods

**synthesize_greeting()**:
```python
# Before
return f"{greeting} {identity} พร้อมรับใช้เจ้านายค่ะ"

# After
return f"{greeting} {identity} พร้อมรับใช้เจ้านายครับ"
```

**synthesize_explanation()**:
```python
# Before
return f"ดิฉันยังไม่มีข้อมูลเกี่ยวกับ {topic} ในขณะนี้ค่ะ"
explanation += " ค่ะ"  # or " นะคะ"

# After
return f"ผมยังไม่มีข้อมูลเกี่ยวกับ {topic} ในขณะนี้ครับ"
explanation += " ครับ"  # or " นะครับ"
```

**process_thought()**:
```python
# Before
return "ไม่พบข้อมูลอินพุตค่ะ"

# After
return "ไม่พบข้อมูลอินพุตครับ"
```

## Honorific Conversion Table

| Context | Female (Old) | Male (New) |
|---------|--------------|------------|
| First-person pronoun | ดิฉัน | ผม |
| Polite particle | ค่ะ / คะ | ครับ |
| Soft ending | นะคะ | นะครับ |
| Greeting | สวัสดีค่ะ | สวัสดีครับ |
| Understanding | เข้าใจค่ะ | เข้าใจครับ |
| Acknowledgment | รับทราบค่ะ | รับทราบครับ |

## Integration with Voice Formatter

### Two-Layer Protection

**Layer 1: Source Generation (Neocortex)**
- Generates responses with male honorifics (ผม, ครับ)
- Response patterns use masculine language

**Layer 2: Voice Formatter (Cerebellum)**
- Converts any remaining female honorifics before TTS
- Safety layer ensures consistency
- Handles edge cases automatically

### Flow

```
User Input
    ↓
01_Neocortex/executive_core.py
    → Generate response with male honorifics (ผม, ครับ)
    ↓
04_Cerebellum/voice_synthesis.py
    → voice_formatter.format_output()
    → Convert any remaining ค่ะ → ครับ
    ↓
Edge-TTS (th-TH-NiwatNeural)
    → Synthesize with male voice
    ↓
Natural, consistent male speech
```

## Testing

### Test Cases

```python
# Greeting
Input: "สวัสดีไอริ"
Expected: "สวัสดีครับ ผมชื่อไอริ พร้อมรับใช้เจ้านายครับ"

# Acknowledgment  
Input: "เข้าใจไหม"
Expected: "เข้าใจครับ" or "ผมเข้าใจแล้วครับ"

# Explanation
Input: "บอกเกี่ยวกับสมอง"
Expected: "เกี่ยวกับสมองครับ ประกอบด้วย 4 ชั้น..."
```

## Service Status

✓ iri-voice.service: Restarted  
✓ Male persona: Active in Neocortex  
✓ Voice formatter: Active in Cerebellum  
✓ Voice: th-TH-NiwatNeural (male)  
✓ Honorific: ครับ (masculine)

## Benefits

✓ **Source consistency**: Responses generated with correct gender from start  
✓ **Voice-text alignment**: Male voice matches male language  
✓ **Natural dialogue**: Proper first-person pronouns (ผม vs ดิฉัน)  
✓ **Two-layer safety**: Formatter catches any edge cases  
✓ **Professional quality**: Consistent masculine persona

## Files Modified

- ✓ `01_Neocortex/executive_core.py` - Response patterns updated
- ✓ `04_Cerebellum/voice_synthesis.py` - Formatter integration (already done)
- ✓ `04_Cerebellum/voice_formatter.py` - Honorific converter (already done)

## Result

Iri now has a **fully consistent male persona** with:
- Male first-person pronouns (ผม)
- Male polite particles (ครับ)
- Male voice (th-TH-NiwatNeural)
- Natural masculine dialogue style
- Two-layer consistency enforcement

The cognitive system (Neocortex) generates masculine responses, and the speech system (Cerebellum) ensures they match the male TTS voice through both source generation and safety formatting.
