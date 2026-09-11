# Thai NLP Resources for AE01M (Iri)

This directory contains Thai language processing resources for local intent recognition and entity extraction without LLM dependencies.

## Datasets

### 1. PyThaiNLP Lexicon-Thai
**Source:** https://github.com/PyThaiNLP/lexicon-thai
**License:** Creative Commons Attribution-ShareAlike 4.0 International
**Size:** ~45 MB
**Contents:**
- Thai person names (male/female): 1,388 names
- Thai abbreviations: 253 entries
- Sentiment lexicons (positive/negative)
- Swear words corpus
- Thai-English sentence pairs
- Thai Brown corpus

**Key Files:**
- `lexicon-thai/thai-name/female.txt` - 926 female names
- `lexicon-thai/thai-name/man.txt` - 462 male names
- `lexicon-thai/thai-abbreviation/data.csv` - Common abbreviations
- `lexicon-thai/sentiment/` - Sentiment analysis wordlists
- `lexicon-thai/corpus/` - Training corpora

### 2. Thai-NER (Named Entity Recognition)
**Source:** https://github.com/wannaphong/thai-ner
**License:** See License-dataset.md
**Size:** ~627 MB
**Contents:**
- NER training datasets with entity tags
- BiLSTM-CRF models
- Historical datasets for entity recognition

**Key Directories:**
- `thai-ner/model/` - Pre-trained NER models
- `thai-ner/bilstm-crf-model/` - BiLSTM-CRF architecture
- `thai-ner/old/` - Historical training data versions

## Integration

### Python Module: `nlp_thai_lexicon.py`
Located at: `03_Hippocampus/nlp_thai_lexicon.py`

**Features:**
- Load Thai name lexicons (male/female)
- Expand Thai abbreviations
- Extract entities from Thai text
- Intent classification without LLM
- Action verb detection

**Usage:**
```python
from nlp_thai_lexicon import get_thai_lexicon

lexicon = get_thai_lexicon()

# Extract intent from Thai command
intent = lexicon.extract_intent("เปิด ไฟ ห้องนอน")
print(intent)
# {
#   "action": "เปิด",
#   "target": "ไฟ",
#   "entities": {...},
#   "confidence": 1.0
# }

# Check if token is a person name
is_name = lexicon.is_person_name("วรรณพงษ์")  # True
```

### Integration with iri_chat.py
The Thai lexicon is integrated into `scripts/iri_chat.py`:
- Automatic intent classification for Thai commands
- Entity extraction for action targets
- No LLM required for basic Thai command parsing

**Supported Commands:**
- เปิด/ปิด (open/close)
- เริ่ม/หยุด (start/stop)
- แสดง/ค้นหา (show/search)
- บันทึก/ลบ (save/delete)
- และอื่นๆ (and more)

## Statistics

**Total Size:** 672 MB
- lexicon-thai: 45 MB
- thai-ner: 627 MB

**Lexicon Counts:**
- Female names: 926
- Male names: 462
- Abbreviations: 253
- Action verbs: ~30 (curated for command recognition)

## Maintenance

**Last Updated:** 2026-09-11
**Dataset Versions:**
- lexicon-thai: Latest from GitHub (2026-09-11)
- thai-ner: Latest from GitHub (2026-09-11)

**Update Command:**
```bash
cd 03_Hippocampus/knowledge_base/nlp_thai/
cd lexicon-thai && git pull
cd ../thai-ner && git pull
```

## Attribution

- **PyThaiNLP lexicon-thai** by Wannaphong Phatthiyaphaibun
- **Thai-NER dataset** by Wannaphong Phatthiyaphaibun
- Integrated into AE01M/Iri by Artid Aunporn (อาทิตย์ อ้วนพร)

## Notes

These datasets enable Iri to perform basic Thai language understanding locally without requiring external LLM calls for simple command parsing and entity recognition. This supports autonomous operation and reduces latency for common interactions.
