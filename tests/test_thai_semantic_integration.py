"""
Integration test: Thai semantic understanding with actual curriculum.
Tests that semantic verification works end-to-end.
"""
import pytest
from runtime.education.thai_lesson_6_7 import thai_to_semantic_representation
from runtime.education.semantic_representation import EvidenceStatus

class TestThaiSemanticIntegration:
    """Test Thai language semantic understanding integration."""
    
    def test_basic_greeting_understood(self):
        """Test สวัสดี (hello) is semantically understood."""
        result, state, evidence = thai_to_semantic_representation('สวัสดี')
        
        assert state != 'UNKNOWN', 'สวัสดี should not be unknown'
        assert len(result.word_meanings) == 1
        assert result.word_meanings[0].word == 'สวัสดี'
        assert 'hello' in result.word_meanings[0].lexical_meaning.lower()
        assert result.confidence > 0.0
    
    def test_gratitude_understood(self):
        """Test ขอบคุณ (thank you) is understood."""
        result, state, evidence = thai_to_semantic_representation('ขอบคุณ')
        
        assert state == 'KNOWN', 'ขอบคุณ should be KNOWN'
        assert result.word_meanings[0].lexical_meaning == 'thank you'
        assert result.confidence >= 0.9  # High confidence even without context
    
    def test_polite_particles_understood(self):
        """Test ครับ/ค่ะ (polite particles) are understood."""
        # Male particle
        result1, state1, _ = thai_to_semantic_representation('ครับ')
        assert state1 == 'KNOWN'
        assert 'polite' in result1.word_meanings[0].lexical_meaning.lower()
        
        # Female particle
        result2, state2, _ = thai_to_semantic_representation('ค่ะ')
        assert state2 == 'KNOWN'
        assert 'polite' in result2.word_meanings[0].lexical_meaning.lower()
    
    def test_interrogatives_understood(self):
        """Test Thai question words are understood."""
        questions = {
            'อะไร': 'what',
            'ที่ไหน': 'where',
        }
        
        for thai, expected in questions.items():
            result, state, _ = thai_to_semantic_representation(thai)
            assert state == 'KNOWN', f'{thai} should be KNOWN'
            assert expected in result.word_meanings[0].lexical_meaning.lower()
    
    def test_negation_understood(self):
        """Test ไม่ (negation) is understood."""
        result, state, _ = thai_to_semantic_representation('ไม่')
        
        assert state == 'KNOWN'
        assert 'no' in result.word_meanings[0].lexical_meaning.lower() or 'not' in result.word_meanings[0].lexical_meaning.lower()
    
    def test_essential_verbs_understood(self):
        """Test essential Thai verbs are understood."""
        verbs = ['เป็น', 'มี', 'ทำ', 'ไป', 'กิน']
        
        for verb in verbs:
            result, state, _ = thai_to_semantic_representation(verb)
            # AMBIGUOUS is acceptable for context-dependent verbs
            assert state in ['KNOWN', 'AMBIGUOUS'], f'{verb} should be understood'
            assert '[UNKNOWN]' not in result.word_meanings[0].lexical_meaning
    
    def test_semantic_fields_assigned(self):
        """Test words have appropriate semantic fields."""
        result, _, _ = thai_to_semantic_representation('ไป')
        assert len(result.word_meanings) == 1
        # Has contextual meanings
        assert len(result.word_meanings[0].contextual_meanings) > 0
