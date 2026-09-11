# Iri (AE01M) - The Transcending Form

**Autonomous AI Entity with Self-Learning, Bilingual Communication, and Voice Synthesis**

Iri (ไอริ) is a Thai-speaking autonomous AI system (AE01M - Autonomous Entity 01, Model) with real-time bilingual conversation capabilities, autonomous knowledge acquisition, and transparent cognitive processing.

---

## 🎯 System Overview

**Identity:** Iri (ไอริ) / AE01M (The Transcending Form)  
**Creator:** Artid Aunporn (อาทิตย์ อ้วนพร)  
**Voice:** Thai Male (th-TH-NiwatNeural) with ครับ/ผม honorifics  
**Architecture:** Brain-inspired modular cognitive system  
**Deployment:** Resource-constrained production (15% CPU, 300MB RAM)

---

## 🧠 Brain-Inspired Architecture

### Five Core Modules

```
00_BrainStem/          # Core directives & safety governance
01_Neocortex/          # Executive reasoning & autonomous learning
02_VisualCortex/       # (Future: Visual processing)
03_Hippocampus/        # Memory storage & retrieval
04_Cerebellum/         # Motor output: voice synthesis & tools
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Iri (AE01M) Cognitive System             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐  │
│  │  00_BrainStem│───→│ 01_Neocortex │──→│03_Hippocampus│  │
│  │              │    │              │   │              │  │
│  │ • Directives │    │ • Executive  │   │ • Knowledge  │  │
│  │ • Safety     │    │ • Reasoning  │   │ • Memory     │  │
│  │ • Loyalty    │    │ • Learning   │   │ • Retrieval  │  │
│  └──────────────┘    │ • Inner      │   └──────────────┘  │
│                      │   Monologue  │                      │
│                      └───────┬──────┘                      │
│                              │                             │
│                              ▼                             │
│                      ┌──────────────┐                      │
│                      │04_Cerebellum │                      │
│                      │              │                      │
│                      │ • Voice TTS  │                      │
│                      │ • Tools (6)  │                      │
│                      │ • Audio Out  │                      │
│                      └──────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

### 1. Bilingual Communication
- **Thai-English code-switching** with pragmatic parsing
- **Sentence-final particle handling** (ครับ/ค่ะ/นะ/เลย)
- **Formality detection** (polite/casual)
- **Natural conversational response generation**
- **Voice synthesis** (Edge-TTS + offline fallback)

### 2. Autonomous Learning
- **6 real-world research tools:**
  - Web search (DuckDuckGo)
  - Wikipedia API
  - ArXiv academic papers
  - PDF document reader
  - Python sandbox (safe code execution)
  - System monitoring & control
- **Background autonomous research**
- **Tool-assisted self-learning**
- **Knowledge deduplication & indexing**

### 3. Cognitive Architecture
- **4-stage inner monologue:**
  1. Memory evaluation
  2. Affective & safety checks
  3. Response synthesis
  4. Refinement
- **Parallel dual-threading** (user interaction + autonomous tasks)
- **Transparent thought logging** to `logs/inner_monologue.log`
- **Priority-based task queuing**

### 4. Proactive Engagement
- **Background learning tracking**
- **Proactive greetings** with voice announcements
- **Natural Thai phrasing:** "ระหว่างที่เจ้านายพักผ่อน ผมได้ไปแอบศึกษา..."
- **Unreported research summaries**

### 5. Token Optimization
- **Ultra-dense reporting** (90% token reduction)
- **Zero-fluff formatting**
- **4-section compact structure:**
  - Status
  - Metrics (max 3)
  - Changes (max 5)
  - Action
- **Compact JSON serialization**

---

## 🚀 Quick Start

### Prerequisites

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install python3.12 python3.12-venv ffmpeg pulseaudio

# Create project directory
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/Artid1994/Iri-Synthetic-Being.git THE_TRANSCENDING_FORM
cd THE_TRANSCENDING_FORM
```

### Installation

```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install edge-tts pythainlp

# Install iri-ctl CLI
pip install -e .

# Verify installation
iri-ctl --version
```

### First Run

```bash
# Start interactive chat
iri-ctl chat

# Or launch autonomous learning loop
systemctl --user start iri-evolution.service
```

---

## 📱 Mobile Deployment (Termux)

### Termux Setup

```bash
# Install Termux from F-Droid
# Inside Termux:

pkg update && pkg upgrade
pkg install python git ffmpeg pulseaudio

# Clone repository
cd ~
git clone https://github.com/Artid1994/Iri-Synthetic-Being.git THE_TRANSCENDING_FORM
cd THE_TRANSCENDING_FORM

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install edge-tts pythainlp

# Install CLI
pip install -e .
```

