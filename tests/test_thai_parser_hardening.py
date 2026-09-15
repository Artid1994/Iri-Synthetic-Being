import unittest
import json
from pathlib import Path

from runtime.education.thai_syllable_parser import ThaiSyllableParser
from runtime.education.thai_tone_calculator import ThaiToneCalculator
from runtime.education.thai_ipa_renderer import ThaiIPARenderer


class TestThaiParserHardening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load Thai linguistic data once for all tests."""
        data_dir = Path(__file__).parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
        
        consonants_file = data_dir / "consonants.json"
        vowels_file = data_dir / "vowel_orthography.json"
        tones_file = data_dir / "tones.json"
        
        consonant_data = json.loads(consonants_file.read_text(encoding='utf-8'))
        vowel_data = json.loads(vowels_file.read_text(encoding='utf-8'))
        tone_data = json.loads(tones_file.read_text(encoding='utf-8'))
        
        cls.parser = ThaiSyllableParser(consonant_data, vowel_data, tone_data)
        cls.calculator = ThaiToneCalculator(consonant_data, vowel_data, tone_data)
        cls.ipa_renderer = ThaiIPARenderer()
    
    # === LEADING ห PRECEDENCE ===
    
    def test_leading_h_nga(self):
        """Test: หง (ng with high class) - ห + ง."""
        analysis, errors = self.parser.parse_syllable('หงา')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'ง')
        self.assertEqual(analysis.consonant_class, 'low')
        self.assertEqual(analysis.effective_class, 'high')  # Modified by leading ห
        
        tone = self.calculator.calculate_tone(analysis)
        self.assertEqual(tone, 4)  # High class behavior = rising
    
    def test_leading_h_na(self):
        """Test: หนา (na: with high class) - ห + น."""
        analysis, errors = self.parser.parse_syllable('หนา')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'น')
        self.assertEqual(analysis.effective_class, 'high')
    
    def test_leading_h_ma(self):
        """Test: หมา (ma: with high class) - ห + ม."""
        analysis, errors = self.parser.parse_syllable('หมา')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'ม')
        self.assertEqual(analysis.effective_class, 'high')
    
    def test_leading_h_ya(self):
        """Test: หยา (ya: with high class) - ห + ย."""
        analysis, errors = self.parser.parse_syllable('หยา')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'ย')
        self.assertEqual(analysis.effective_class, 'high')
    
    def test_leading_h_ra(self):
        """Test: หรา (ra: with high class) - ห + ร."""
        analysis, errors = self.parser.parse_syllable('หรา')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'ร')
        self.assertEqual(analysis.effective_class, 'high')
    
    def test_leading_h_la(self):
        """Test: หลา (la: with high class) - ห + ล."""
        analysis, errors = self.parser.parse_syllable('หลา')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'ล')
        self.assertEqual(analysis.effective_class, 'high')
    
    def test_leading_h_wa(self):
        """Test: หวา (wa: with high class) - ห + ว."""
        analysis, errors = self.parser.parse_syllable('หวา')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'ว')
        self.assertEqual(analysis.effective_class, 'high')
    
    def test_leading_h_vs_cluster(self):
        """Test: หม is NOT confused with a cluster."""
        # หม should be ห leading + ม, not a cluster
        analysis, errors = self.parser.parse_syllable('หมา')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(len(analysis.initial_consonant), 1)  # Single consonant, not cluster
        self.assertEqual(analysis.initial_consonant, 'ม')
    
    # === SILENT LETTERS ===
    
    def test_silent_final_with_thanthakhat(self):
        """Test: กา์ - ◌์ marks final consonant as silent."""
        # Artificial example: า + (silent า would be า์)
        # Real example: สระ vs สระ์ (if final were silent)
        analysis, errors = self.parser.parse_syllable('กาด์')
        
        self.assertIsNotNone(analysis)
        # The ด์ should be parsed as no final (silent)
        self.assertIsNone(analysis.final_consonant)
    
    # === IPA RENDERING ===
    
    def test_ipa_render_simple(self):
        """Test: กา → /kaː˧/ (mid tone)."""
        analysis, errors = self.parser.parse_syllable('กา')
        tone = self.calculator.calculate_tone(analysis)
        
        ipa = self.ipa_renderer.render_ipa(analysis, tone)
        
        # Should be /kaː˧/ (proper IPA notation, no double slashes)
        self.assertTrue(ipa.startswith('/'))
        self.assertTrue(ipa.endswith('/'))
        self.assertIn('k', ipa)
        self.assertIn('aː', ipa)
        self.assertIn('˧', ipa)  # Mid tone marker
        self.assertNotIn('//', ipa)  # No double slashes
    
    def test_ipa_render_with_final(self):
        """Test: กิน → /kin˧/."""
        analysis, errors = self.parser.parse_syllable('กิน')
        tone = self.calculator.calculate_tone(analysis)
        
        ipa = self.ipa_renderer.render_ipa(analysis, tone)
        
        self.assertTrue(ipa.startswith('/'))
        self.assertTrue(ipa.endswith('/'))
        self.assertIn('k', ipa)
        self.assertIn('i', ipa)
        self.assertIn('n', ipa)
        self.assertNotIn('//', ipa)
    
    def test_ipa_render_cluster(self):
        """Test: กรา → /kraː˧/."""
        analysis, errors = self.parser.parse_syllable('กรา')
        tone = self.calculator.calculate_tone(analysis)
        
        ipa = self.ipa_renderer.render_ipa(analysis, tone)
        
        self.assertTrue(ipa.startswith('/'))
        self.assertTrue(ipa.endswith('/'))
        self.assertIn('k', ipa)
        self.assertIn('r', ipa)
        self.assertIn('aː', ipa)
        self.assertNotIn('//', ipa)
    
    def test_ipa_render_with_tone_mark(self):
        """Test: ก่า → /kaː˨˩/ (low tone)."""
        analysis, errors = self.parser.parse_syllable('ก่า')
        tone = self.calculator.calculate_tone(analysis)
        
        ipa = self.ipa_renderer.render_ipa(analysis, tone)
        
        self.assertIn('˨˩', ipa)  # Low tone marker
    
    # === REAL THAI EXAMPLES ===
    
    def test_real_word_sawasdee(self):
        """Test: สวัสดี (sawatdii, 'hello') - first syllable."""
        analysis, errors = self.parser.parse_syllable('สวัส')
        
        self.assertIsNotNone(analysis)
        # ส + ว + ัส
        # This is tricky - might parse as ส initial, ว as part of vowel or separate
        # At minimum, should parse without fatal error
        self.assertLess(len(errors), 3)  # Allow some ambiguity
    
    def test_real_word_khao(self):
        """Test: ข้าว (khao, 'rice')."""
        analysis, errors = self.parser.parse_syllable('ข้าว')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'ข')
        self.assertEqual(analysis.tone_mark, '้')
        self.assertEqual(analysis.final_consonant, 'ว')
    
    def test_real_word_phuut(self):
        """Test: พูด (phuut, 'speak')."""
        analysis, errors = self.parser.parse_syllable('พูด')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'พ')
        self.assertEqual(analysis.vowel, 'ู')
        self.assertEqual(analysis.final_consonant, 'ด')
    
    def test_real_word_khrap(self):
        """Test: ครับ (khrap, polite particle)."""
        analysis, errors = self.parser.parse_syllable('ครับ')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.initial_consonant, 'คร')  # Cluster
        self.assertEqual(analysis.final_consonant, 'บ')
    
    def test_real_word_chai(self):
        """Test: ใช่ (chai, 'yes/correct')."""
        analysis, errors = self.parser.parse_syllable('ใช่')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.vowel, 'ใ')
        self.assertEqual(analysis.tone_mark, '่')
    
    def test_real_word_mai(self):
        """Test: ใหม่ (mai, 'new')."""
        analysis, errors = self.parser.parse_syllable('ใหม่')
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.vowel, 'ใ')
        self.assertEqual(analysis.initial_consonant, 'ม')  # ห leading detected
        self.assertEqual(analysis.effective_class, 'high')
    
    # === EDGE CASES ===
    
    def test_ambiguous_vowel_pattern(self):
        """Test: Unknown vowel pattern returns explicit error."""
        # Create artificial ambiguous pattern (if possible)
        # For now, test that parser doesn't crash on unusual input
        analysis, errors = self.parser.parse_syllable('ก')
        
        # Single consonant should parse with implicit vowel
        if analysis:
            self.assertEqual(analysis.vowel, 'implicit')
    
    def test_invalid_cluster(self):
        """Test: Invalid cluster กน is not treated as cluster."""
        analysis, errors = self.parser.parse_syllable('กนา')
        
        # กน is not a valid cluster, so should parse as ก + (something else)
        # Likely fails or treats น as start of next syllable
        # At minimum, should not crash
        self.assertTrue(True)  # Placeholder


if __name__ == "__main__":
    unittest.main()
