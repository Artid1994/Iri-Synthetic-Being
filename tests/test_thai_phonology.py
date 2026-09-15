import unittest
import json
from pathlib import Path

from runtime.education.thai_tone_calculator import (
    ThaiToneCalculator,
    SyllableAnalysis,
)


class TestThaiToneCalculator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load Thai linguistic data once for all tests."""
        data_dir = Path(__file__).parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
        
        consonants_file = data_dir / "consonants.json"
        vowels_file = data_dir / "vowel_orthography.json"
        tones_file = data_dir / "tones.json"
        
        consonant_data = json.loads(consonants_file.read_text(encoding='utf-8'))
        vowel_data = json.loads(vowels_file.read_text(encoding='utf-8'))
        tone_rules = json.loads(tones_file.read_text(encoding='utf-8'))
        
        cls.calculator = ThaiToneCalculator(consonant_data, vowel_data, tone_rules)
    
    def test_determine_syllable_type_live_long_vowel(self):
        """Test live syllable: long vowel, no final."""
        is_live = self.calculator.determine_syllable_type('long', None)
        self.assertTrue(is_live)
    
    def test_determine_syllable_type_live_sonorant_final(self):
        """Test live syllable: short vowel + sonorant final."""
        is_live = self.calculator.determine_syllable_type('short', 'น')
        self.assertTrue(is_live)
    
    def test_determine_syllable_type_live_long_vowel_sonorant(self):
        """Test live syllable: long vowel + sonorant final."""
        is_live = self.calculator.determine_syllable_type('long', 'ง')
        self.assertTrue(is_live)
    
    def test_determine_syllable_type_dead_short_vowel_stop(self):
        """Test dead syllable: short vowel + stop final."""
        is_live = self.calculator.determine_syllable_type('short', 'ก')
        self.assertFalse(is_live)
    
    def test_determine_syllable_type_dead_short_vowel_alone(self):
        """Test dead syllable: short vowel, no final."""
        is_live = self.calculator.determine_syllable_type('short', None)
        self.assertFalse(is_live)
    
    def test_determine_syllable_type_live_long_vowel_stop(self):
        """Test live syllable: long vowel + stop final."""
        is_live = self.calculator.determine_syllable_type('long', 'ก')
        self.assertTrue(is_live)
    
    def test_leading_h_modification_applies(self):
        """Test ห leading before low-class sonorant → high class."""
        effective = self.calculator.apply_leading_h_modification('น', 'low', leading_h=True)
        self.assertEqual(effective, 'high')
    
    def test_leading_h_modification_no_h(self):
        """Test no modification without leading ห."""
        effective = self.calculator.apply_leading_h_modification('น', 'low', leading_h=False)
        self.assertEqual(effective, 'low')
    
    def test_leading_h_modification_not_sonorant(self):
        """Test ห before non-sonorant doesn't modify."""
        effective = self.calculator.apply_leading_h_modification('ก', 'mid', leading_h=True)
        self.assertEqual(effective, 'mid')
    
    def test_calculate_tone_mid_live_no_mark(self):
        """Test: mid class + live syllable + no mark = tone 0 (mid)."""
        analysis = SyllableAnalysis(
            initial_consonant='ก',
            consonant_class='mid',
            vowel='◌า',
            vowel_length='long',
            final_consonant=None,
            tone_mark=None,
            is_live=True,
            effective_class='mid'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 0)
        self.assertEqual(self.calculator.get_tone_name(tone), "mid tone")
    
    def test_calculate_tone_mid_live_mai_ek(self):
        """Test: mid class + live syllable + ◌่ = tone 1 (low)."""
        analysis = SyllableAnalysis(
            initial_consonant='ก',
            consonant_class='mid',
            vowel='◌า',
            vowel_length='long',
            final_consonant=None,
            tone_mark='่',  # Tone mark without dotted circle
            is_live=True,
            effective_class='mid'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 1)
        self.assertEqual(self.calculator.get_tone_name(tone), "low tone")
    
    def test_calculate_tone_high_live_no_mark(self):
        """Test: high class + live syllable + no mark = tone 4 (rising)."""
        analysis = SyllableAnalysis(
            initial_consonant='ข',
            consonant_class='high',
            vowel='◌า',
            vowel_length='long',
            final_consonant=None,
            tone_mark=None,
            is_live=True,
            effective_class='high'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 4)
        self.assertEqual(self.calculator.get_tone_name(tone), "rising tone")
    
    def test_calculate_tone_low_live_no_mark(self):
        """Test: low class + live syllable + no mark = tone 0 (mid)."""
        analysis = SyllableAnalysis(
            initial_consonant='ค',
            consonant_class='low',
            vowel='◌า',
            vowel_length='long',
            final_consonant=None,
            tone_mark=None,
            is_live=True,
            effective_class='low'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 0)
    
    def test_calculate_tone_low_live_mai_ek(self):
        """Test: low class + live syllable + ◌่ = tone 2 (falling)."""
        analysis = SyllableAnalysis(
            initial_consonant='ค',
            consonant_class='low',
            vowel='◌า',
            vowel_length='long',
            final_consonant=None,
            tone_mark='่',  # Tone mark without dotted circle
            is_live=True,
            effective_class='low'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 2)
        self.assertEqual(self.calculator.get_tone_name(tone), "falling tone")
    
    def test_calculate_tone_low_live_mai_tho(self):
        """Test: low class + live syllable + ◌้ = tone 3 (high)."""
        analysis = SyllableAnalysis(
            initial_consonant='ค',
            consonant_class='low',
            vowel='◌า',
            vowel_length='long',
            final_consonant=None,
            tone_mark='้',  # Tone mark without dotted circle
            is_live=True,
            effective_class='low'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 3)
        self.assertEqual(self.calculator.get_tone_name(tone), "high tone")
    
    def test_calculate_tone_mid_dead_short(self):
        """Test: mid class + dead syllable (short vowel) = tone 1 (low)."""
        analysis = SyllableAnalysis(
            initial_consonant='ก',
            consonant_class='mid',
            vowel='◌ะ',
            vowel_length='short',
            final_consonant=None,
            tone_mark=None,
            is_live=False,
            effective_class='mid'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 1)
    
    def test_calculate_tone_high_dead_short(self):
        """Test: high class + dead syllable (short vowel) = tone 1 (low)."""
        analysis = SyllableAnalysis(
            initial_consonant='ข',
            consonant_class='high',
            vowel='◌ะ',
            vowel_length='short',
            final_consonant=None,
            tone_mark=None,
            is_live=False,
            effective_class='high'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 1)
    
    def test_calculate_tone_low_dead_short(self):
        """Test: low class + dead syllable (short vowel) = tone 3 (high)."""
        analysis = SyllableAnalysis(
            initial_consonant='ค',
            consonant_class='low',
            vowel='◌ะ',
            vowel_length='short',
            final_consonant=None,
            tone_mark=None,
            is_live=False,
            effective_class='low'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 3)
    
    def test_calculate_tone_low_dead_long(self):
        """Test: low class + dead syllable (long vowel + stop) = tone 2 (falling)."""
        analysis = SyllableAnalysis(
            initial_consonant='ค',
            consonant_class='low',
            vowel='◌า',
            vowel_length='long',
            final_consonant='ก',
            tone_mark=None,
            is_live=False,
            effective_class='low'
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 2)
    
    def test_calculate_tone_with_leading_h(self):
        """Test: ห leading + low sonorant → high class behavior."""
        analysis = SyllableAnalysis(
            initial_consonant='น',
            consonant_class='low',
            vowel='◌า',
            vowel_length='long',
            final_consonant=None,
            tone_mark=None,
            is_live=True,
            effective_class='high'  # Modified by leading ห
        )
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 4)  # High class, live, no mark = rising


