"""
Test semantic cognitive integration.
Verifies that Thai semantic understanding flows through cognitive engine.
"""
import pytest
from runtime.cognitive_engine import CognitiveEngine
from runtime.memory import Memory


class TestSemanticCognitiveIntegration:
    """Test semantic understanding integrated into cognition."""
    
    def test_thai_input_uses_semantic_bridge(self):
        """Test Thai input is processed through semantic bridge."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        result = cognitive.process('สวัสดี', record_experience=False)
        
        # Should have semantic context
        assert cognitive.state.last_semantic_context is not None
        assert 'Thai understood' in cognitive.state.last_semantic_context
        assert 'สวัสดี' in cognitive.state.last_semantic_context
        assert 'hello' in cognitive.state.last_semantic_context.lower()
    
    def test_english_input_no_semantic_processing(self):
        """Test English input gets semantic processing."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        result = cognitive.process('Hello', record_experience=False)
        
        # Should have English semantic context now
        assert cognitive.state.last_semantic_context is not None
        assert 'English' in cognitive.state.last_semantic_context
    
    def test_thai_understanding_in_recall(self):
        """Test semantic understanding appears in recall."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        cognitive.process('ขอบคุณ', record_experience=False)
        
        # Semantic understanding should be in recalled context
        recalled = cognitive.state.last_recalled
        assert recalled is not None
        assert 'Semantic:' in recalled
        assert 'Thai understood' in recalled
        assert 'ขอบคุณ' in recalled
    
    def test_thai_understanding_affects_reasoning(self):
        """Test semantic understanding flows to reasoning."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        cognitive.process('รัก', record_experience=False)
        
        # Reasoning should include semantic context
        reasoning = cognitive.state.last_reasoning
        assert reasoning is not None
        assert len(reasoning) > 0
    
    def test_semantic_memory_persistence(self):
        """Test semantic understanding persists across cognitive cycles."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        # Process multiple Thai words
        words = ['สวัสดี', 'ขอบคุณ', 'ไป', 'กิน']
        for word in words:
            cognitive.process(word, record_experience=False)
        
        # Check semantic memory grew
        vocab_size = cognitive.semantic_bridge.get_vocabulary_size('thai')
        assert vocab_size >= len(words)
    
    def test_unknown_thai_word_tracked(self):
        """Test unknown Thai words are tracked as UNKNOWN."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        # Made-up Thai-like text
        cognitive.process('ฟหกด', record_experience=False)
        
        # Should have semantic context indicating unknown
        ctx = cognitive.state.last_semantic_context
        assert ctx is not None
        assert 'Unknown' in ctx or 'UNKNOWN' in ctx
    
    def test_mixed_known_unknown_thai(self):
        """Test Thai input with both known and unknown words."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        # Mix known word (สวัสดี) with unknown
        cognitive.process('สวัสดี ฟหกด', record_experience=False)
        
        ctx = cognitive.state.last_semantic_context
        assert ctx is not None
        assert 'สวัสดี' in ctx
        assert ('understood' in ctx.lower() or 'unknown' in ctx.lower())
    
    def test_semantic_disabled_mode(self):
        """Test cognition works without semantic bridge."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=False)
        
        result = cognitive.process('สวัสดี', record_experience=False)
        
        # No semantic context when disabled
        assert cognitive.state.last_semantic_context is None
        assert cognitive.semantic_bridge is None
    
    def test_cognitive_state_includes_semantic(self):
        """Test cognitive state snapshot includes semantic context."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        cognitive.process('ไทย', record_experience=False)
        snapshot = cognitive.snapshot()
        
        assert hasattr(snapshot, 'last_semantic_context')
        assert snapshot.last_semantic_context is not None


class TestSemanticMemoryRecall:
    """Test semantic memory recall from cognition."""
    
    def test_recall_semantic_understanding(self):
        """Test recalling semantic understanding through bridge."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        # Process and store
        cognitive.process('ชอบ', record_experience=False)
        
        # Recall through bridge
        meaning = cognitive.semantic_bridge.recall_semantic_understanding('ชอบ', 'thai')
        assert meaning is not None
        assert 'like' in meaning.lower()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
