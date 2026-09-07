"""Test suite for AE01M Cerebellum Voice Synthesis and Cognitive Loop integration."""

import os
import sys
from importlib.machinery import SourceFileLoader
import pytest

voice_mod = SourceFileLoader(
    "voice_synthesis", "04_Cerebellum/voice_synthesis.py"
).load_module()
VoiceSynthesizer = voice_mod.VoiceSynthesizer


def test_voice_synthesizer_thai_detection():
    synth = VoiceSynthesizer()
    assert synth._contains_thai("สวัสดี") is True
    assert synth._contains_thai("Hello World") is False
    assert synth.select_voice("สวัสดี ไอริ") == VoiceSynthesizer.DEFAULT_THAI_VOICE
    assert synth.select_voice("Hello Iri") == VoiceSynthesizer.DEFAULT_ENGLISH_VOICE


def test_voice_synthesizer_synthesis_and_play():
    synth = VoiceSynthesizer()
    text = "ระบบเสียงของ AE01M พร้อมทำงานแล้วครับคุณอาทิตย์"
    out_file = synth.synthesize(text)
    assert out_file is not None
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0

    # Test playback via detected system player (ffplay/paplay)
    played = synth.play(out_file, block=True)
    assert played is True

    # Cleanup test artifact
    if os.path.exists(out_file):
        os.remove(out_file)