class TestSyllableStructureData(unittest.TestCase):
    def test_load_syllable_structure(self):
        """Test that syllable structure data loads correctly."""
        data_dir = Path(__file__).parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
        syllable_file = data_dir / "syllable_structure.json"
        
        data = json.loads(syllable_file.read_text(encoding='utf-8'))
        
        self.assertIn('syllable_structure', data)
        self.assertIn('live_vs_dead', data)
        self.assertIn('consonant_clusters', data)
        self.assertIn('leading_h_modification', data)
    
    def test_consonant_clusters_data(self):
        """Test consonant cluster data structure."""
        data_dir = Path(__file__).parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
        syllable_file = data_dir / "syllable_structure.json"
        
        data = json.loads(syllable_file.read_text(encoding='utf-8'))
        clusters = data['consonant_clusters']
        
        self.assertIn('cluster_types', clusters)
        self.assertIn('stop_liquid', clusters['cluster_types'])
        
        valid_clusters = clusters['cluster_types']['stop_liquid']['valid']
        self.assertIn('กร', valid_clusters)
        self.assertIn('ปล', valid_clusters)


class TestConsonantPhonology(unittest.TestCase):
    def test_load_consonant_phonology(self):
        """Test that consonant phonology data loads correctly."""
        data_dir = Path(__file__).parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
        phon_file = data_dir / "consonant_phonology.json"
        
        data = json.loads(phon_file.read_text(encoding='utf-8'))
        
        self.assertIn('consonant_phonemes', data)
        self.assertGreater(len(data['consonant_phonemes']), 40)
    
    def test_consonant_ipa_data(self):
        """Test consonant IPA transcriptions."""
        data_dir = Path(__file__).parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
        phon_file = data_dir / "consonant_phonology.json"
        
        data = json.loads(phon_file.read_text(encoding='utf-8'))
        
        # Find ก (ko kai)
        ko_kai = [c for c in data['consonant_phonemes'] if c['grapheme'] == 'ก'][0]
        
        self.assertEqual(ko_kai['ipa'], '/k/')
        self.assertEqual(ko_kai['place'], 'velar')
        self.assertEqual(ko_kai['manner'], 'stop')
        self.assertEqual(ko_kai['voicing'], 'voiceless')
        self.assertEqual(ko_kai['class'], 'mid')
    
    def test_sonorant_identification(self):
        """Test sonorant consonants are marked."""
        data_dir = Path(__file__).parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
        phon_file = data_dir / "consonant_phonology.json"
        
        data = json.loads(phon_file.read_text(encoding='utf-8'))
        
        sonorants = [c for c in data['consonant_phonemes'] if c.get('sonorant')]
        sonorant_graphemes = [c['grapheme'] for c in sonorants]
        
        # Check that nasals and liquids are marked as sonorants
        self.assertIn('ง', sonorant_graphemes)
        self.assertIn('น', sonorant_graphemes)
        self.assertIn('ม', sonorant_graphemes)
        self.assertIn('ย', sonorant_graphemes)
        self.assertIn('ร', sonorant_graphemes)
        self.assertIn('ล', sonorant_graphemes)
        self.assertIn('ว', sonorant_graphemes)


if __name__ == "__main__":
    unittest.main()
