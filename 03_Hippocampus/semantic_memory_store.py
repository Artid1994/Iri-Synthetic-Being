"""
Semantic Memory Integration
Stores semantic understanding in persistent memory.
"""
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict
import json

from runtime.education.semantic_representation import SemanticMeaning, EvidenceStatus


@dataclass
class SemanticMemoryEntry:
    """A semantic understanding stored in memory."""
    word: str
    language: str  # 'thai', 'english'
    lexical_meaning: str
    confidence: float
    evidence_status: str
    timestamp: float
    context_used: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SemanticMemoryStore:
    """
    Stores semantic understanding in persistent memory.
    
    Links semantic vocabulary to actual usage/understanding.
    """
    
    def __init__(self, memory_path: str = "03_Hippocampus/semantic_memory.json"):
        self.memory_path = Path(memory_path)
        self.entries: List[SemanticMemoryEntry] = []
        self._load()
    
    def _load(self):
        """Load existing semantic memory."""
        if self.memory_path.exists():
            data = json.loads(self.memory_path.read_text())
            self.entries = [
                SemanticMemoryEntry(**entry)
                for entry in data.get('entries', [])
            ]
    
    def _save(self):
        """Persist semantic memory."""
        data = {
            'entries': [e.to_dict() for e in self.entries],
            'count': len(self.entries)
        }
        self.memory_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    
    def store_understanding(
        self,
        word: str,
        language: str,
        meaning: SemanticMeaning,
        context: Optional[str] = None
    ):
        """Store semantic understanding of a word."""
        import time
        
        entry = SemanticMemoryEntry(
            word=word,
            language=language,
            lexical_meaning=meaning.lexical_meaning,
            confidence=meaning.confidence,
            evidence_status=meaning.evidence_status.value,
            timestamp=time.time(),
            context_used=context
        )
        
        self.entries.append(entry)
        self._save()
    
    def recall_understanding(
        self,
        word: str,
        language: str
    ) -> Optional[SemanticMemoryEntry]:
        """Recall semantic understanding of a word."""
        # Most recent understanding
        for entry in reversed(self.entries):
            if entry.word == word and entry.language == language:
                return entry
        return None
    
    def get_vocabulary_size(self, language: str) -> int:
        """Count unique words understood in a language."""
        words = set()
        for entry in self.entries:
            if entry.language == language:
                words.add(entry.word)
        return len(words)
