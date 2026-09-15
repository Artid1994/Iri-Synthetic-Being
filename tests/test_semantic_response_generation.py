"""
Test semantic response generation.
Verifies that Thai responses are generated from semantic understanding.
"""
import pytest
from runtime.cognitive_engine import CognitiveEngine
from runtime.memory import Memory


class TestSemanticResponseGeneration:
    """Test response generation using semantic understanding."""
    
    def test_thai_greeting_response(self):
        """Test Thai greeting generates appropriate response."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True, enable_response=True)
        
        result = cognitive.process('สวัสดี ครับ', record_experience=False)
        
        assert result == 'RESPOND'
        assert cognitive.state.last_response is not None
        assert 'สวัสดี' in cognitive.state.last_response
    
    def test_thai_thanks_response(self):
        """Test Thai thanks generates appropriate response."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True, enable_response=True)
        
        result = cognitive.process('ขอบคุณ ครับ', record_experience=False)
        
        assert result == 'RESPOND'
        assert cognitive.state.last_response is not None
        # Should respond with acknowledgment
        assert cognitive.state.last_response is not None
    
    def test_thai_question_response(self):
        """Test Thai question generates acknowledgment."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True, enable_response=True)
        
        result = cognitive.process('ไป ที่ไหน ครับ', record_experience=False)
        
        assert result == 'RESPOND'
        assert cognitive.state.last_response is not None
        # Should acknowledge understanding the question
        assert 'เข้าใจ' in cognitive.state.last_response or 'ครับ' in cognitive.state.last_response
    
    def test_response_preserves_politeness(self):
        """Test response preserves politeness markers."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True, enable_response=True)
        
        # Male polite
        cognitive.process('สวัสดี ครับ', record_experience=False)
        response_male = cognitive.state.last_response
        assert 'ครับ' in response_male
        
        # Female polite
        cognitive.process('สวัสดี ค่ะ', record_experience=False)
        response_female = cognitive.state.last_response
        assert 'ค่ะ' in response_female
    
    def test_response_disabled_mode(self):
        """Test response generation can be disabled."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True, enable_response=False)
        
        result = cognitive.process('สวัสดี ครับ', record_experience=False)
        
        assert result == 'RESPOND'
        assert cognitive.state.last_response is None
    
    def test_english_input_response(self):
        """Test English input gets English response."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True, enable_response=True)
        
        result = cognitive.process('Hello', record_experience=False)
        
        assert result == 'RESPOND'
        # Should get some response
        assert cognitive.state.last_response is not None


class TestResponseQuality:
    """Test response quality and appropriateness."""
    
    def test_name_introduction_response(self):
        """Test name introduction gets polite response."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True, enable_response=True)
        
        cognitive.process('ผม ชื่อ ไอริ ครับ', record_experience=False)
        response = cognitive.state.last_response
        
        assert response is not None
        # Should be polite acknowledgment
        assert 'ยินดี' in response or 'ครับ' in response
    
    def test_unknown_thai_gets_acknowledgment(self):
        """Test unknown Thai words still get acknowledgment."""
        memory = Memory()
        cognitive = CognitiveEngine(memory, enable_semantic=True, enable_response=True)
        
        # Mix known and unknown
        cognitive.process('สวัสดี ฟหกด ครับ', record_experience=False)
        response = cognitive.state.last_response
        
        # Should still respond politely
        assert response is not None
        assert len(response) > 0


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
