"""
Test semantic memory persistence.
"""
import pytest
from pathlib import Path
import tempfile
import os

from runtime.education.thai_lesson_6_7 import thai_to_semantic_representation  
from runtime.education.semantic_representation import SemanticMeaning, EvidenceStatus
# Import from 03_Hippocampus not hippocampus module
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / '03_Hippocampus'))
from semantic_memory_store import SemanticMemoryStore, SemanticMemoryEntry


class TestSemanticMemoryIntegration:
    """Test semantic understanding persists in memory."""
    
    def test_store_thai_understanding(self, tmp_path):
        """Test storing Thai semantic understanding."""
        memory_file = tmp_path / "test_semantic.json"
        store = SemanticMemoryStore(str(memory_file))
        
        # Get semantic understanding
        result, state, _ = thai_to_semantic_representation('สวัสดี')
        assert state != 'UNKNOWN'
        
        # Store it
        store.store_understanding(
            word='สวัสดี',
            language='thai',
            meaning=result.word_meanings[0],
            context='greeting'
        )
        
        # Verify stored
        assert memory_file.exists()
        assert store.get_vocabulary_size('thai') == 1
    
    def test_recall_understanding(self, tmp_path):
        """Test recalling stored understanding."""
        memory_file = tmp_path / "test_semantic.json"
        store = SemanticMemoryStore(str(memory_file))
        
        # Store understanding
        result, _, _ = thai_to_semantic_representation('ขอบคุณ')
        store.store_understanding('ขอบคุณ', 'thai', result.word_meanings[0])
        
        # Recall it
        recalled = store.recall_understanding('ขอบคุณ', 'thai')
        assert recalled is not None
        assert recalled.word == 'ขอบคุณ'
        assert 'thank' in recalled.lexical_meaning.lower()
        assert recalled.confidence >= 0.9
    
    def test_vocabulary_growth(self, tmp_path):
        """Test vocabulary size tracking."""
        memory_file = tmp_path / "test_semantic.json"
        store = SemanticMemoryStore(str(memory_file))
        
        words = ['สวัสดี', 'ขอบคุณ', 'ใช่', 'ไม่']
        
        for word in words:
            result, _, _ = thai_to_semantic_representation(word)
            if result.word_meanings:
                store.store_understanding(word, 'thai', result.word_meanings[0])
        
        assert store.get_vocabulary_size('thai') == len(words)
    
    def test_persistence_across_sessions(self, tmp_path):
        """Test memory persists across instances."""
        memory_file = tmp_path / "test_semantic.json"
        
        # First session
        store1 = SemanticMemoryStore(str(memory_file))
        result, _, _ = thai_to_semantic_representation('รัก')
        store1.store_understanding('รัก', 'thai', result.word_meanings[0])
        vocab_size_1 = store1.get_vocabulary_size('thai')
        
        # Second session (new instance)
        store2 = SemanticMemoryStore(str(memory_file))
        vocab_size_2 = store2.get_vocabulary_size('thai')
        
        assert vocab_size_1 == vocab_size_2 == 1
        
        recalled = store2.recall_understanding('รัก', 'thai')
        assert recalled is not None
        assert 'love' in recalled.lexical_meaning.lower()
