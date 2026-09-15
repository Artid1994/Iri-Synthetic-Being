"""
Test vocabulary learning from conversations.
"""
import pytest
from runtime.cognitive_engine import CognitiveEngine
from runtime.memory import Memory


class TestVocabularyLearning:
    """Test learning new vocabulary from conversations."""
    
    def test_unknown_word_tracked(self):
        """Test unknown words are tracked for learning."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        # Input with unknown word
        cognitive.process('สวัสดี ฟหกด ครับ', record_experience=False)
        
        # Check vocabulary learner tracked it
        bridge = cognitive.semantic_bridge
        unknown = bridge.vocabulary_learner.get_unknown_words(language='thai')
        
        assert len(unknown) > 0
        assert any(c.word == 'ฟหกด' for c in unknown)
    
    def test_teach_new_word(self):
        """Test teaching IRI a new word."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        # First encounter - unknown
        cognitive.process('นอน', record_experience=False)
        ctx1 = cognitive.state.last_semantic_context
        assert 'Unknown' in ctx1 or 'UNKNOWN' in ctx1
        
        # Teach the word
        bridge = cognitive.semantic_bridge
        success = bridge.vocabulary_learner.teach_word(
            word='นอน',
            language='thai',
            meaning='sleep',
            semantic_field='ACTION'
        )
        
        assert success
        
        # Second encounter - should be known now
        cognitive.process('นอน', record_experience=False)
        
        # Verify it's in semantic memory
        meaning = bridge.recall_semantic_understanding('นอน', 'thai')
        assert meaning is not None
        assert 'sleep' in meaning.lower()
    
    def test_unknown_words_list(self):
        """Test getting list of unknown words."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        # Encounter multiple unknown words
        cognitive.process('ฟหกด จดห ครับ', record_experience=False)
        
        bridge = cognitive.semantic_bridge
        unknown = bridge.vocabulary_learner.get_unknown_words(language='thai')
        
        assert len(unknown) >= 2
        unknown_words = [c.word for c in unknown]
        assert 'ฟหกด' in unknown_words
        assert 'จดห' in unknown_words
    
    def test_learning_persists(self):
        """Test learned words persist in semantic memory."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True)
        
        bridge = cognitive.semantic_bridge
        
        # Teach a word
        bridge.vocabulary_learner.teach_word(
            word='นอน',
            language='thai',
            meaning='sleep',
            semantic_field='ACTION'
        )
        
        # Verify it's stored
        vocab_size_before = bridge.get_vocabulary_size('thai')
        
        # Process input with the word
        cognitive.process('ไป นอน', record_experience=False)
        ctx = cognitive.state.last_semantic_context
        
        # Should understand it now
        assert 'นอน=sleep' in ctx or 'sleep' in ctx.lower()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
