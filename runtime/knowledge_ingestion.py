"""
Knowledge Ingestion Pipeline v1
Minimal infrastructure for ingesting Thai knowledge sources into Education System.

CRITICAL RULES:
- Extraction ≠ Understanding
- Evidence required from actual learning/practice
- Provenance must be preserved at all levels
- No LLM dependency
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path
from enum import Enum
import json


class SourceType(Enum):
    """Type of knowledge source."""
    TXT = "txt"
    JSON = "json"
    MARKDOWN = "markdown"


@dataclass
class Provenance:
    """Tracks where knowledge came from."""
    source_path: str
    source_type: SourceType
    extraction_timestamp: float
    line_number: Optional[int] = None
    section: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_path": self.source_path,
            "source_type": self.source_type.value,
            "extraction_timestamp": self.extraction_timestamp,
            "line_number": self.line_number,
            "section": self.section,
        }


@dataclass
class Concept:
    """
    Extracted concept (candidate knowledge, NOT learned yet).
    
    Represents potential knowledge that needs verification through Education System.
    """
    term: str
    definition: str
    language: str  # "thai", "english", etc.
    provenance: Provenance
    confidence: float = 0.0  # Extraction confidence, NOT learning confidence
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("Confidence must be 0.0-1.0")


@dataclass
class Relation:
    """Extracted relationship between concepts."""
    source_term: str
    relation_type: str  # "is_a", "part_of", "related_to", etc.
    target_term: str
    provenance: Provenance
    confidence: float = 0.0


@dataclass
class Example:
    """Extracted usage example."""
    concept_term: str
    example_text: str
    translation: Optional[str] = None
    provenance: Optional[Provenance] = None


@dataclass
class KnowledgeSource:
    """Represents a source document."""
    path: Path
    source_type: SourceType
    content: str
    loaded_timestamp: float
    
    def get_provenance(self, line_num: Optional[int] = None, section: Optional[str] = None) -> Provenance:
        """Create provenance for extracted knowledge."""
        import time
        return Provenance(
            source_path=str(self.path),
            source_type=self.source_type,
            extraction_timestamp=time.time(),
            line_number=line_num,
            section=section,
        )


class DocumentLoader:
    """Loads documents from various formats."""
    
    @staticmethod
    def load(path: Path) -> KnowledgeSource:
        """Load document and determine type."""
        import time
        
        if not path.exists():
            raise FileNotFoundError(f"Source not found: {path}")
        
        suffix = path.suffix.lower()
        if suffix == ".txt":
            source_type = SourceType.TXT
        elif suffix == ".json":
            source_type = SourceType.JSON
        elif suffix in [".md", ".markdown"]:
            source_type = SourceType.MARKDOWN
        else:
            raise ValueError(f"Unsupported file type: {suffix}")
        
        content = path.read_text(encoding="utf-8")
        
        return KnowledgeSource(
            path=path,
            source_type=source_type,
            content=content,
            loaded_timestamp=time.time(),
        )


class KnowledgeExtractor:
    """
    Extracts structured knowledge from source.
    
    IMPORTANT: Extraction creates CANDIDATE knowledge, not learned knowledge.
    Must go through Education System for actual learning.
    """
    
    @staticmethod
    def extract_from_json(source: KnowledgeSource) -> tuple[List[Concept], List[Relation], List[Example]]:
        """Extract from JSON format."""
        data = json.loads(source.content)
        
        concepts = []
        relations = []
        examples = []
        
        # Handle vocabulary-like JSON
        if "vocabulary" in data or "concepts" in data:
            items = data.get("vocabulary", data.get("concepts", []))
            for item in items:
                if "term" in item or "word" in item:
                    term = item.get("term", item.get("word"))
                    definition = item.get("definition", item.get("meaning", ""))
                    
                    concept = Concept(
                        term=term,
                        definition=definition,
                        language=item.get("language", "unknown"),
                        provenance=source.get_provenance(),
                        confidence=1.0,  # Source confidence, not learning confidence
                        metadata=item,
                    )
                    concepts.append(concept)
                    
                    # Extract examples if present
                    if "examples" in item:
                        for ex in item["examples"]:
                            examples.append(Example(
                                concept_term=term,
                                example_text=ex,
                                provenance=source.get_provenance(),
                            ))
        
        return concepts, relations, examples
    
    @staticmethod
    def extract_from_txt(source: KnowledgeSource) -> tuple[List[Concept], List[Relation], List[Example]]:
        """Extract from plain text (simple pattern matching)."""
        concepts = []
        lines = source.content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Simple pattern: "term: definition" or "term = definition"
            if ':' in line or '=' in line:
                separator = ':' if ':' in line else '='
                parts = line.split(separator, 1)
                if len(parts) == 2:
                    term = parts[0].strip()
                    definition = parts[1].strip()
                    
                    concept = Concept(
                        term=term,
                        definition=definition,
                        language="unknown",  # Cannot determine from plain text
                        provenance=source.get_provenance(line_num=i+1),
                        confidence=0.7,  # Lower confidence for unstructured source
                    )
                    concepts.append(concept)
        
        return concepts, [], []  # No relations/examples from simple TXT
    
    @staticmethod
    def extract(source: KnowledgeSource) -> tuple[List[Concept], List[Relation], List[Example]]:
        """Extract based on source type."""
        if source.source_type == SourceType.JSON:
            return KnowledgeExtractor.extract_from_json(source)
        elif source.source_type == SourceType.TXT:
            return KnowledgeExtractor.extract_from_txt(source)
        elif source.source_type == SourceType.MARKDOWN:
            # For v1, treat markdown like txt
            return KnowledgeExtractor.extract_from_txt(source)
        else:
            return [], [], []


@dataclass
class IngestionResult:
    """Result of knowledge ingestion."""
    concepts_extracted: int
    relations_extracted: int
    examples_extracted: int
    concepts_learned: int  # Actually went through Education System
    concepts_consolidated: int  # Reached Memory with evidence
    provenance_preserved: bool
    
    def success(self) -> bool:
        """Check if ingestion succeeded."""
        return self.concepts_extracted > 0 and self.provenance_preserved


class KnowledgeIngestionPipeline:
    """
    Orchestrates knowledge ingestion.
    
    Pipeline: SOURCE → EXTRACT → CANDIDATE → (Education System) → EVIDENCE → CONSOLIDATE
    """
    
    def __init__(self, memory, knowledge_state_tracker: Optional[Dict] = None):
        """
        Args:
            memory: Memory instance
            knowledge_state_tracker: Dict[concept_id, KnowledgeState] for tracking learning
        """
        self.memory = memory
        self.knowledge_state_tracker = knowledge_state_tracker or {}
    
    def ingest(self, source_path: Path) -> IngestionResult:
        """
        Ingest knowledge from source.
        
        Returns metrics, NOT learned knowledge.
        Caller must integrate with Education System for actual learning.
        """
        # Step 1: Load source
        source = DocumentLoader.load(source_path)
        
        # Step 2: Extract candidate knowledge
        concepts, relations, examples = KnowledgeExtractor.extract(source)
        
        # Step 3: Store as CANDIDATE knowledge (not learned yet)
        # For v1, store in Memory as working knowledge with provenance
        for concept in concepts:
            # Add to working memory with provenance
            entry = f"[CANDIDATE] {concept.term}: {concept.definition} (source: {concept.provenance.source_path})"
            self.memory.add_working(entry)
        
        # Provenance preservation check
        provenance_preserved = all(c.provenance is not None for c in concepts)
        
        return IngestionResult(
            concepts_extracted=len(concepts),
            relations_extracted=len(relations),
            examples_extracted=len(examples),
            concepts_learned=0,  # None learned yet - needs Education System
            concepts_consolidated=0,  # None consolidated yet - needs evidence
            provenance_preserved=provenance_preserved,
        )
    
    def consolidate_with_evidence(
        self,
        concept: Concept,
        knowledge_state,
        evidence_verified: bool,
    ) -> bool:
        """
        Consolidate concept to Memory ONLY if evidence verified.
        
        This is called AFTER Education System provides evidence.
        Extraction alone is NOT sufficient.
        """
        if not evidence_verified:
            return False
        
        # Check knowledge state level
        from runtime.education.knowledge_state import KnowledgeLevel
        if knowledge_state.level not in [KnowledgeLevel.CAN_USE, KnowledgeLevel.MASTERED]:
            return False  # Insufficient learning level
        
        # Consolidate to semantic memory with full provenance
        entry = f"{concept.term}: {concept.definition}"
        self.memory.add_semantic(entry)
        
        # Add provenance as experience
        prov_entry = f"Learned '{concept.term}' from {concept.provenance.source_path}"
        self.memory.add_experience(prov_entry)
        
        return True
