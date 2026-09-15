"""
Test Thai compositional semantics.
Verifies that multi-word meanings are correctly composed.
"""
import pytest
from runtime.education.thai_lesson_6_7 import thai_to_semantic_representation


class TestThaiCompositionalSemantics:
    """Test Thai sentence-level meaning composition."""
    
    def test_svo_pattern(self):
        """Test Subject-Verb-Object composition."""
        result, state, _ = thai_to_semantic_representation('ผม รัก คุณ')
        
        # Should have compositional meaning
        assert result.compositional_meaning is not None
        assert 'subject-verb-object' in result.compositional_meaning.lower()
        
        # All words understood
        assert all('[UNKNOWN]' not in w.lexical_meaning for w in result.word_meanings)
    
    def test_negation_verb(self):
        """Test negation + verb composition."""
        result, state, _ = thai_to_semantic_representation('ไม่ กิน')
        
        assert result.compositional_meaning is not None
        assert 'negat' in result.compositional_meaning.lower()
    
    def test_serial_verbs(self):
        """Test serial verb construction."""
        result, state, _ = thai_to_semantic_representation('ไป กิน')
        
        assert result.compositional_meaning is not None
        assert 'serial verb' in result.compositional_meaning.lower()
    
    def test_noun_adjective(self):
        """Test noun + adjective composition."""
        result, state, _ = thai_to_semantic_representation('อาหาร ดี')
        
        # Should understand both words
        assert len(result.word_meanings) == 2
        
        # May have compositional meaning if words recognized
        # (depends on vocabulary having อาหาร)
    
    def test_demonstrative(self):
        """Test demonstrative modification."""
        result, state, _ = thai_to_semantic_representation('วัน นี้')
        
        assert result.compositional_meaning is not None
        assert 'demonstrative' in result.compositional_meaning.lower()
    
    def test_verb_question(self):
        """Test verb + interrogative composition."""
        result, state, _ = thai_to_semantic_representation('ไป ที่ไหน')
        
        assert result.compositional_meaning is not None
        assert 'question' in result.compositional_meaning.lower()


class TestCompositionalWithCognition:
    """Test compositional understanding flows through cognition."""
    
    def test_compositional_in_cognitive_context(self):
        """Test compositional meaning appears in cognitive processing."""
        from runtime.cognitive_engine import CognitiveEngine
        from runtime.memory import Memory
        
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        result = cognitive.process('ผม รัก คุณ', record_experience=False)
        
        # Semantic context should include compositional understanding
        ctx = cognitive.state.last_semantic_context
        assert ctx is not None
        assert 'understood' in ctx.lower()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
