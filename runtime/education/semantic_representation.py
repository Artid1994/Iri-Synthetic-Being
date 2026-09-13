"""
Semantic Representation Core
Data structures for representing meaning beyond word-level recognition.

This is language-general: supports Thai now, English future.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class EvidenceStatus(Enum):
    """Status of evidence for a semantic claim."""
    KNOWN = "known"                    # Verified from authoritative source
    AMBIGUOUS = "ambiguous"            # Multiple interpretations possible
    UNKNOWN = "unknown"                # No evidence available
    NOT_APPLICABLE = "not_applicable"  # Category doesn't apply


class ContextType(Enum):
    """Type of context for meaning interpretation."""
    LITERAL = "literal"          # Direct dictionary meaning
    PRAGMATIC = "pragmatic"      # Context-dependent use
    IDIOMATIC = "idiomatic"      # Fixed expression
    CULTURAL = "cultural"        # Culture-specific meaning


class AmbiguityType(Enum):
    """Type of ambiguity in interpretation."""
    LEXICAL = "lexical"          # Word has multiple meanings
    STRUCTURAL = "structural"    # Sentence structure ambiguous
    PRAGMATIC = "pragmatic"      # Use/function ambiguous
    REFERENCE = "reference"      # Unclear what is referred to


class EvidenceType(Enum):
    """Type of evidence for understanding."""
    TRANSLATION = "translation"              # Translation/recall only (insufficient for semantic mastery)
    EXPLANATION = "explanation"              # Can explain structure/meaning
    PARAPHRASE = "paraphrase"               # Can express in different words
    APPLICATION = "application"              # Can apply pattern to new case
    INFERENCE = "inference"                  # Can draw valid conclusions
    CONTEXTUAL_INTERPRETATION = "contextual" # Can interpret in context
    PATTERN_EXTRACTION = "pattern"           # Can identify pattern
    TRANSFER = "transfer"                    # Can transfer to novel example


@dataclass
class ContextualMeaning:
    """
    One possible meaning in a specific context.
    
    Separates lexical meaning from contextual interpretation.
    """
    context_type: ContextType
    meaning: str
    required_context: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    confidence: float = 0.0  # 0.0-1.0, confidence in THIS interpretation
    data_status: EvidenceStatus = EvidenceStatus.KNOWN
    
    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be 0.0-1.0, got {self.confidence}")
        
        if not self.meaning.strip():
            raise ValueError("Meaning cannot be empty")


@dataclass
class SemanticMeaning:
    """
    Semantic representation of a word/phrase.
    
    Supports multiple interpretations, context-dependence, ambiguity.
    Language-general design.
    """
    word: str  # Thai, English, or other language
    lexical_meaning: str  # Core dictionary meaning
    semantic_field: Optional[str] = None  # MOTION, QUALITY, STATE, etc.
    contextual_meanings: List[ContextualMeaning] = field(default_factory=list)
    ambiguity_level: str = "UNAMBIGUOUS"  # UNAMBIGUOUS, MILDLY_AMBIGUOUS, HIGHLY_AMBIGUOUS
    evidence_status: EvidenceStatus = EvidenceStatus.KNOWN
    confidence: float = 0.0  # Overall confidence in semantic representation
    
    def __post_init__(self):
        if not self.word.strip():
            raise ValueError("Word cannot be empty")
        
        if not self.lexical_meaning.strip():
            raise ValueError("Lexical meaning cannot be empty")
        
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be 0.0-1.0, got {self.confidence}")
        
        valid_ambiguity = ["UNAMBIGUOUS", "MILDLY_AMBIGUOUS", "HIGHLY_AMBIGUOUS"]
        if self.ambiguity_level not in valid_ambiguity:
            raise ValueError(f"Ambiguity level must be one of {valid_ambiguity}")
    
    def get_meaning_in_context(self, context_type: ContextType) -> Optional[ContextualMeaning]:
        """Get meaning for specific context type."""
        for cm in self.contextual_meanings:
            if cm.context_type == context_type:
                return cm
        return None
    
    def is_ambiguous(self) -> bool:
        """Check if word has ambiguous meanings."""
        return self.ambiguity_level in ["MILDLY_AMBIGUOUS", "HIGHLY_AMBIGUOUS"]


@dataclass
class AmbiguityPoint:
    """
    Represents one point of ambiguity in understanding.
    """
    location: str  # "word:2" or "sentence:overall"
    ambiguity_type: AmbiguityType
    possible_interpretations: List[str]
    resolution_required: bool = True
    resolution_strategy: Optional[str] = None  # CONTEXT, DISAMBIGUATION, ACCEPT_AMBIGUITY
    
    def __post_init__(self):
        if not self.possible_interpretations:
            raise ValueError("Must have at least one possible interpretation")
        
        if len(self.possible_interpretations) < 2:
            raise ValueError("Ambiguity requires at least 2 interpretations")


@dataclass
class SentenceSemantics:
    """
    Semantic representation of a complete sentence.
    
    Compositional + pragmatic meaning.
    """
    sentence: str  # Original sentence (Thai, English, etc.)
    word_meanings: List[SemanticMeaning] = field(default_factory=list)
    compositional_meaning: Optional[str] = None  # Meaning from word combination
    pragmatic_meaning: Optional[str] = None  # Context-dependent interpretation
    ambiguity_points: List[AmbiguityPoint] = field(default_factory=list)
    confidence: float = 0.0
    evidence: List[str] = field(default_factory=list)  # Why this interpretation
    
    def __post_init__(self):
        if not self.sentence.strip():
            raise ValueError("Sentence cannot be empty")
        
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be 0.0-1.0, got {self.confidence}")
    
    def has_ambiguity(self) -> bool:
        """Check if sentence has unresolved ambiguity."""
        return len(self.ambiguity_points) > 0
    
    def get_final_meaning(self) -> str:
        """Get final interpreted meaning (pragmatic if available, else compositional)."""
        if self.pragmatic_meaning:
            return self.pragmatic_meaning
        return self.compositional_meaning or ""


@dataclass
class UnderstandingEvidence:
    """
    Evidence that understanding occurred (not just translation/memorization).
    
    Understanding requires demonstration, not just recall.
    """
    evidence_type: EvidenceType
    language_input: str  # Thai, English, etc.
    learner_output: str  # What learner produced
    expected_pattern: str  # What evidence should look like
    verified: bool = False
    confidence: float = 0.0
    explanation: Optional[str] = None  # Why this counts as evidence
    
    def __post_init__(self):
        if not self.language_input.strip():
            raise ValueError("Language input cannot be empty")
        
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be 0.0-1.0, got {self.confidence}")


class SemanticVerifier:
    """
    Validates semantic representations and evidence.
    
    Enforces: KNOWN/AMBIGUOUS/UNKNOWN discipline.
    """
    
    @staticmethod
    def validate_semantic_meaning(sem: SemanticMeaning) -> tuple[bool, List[str]]:
        """
        Validate SemanticMeaning structure.
        
        Returns: (valid, error_messages)
        """
        errors = []
        
        # Basic structure
        if not sem.word or not sem.lexical_meaning:
            errors.append("Word and lexical_meaning required")
        
        # Contextual meanings must be valid
        for cm in sem.contextual_meanings:
            if cm.confidence > sem.confidence:
                errors.append(f"Contextual confidence ({cm.confidence}) cannot exceed overall ({sem.confidence})")
        
        # Evidence status consistency
        if sem.evidence_status == EvidenceStatus.UNKNOWN and sem.confidence > 0.3:
            errors.append("UNKNOWN status should have low confidence")
        
        if sem.evidence_status == EvidenceStatus.KNOWN and sem.confidence < 0.7:
            errors.append("KNOWN status should have high confidence")
        
        return (len(errors) == 0, errors)
    
    @staticmethod
    def validate_understanding_evidence(evidence: UnderstandingEvidence) -> tuple[bool, List[str]]:
        """
        Validate understanding evidence.
        
        Ensures evidence actually demonstrates understanding.
        """
        errors = []
        
        # Must have learner output
        if not evidence.learner_output.strip():
            errors.append("Learner must produce output")
        
        # Evidence type requirements
        if evidence.evidence_type == EvidenceType.EXPLANATION:
            if len(evidence.learner_output) < 10:
                errors.append("Explanation too short to demonstrate understanding")
            # CRITICAL: Explanation must not just repeat input
            if evidence.language_input.strip().lower() == evidence.learner_output.strip().lower():
                errors.append("Explanation must not just repeat input")
        
        if evidence.evidence_type == EvidenceType.APPLICATION:
            if evidence.language_input == evidence.learner_output:
                errors.append("Application must produce new example, not repeat input")
        
        if evidence.evidence_type == EvidenceType.TRANSFER:
            if evidence.language_input in evidence.learner_output:
                errors.append("Transfer must use new material, not memorized input")
        
        # Verified evidence should have explanation
        if evidence.verified and not evidence.explanation:
            errors.append("Verified evidence should explain why it's valid")
        
        return (len(errors) == 0, errors)
    
    @staticmethod
    def check_ambiguity_resolution(ambiguity: AmbiguityPoint, context: Dict[str, str]) -> Optional[str]:
        """
        Attempt to resolve ambiguity using context.
        
        Returns: selected interpretation or None if cannot resolve
        """
        if not ambiguity.resolution_required:
            return None
        
        if ambiguity.resolution_strategy == "ACCEPT_AMBIGUITY":
            return None
        
        if ambiguity.resolution_strategy == "CONTEXT":
            # Check if context provides clues
            # This is a placeholder - real implementation would need actual resolution logic
            return None  # Cannot resolve without sufficient context
        
        # Default: cannot resolve
        return None
