"""
Semantic Cognitive Bridge
Integrates semantic understanding into cognitive processing.

Links:
- Thai semantic understanding (thai_lesson_6_7)
- Semantic memory (03_Hippocampus/semantic_memory_store.py)
- Cognitive engine (cognitive_engine.py)
"""
from __future__ import annotations
from typing import Optional, Tuple
import unicodedata
import sys
from pathlib import Path

# Add Hippocampus to path for semantic memory
sys.path.insert(0, str(Path(__file__).parent.parent / '03_Hippocampus'))
from semantic_memory_store import SemanticMemoryStore

from runtime.education.thai_lesson_6_7 import thai_to_semantic_representation
from runtime.education.semantic_representation import SemanticMeaning


def is_thai_text(text: str) -> bool:
    """Check if text contains Thai script."""
    if not text:
        return False
    
    for char in text:
        if '\u0e00' <= char <= '\u0e7f':  # Thai Unicode range
            return True
    return False


class SemanticCognitiveBridge:
    """
    Bridges semantic understanding with cognitive processing.
    
    When Thai input is detected:
    1. Convert to semantic representation
    2. Check semantic memory for known understanding
    3. Provide semantic context to reasoning
    4. Store new understanding if learned
    """
    
    def __init__(self, semantic_memory_path: str = "03_Hippocampus/semantic_memory.json"):
        self.semantic_memory = SemanticMemoryStore(semantic_memory_path)
        self.last_semantic_understanding: Optional[Tuple[str, SemanticMeaning]] = None
        
        # NEW: Vocabulary learning
        from runtime.vocabulary_learner import VocabularyLearner
        self.vocabulary_learner = VocabularyLearner(self.semantic_memory)
    
    def process_input(self, user_input: str) -> Tuple[str, Optional[str]]:
        """
        Process input through semantic understanding.
        
        Returns:
            (processed_input, semantic_context)
            
        If Thai:
            - processed_input: Thai text
            - semantic_context: Thai understanding evidence
        If English:
            - processed_input: English text
            - semantic_context: English understanding evidence
        If neither:
            - processed_input: original
            - semantic_context: None
        """
        if is_thai_text(user_input):
            return self._process_thai_input(user_input)
        else:
            # Assume English for now (could add more language detection)
            return self._process_english_input(user_input)
    
    def _process_thai_input(self, user_input: str) -> Tuple[str, Optional[str]]:
        """Process Thai input through semantic understanding."""
        
        # Thai input - get semantic understanding
        result, state, evidence = thai_to_semantic_representation(user_input)
        
        # NEW: Check semantic memory for dynamically learned words
        # (thai_to_semantic_representation only loads from JSON)
        for i, word_meaning in enumerate(result.word_meanings):
            if '[UNKNOWN]' in word_meaning.lexical_meaning:
                # Check if word was learned dynamically
                learned = self.semantic_memory.recall_understanding(word_meaning.word, 'thai')
                if learned:
                    # Replace with learned meaning
                    from runtime.education.semantic_representation import SemanticMeaning, EvidenceStatus
                    result.word_meanings[i] = SemanticMeaning(
                        word=word_meaning.word,
                        lexical_meaning=learned.lexical_meaning,
                        semantic_field='LEARNED',
                        confidence=learned.confidence,
                        evidence_status=EvidenceStatus.KNOWN,
                    )
        
        # Build semantic context
        words_understood = []
        words_unknown = []
        
        for word_meaning in result.word_meanings:
            if '[UNKNOWN]' not in word_meaning.lexical_meaning:
                words_understood.append(f"{word_meaning.word}={word_meaning.lexical_meaning}")
            else:
                words_unknown.append(word_meaning.word)
                # NEW: Track unknown words for learning
                self.vocabulary_learner.track_unknown_word(
                    word=word_meaning.word,
                    language='thai',
                    context=user_input
                )
        
        # Construct semantic context
        if words_understood:
            semantic_context = f"Thai understood: {', '.join(words_understood)}"
            if words_unknown:
                semantic_context += f" | Unknown: {', '.join(words_unknown)}"
            semantic_context += f" | State: {state}"
        else:
            semantic_context = f"Thai not understood: {user_input} | State: {state}"
        
        # Store understanding in semantic memory
        if words_understood and result.word_meanings:
            for word_meaning in result.word_meanings:
                if '[UNKNOWN]' not in word_meaning.lexical_meaning:
                    self.semantic_memory.store_understanding(
                        word=word_meaning.word,
                        language='thai',
                        meaning=word_meaning,
                        context=user_input
                    )
        
        return user_input, semantic_context
    
    def _process_english_input(self, user_input: str) -> Tuple[str, Optional[str]]:
        """Process English input through semantic understanding."""
        import json
        from pathlib import Path
        
        # Load English vocabulary
        vocab_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "english_language" / "semantic_vocabulary.json"
        
        if not vocab_path.exists():
            # No English vocabulary yet
            return user_input, "English input (no semantic vocabulary loaded)"
        
        vocab_data = json.loads(vocab_path.read_text())
        vocab = vocab_data.get('semantic_vocabulary', [])
        
        # Simple word-level understanding
        words = user_input.lower().split()
        words_understood = []
        words_unknown = []
        
        for word in words:
            word_data = next((v for v in vocab if v['word'].lower() == word.lower()), None)
            if word_data:
                meaning = word_data['lexical_meaning']
                words_understood.append(f"{word}={meaning}")
            else:
                words_unknown.append(word)
                # Track unknown English words for learning
                self.vocabulary_learner.track_unknown_word(
                    word=word,
                    language='english',
                    context=user_input
                )
        
        # Build semantic context
        if words_understood:
            semantic_context = f"English understood: {', '.join(words_understood)}"
            if words_unknown:
                semantic_context += f" | Unknown: {', '.join(words_unknown)}"
            semantic_context += " | State: KNOWN" if not words_unknown else " | State: PARTIAL"
        else:
            semantic_context = f"English not understood: {user_input} | State: UNKNOWN"
        
        return user_input, semantic_context
    
    def recall_semantic_understanding(self, word: str, language: str) -> Optional[str]:
        """
        Recall semantic understanding from memory.
        
        Returns lexical meaning if known, None otherwise.
        """
        entry = self.semantic_memory.recall_understanding(word, language)
        if entry:
            return entry.lexical_meaning
        return None
    
    def get_vocabulary_size(self, language: str = 'thai') -> int:
        """Get number of words understood in a language."""
        return self.semantic_memory.get_vocabulary_size(language)