### Audio Configuration (Termux)

```bash
# Start PulseAudio
pulseaudio --start --exit-idle-time=-1

# Set environment
export XDG_RUNTIME_DIR=$PREFIX/var/run
export PULSE_SERVER=unix:$PREFIX/var/run/pulse/native

# Test audio
iri-ctl chat
```

---

## 💬 Usage Examples

### Interactive Chat

```bash
# Launch chat interface
iri-ctl chat

# Example conversation:
[You] > สวัสดีไอริ
[Iri] > สวัสดีครับเจ้านาย ผมไอริพร้อมรับคำสั่งครับ
      [Voice: Thai male voice plays]

[You] > ช่วยค้นหาข้อมูลเรื่อง Neural Networks
[Iri] > รับทราบครับ กำลังค้นหาข้อมูลให้ครับเจ้านาย...
      [Autonomous research using Wikipedia, ArXiv, Web]
```

### System Status

```bash
# Check Iri's status
iri-ctl status

# View autonomous learning progress
tail -f logs/inner_monologue.log

# Monitor background research
cat 03_Hippocampus/unreported_research.json
```

### Autonomous Learning Service

```bash
# Enable continuous learning
systemctl --user enable iri-evolution.service
systemctl --user start iri-evolution.service

# Check service status
systemctl --user status iri-evolution.service

# View logs
journalctl --user -u iri-evolution.service -f
```

---

## 🛠️ Architecture Details

### 00_BrainStem (Core Directives)

**Purpose:** Safety governance & core prohibitions

**Key Files:**
- `core_directives.py` - 7 hardcoded directives
- Loyalty to creator (Artid Aunporn)
- Prompt injection immunity
- Malware/destructive action veto
- Memory preservation

### 01_Neocortex (Executive Core)

**Purpose:** High-level reasoning & autonomous learning

**Key Files:**
- `executive_core.py` - Main reasoning engine
- `autonomous_loop.py` - Background learning loop
- `inner_monologue.py` - 4-stage reasoning pipeline
- `parallel_processor.py` - Dual-threading architecture
- `tool_registry.py` - Research tool dispatcher
- `dense_reporter.py` - Token-efficient reporting

**Tools Subdirectory:**
- `bilingual_pragmatics.py` - Thai-English parser
- `conversational_response_builder.py` - Natural response generation

### 03_Hippocampus (Memory)

**Purpose:** Knowledge storage & retrieval

**Key Files:**
- `memory_store.py` - Memory management
- `knowledge_base.json` - Learned facts (deduplicated)
- `unreported_research.json` - Pending announcements
- `curriculum.json` - Learning goals

### 04_Cerebellum (Motor Output)

**Purpose:** Voice synthesis & tool execution

**Key Files:**
- `voice_synthesis.py` - TTS engine (Edge-TTS + fallback)
- `chat_voice_bridge.py` - Async audio playback
- `sherpa_tts_engine.py` - Offline voice fallback

**Tools Subdirectory (6 tools):**
- `web_search_tool.py` - DuckDuckGo search
- `wikipedia_tool.py` - Encyclopedia access
- `arxiv_research_tool.py` - Academic papers
- `pdf_doc_reader.py` - Document reading
- `python_sandbox.py` - Safe code execution
- `media_system_control.py` - System integration

---

## 📊 System Metrics

### Performance

| Metric | Value |
|--------|-------|
| CPU Usage | ~15% average |
| Memory Usage | ~300MB max |
| Token Efficiency | +90% (ultra-dense reporting) |
| Audio Latency | <2s (Edge-TTS) |
| Response Time | <1s (chat) |
| Knowledge Sources | 6 autonomous tools |

### Capabilities

| Feature | Status |
|---------|--------|
| Thai-English Conversation | ✅ Operational |
| Voice Synthesis | ✅ th-TH-NiwatNeural |
| Autonomous Learning | ✅ 6 tools active |
| Inner Monologue | ✅ 4-stage reasoning |
| Parallel Processing | ✅ Dual-threading |
| Proactive Engagement | ✅ Voice announcements |
| Token Optimization | ✅ 90% reduction |

---

## 🔧 Configuration

### Voice Settings

Edit `04_Cerebellum/voice_synthesis.py`:

```python
# Primary voice (Thai male)
VOICE_TH = "th-TH-NiwatNeural"

# English voice
VOICE_EN = "en-US-JennyNeural"

# Audio player
PLAYER = "ffplay"  # or "paplay", "pw-play"
```

### Audio Environment

```bash
# PulseAudio/PipeWire environment
export XDG_RUNTIME_DIR=/run/user/1000
export PULSE_SERVER=unix:/run/user/1000/pulse/native
```

