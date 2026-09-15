"""
Vocabulary Learning from Experience
Learns new vocabulary from conversations.

When IRI encounters unknown words, it can learn them through:
1. Explicit teaching (user provides meaning)
2. Context inference (future: use surrounding words)
3. Confirmation (verify understanding)
"""
from __future__ import annotations
from typing import Optional, Dict, List
from dataclasses import dataclass
import time


@dataclass
class VocabularyLearningCandidate:
    """A word candidate for learning."""
    word: str
    language: str  # 'thai', 'english'
    proposed_meaning: Optional[str] = None
    context: Optional[str] = None  # Sentence where word appeared
    confidence: float = 0.0
    timestamp: float = 0.0
    source: str = "conversation"  # 'conversation', 'teaching', 'inference'


class VocabularyLearner:
    """
    Learns new vocabulary from conversations.
    
    Tracks unknown words and enables learning through teaching or inference.
    """
    
    def __init__(self, semantic_memory_store):
        self.semantic_memory = semantic_memory_store
        self.unknown_words: List[VocabularyLearningCandidate] = []
        self.pending_confirmation: Optional[VocabularyLearningCandidate] = None
    
    def track_unknown_word(
        self,
        word: str,
        language: str,
        context: Optional[str] = None
    ) -> VocabularyLearningCandidate:
        """
        Track an unknown word for learning.
        
        Returns the learning candidate.
        """
        candidate = VocabularyLearningCandidate(
            word=word,
            language=language,
            context=context,
            timestamp=time.time(),
            source="conversation"
        )
        
        # Check if already tracked recently (within last 60 seconds)
        recent = [
            c for c in self.unknown_words 
            if c.word == word 
            and c.language == language 
            and (time.time() - c.timestamp) < 60
        ]
        
        if not recent:
            self.unknown_words.append(candidate)
        
        return candidate
    
    def teach_word(
        self,
        word: str,
        language: str,
        meaning: str,
        semantic_field: str = "UNKNOWN",
        confidence: float = 1.0
    ) -> bool:
        """
        Teach IRI a new word explicitly.
        
        Args:
            word: The word to learn
            language: Language ('thai', 'english')
            meaning: The meaning/translation
            semantic_field: Optional semantic category
            confidence: Confidence in this teaching (default 1.0)
            
        Returns:
            True if learned successfully
        """
        from runtime.education.semantic_representation import SemanticMeaning, EvidenceStatus
        
        # Create semantic meaning
        semantic_meaning = SemanticMeaning(
            word=word,
            lexical_meaning=meaning,
            semantic_field=semantic_field,
            confidence=confidence,
            evidence_status=EvidenceStatus.KNOWN,
        )
        
        # Store in semantic memory
        self.semantic_memory.store_understanding(
            word=word,
            language=language,
            meaning=semantic_meaning,
            context="taught_by_user"
        )
        
        # Remove from unknown list
        self.unknown_words = [
            c for c in self.unknown_words 
            if not (c.word == word and c.language == language)
        ]
        
        return True
    
    def get_unknown_words(
        self,
        language: Optional[str] = None,
        limit: int = 10
    ) -> List[VocabularyLearningCandidate]:
        """
        Get list of recently encountered unknown words.
        
        Args:
            language: Filter by language (None = all)
            limit: Maximum number to return
            
        Returns:
            List of unknown word candidates
        """
        candidates = self.unknown_words
        
        if language:
            candidates = [c for c in candidates if c.language == language]
        
        # Sort by most recent
        candidates = sorted(candidates, key=lambda c: c.timestamp, reverse=True)
        
        return candidates[:limit]
    
    def propose_learning(
        self,
        word: str,
        language: str,
        meaning: str,
        confidence: float = 0.7
    ) -> VocabularyLearningCandidate:
        """
        Propose a meaning for an unknown word (for confirmation).
        
        Returns candidate pending confirmation.
        """
        candidate = VocabularyLearningCandidate(
            word=word,
            language=language,
            proposed_meaning=meaning,
            confidence=confidence,
            timestamp=time.time(),
            source="inference"
        )
        
        self.pending_confirmation = candidate
        return candidate
    
    def confirm_learning(self, confirmed: bool) -> bool:
        """
        Confirm or reject pending learning.
        
        Returns True if learning was accepted and stored.
        """
        if not self.pending_confirmation:
            return False
        
        candidate = self.pending_confirmation
        
        if confirmed and candidate.proposed_meaning:
            # Learn the word
            success = self.teach_word(
                word=candidate.word,
                language=candidate.language,
                meaning=candidate.proposed_meaning,
                confidence=candidate.confidence
            )
            self.pending_confirmation = None
            return success
        else:
            # Rejected, keep in unknown list
            self.pending_confirmation = None
            return False