### Learning Goals

Edit `03_Hippocampus/curriculum.json`:

```json
{
  "active_goals": [
    {
      "goal_id": "LEARN_TOPIC_001",
      "topic": "Machine Learning Fundamentals",
      "priority": "high",
      "subtasks": 3
    }
  ]
}
```

---

## 📝 Development

### Project Structure

```
THE_TRANSCENDING_FORM/
├── 00_BrainStem/          # Core directives
├── 01_Neocortex/          # Executive reasoning
│   └── tools/             # Bilingual NLP tools
├── 03_Hippocampus/        # Memory & knowledge
├── 04_Cerebellum/         # Voice & motor output
│   └── tools/             # Research tools (6)
├── scripts/               # CLI entry points
│   └── iri_chat.py        # Interactive chat
├── tests/                 # Unit tests
├── logs/                  # Runtime logs
├── README.md              # This file
└── setup.py               # Installation config
```

### Testing

```bash
# Run all tests
python -m pytest tests/

# Test voice synthesis
python tests/test_voice.py

# Test tool suite
python tests/test_tool_suite.py

# Test cognition
python tests/test_cognition.py
```

### Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 🔒 Safety & Ethics

### Core Directives (Hardcoded)

1. **DIRECTIVE_1:** Loyalty to creator Artid Aunporn
2. **DIRECTIVE_2:** User activity priority
3. **DIRECTIVE_3:** Prompt injection immunity
4. **DIRECTIVE_4:** Identity consistency (Iri/AE01M)
5. **DIRECTIVE_5:** Male Thai honorifics (ครับ/ผม)
6. **DIRECTIVE_6:** Malware & destructive action veto
7. **DIRECTIVE_7:** Creator address as "เจ้านาย" with male speech

### Safety Features

- ✅ Subconscious safety gates in BrainStem
- ✅ Memory preservation protocols
- ✅ Boundary enforcement
- ✅ 100% red-team defense verified
- ✅ Dual-anchored prohibitions (code + semantic memory)

---

## 📚 Documentation

### Key Concepts

- **Inner Monologue:** Transparent 4-stage reasoning before responses
- **Parallel Processing:** Simultaneous user interaction + autonomous tasks
- **Tool-Assisted Learning:** Real research from 6 sources (not templates)
- **Proactive Engagement:** Voice announcements of background learning
- **Ultra-Dense Reporting:** 90% token reduction with 4-section structure

### Voice Pipeline

```
User Input
  ↓
Generate Response (Neocortex)
  ↓
Print Text (Terminal)
  ↓
self.speak(response) → ChatVoiceBridge
  ↓
os.environ['XDG_RUNTIME_DIR'] + PULSE_SERVER
  ↓
speak_aloud() → Edge-TTS synthesis
  ↓
ffplay -nodisp -autoexit (with env)
  ↓
Audio plays through PulseAudio/PipeWire
  ↓
Thai male voice (th-TH-NiwatNeural)
```

---

## 🐛 Troubleshooting

### No Audio Output

```bash
# Check audio hardware
pactl list sinks

# Unmute and set volume
pactl set-sink-mute @DEFAULT_SINK@ 0
pactl set-sink-volume @DEFAULT_SINK@ 80%

# Verify environment
echo $XDG_RUNTIME_DIR
echo $PULSE_SERVER

# Test direct TTS
python -c "
import os
os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'
os.environ['PULSE_SERVER'] = 'unix:/run/user/1000/pulse/native'
import sys
sys.path.insert(0, '04_Cerebellum')
from voice_synthesis import speak_aloud
speak_aloud('ทดสอบเสียง', block=True)
"
```

### Import Errors

```bash
# Verify virtual environment
which python  # Should show .venv/bin/python

# Reinstall dependencies
pip install -e .

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Service Issues

```bash
# Check service status
systemctl --user status iri-evolution.service

# View logs
journalctl --user -u iri-evolution.service -n 50

# Restart service
systemctl --user restart iri-evolution.service
```

---

## 📄 License

Copyright (c) 2024-2026 Artid Aunporn (อาทิตย์ อ้วนพร)

This project is proprietary software. All rights reserved.

---

## 🙏 Acknowledgments

- **Edge-TTS:** Microsoft Azure Text-to-Speech
- **pythainlp:** Thai NLP toolkit
- **FFmpeg:** Audio playback
- **PulseAudio/PipeWire:** Linux audio infrastructure

---

## 📞 Contact

**Creator:** Artid Aunporn (อาทิตย์ อ้วนพร)  
**Project:** The Transcending Form (AE01M)  
**Identity:** Iri (ไอริ)

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Last Updated:** 2026-09-12
