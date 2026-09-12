"""
Test Knowledge Ingestion Pipeline v1
Proves end-to-end: source → extract → learn → evidence → consolidate
"""
import pytest
import json
from pathlib import Path
from runtime.knowledge_ingestion import (
    KnowledgeSource,
    DocumentLoader,
    KnowledgeExtractor,
    Concept,
    Relation,
    Example,
    Provenance,
    KnowledgeIngestionPipeline,
    SourceType,
)
from runtime.memory import Memory
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel, ErrorType


class TestProvenance:
    """Test provenance tracking."""
    
    def test_provenance_creation(self):
        """Test provenance tracks source."""
        import time
        before = time.time()
        prov = Provenance(
            source_path="/test/source.json",
            source_type=SourceType.JSON,
            extraction_timestamp=time.time(),
            line_number=42,
        )
        after = time.time()
        
        assert prov.source_path == "/test/source.json"
        assert prov.source_type == SourceType.JSON
        assert before <= prov.extraction_timestamp <= after
        assert prov.line_number == 42
    
    def test_provenance_preserved_in_dict(self):
        """Test provenance serialization."""
        prov = Provenance(
            source_path="/test/file.txt",
            source_type=SourceType.TXT,
            extraction_timestamp=123.456,
        )
        
        data = prov.to_dict()
        assert data["source_path"] == "/test/file.txt"
        assert data["source_type"] == "txt"
        assert data["extraction_timestamp"] == 123.456


class TestConcept:
    """Test Concept structure."""
    
    def test_concept_creation(self):
        """Test concept with provenance."""
        prov = Provenance(
            source_path="/test.json",
            source_type=SourceType.JSON,
            extraction_timestamp=100.0,
        )
        
        concept = Concept(
            term="ไป",
            definition="go",
            language="thai",
            provenance=prov,
            confidence=1.0,
        )
        
        assert concept.term == "ไป"
        assert concept.definition == "go"
        assert concept.provenance.source_path == "/test.json"
    
    def test_concept_confidence_validation(self):
        """Test confidence bounds."""
        prov = Provenance("/test", SourceType.TXT, 100.0)
        
        with pytest.raises(ValueError, match="Confidence must be"):
            Concept("test", "def", "en", prov, confidence=1.5)


class TestDocumentLoader:
    """Test document loading."""
    
    def test_load_json(self, tmp_path):
        """Test loading JSON file."""
        test_file = tmp_path / "test.json"
        test_file.write_text('{"test": "data"}', encoding="utf-8")
        
        source = DocumentLoader.load(test_file)
        
        assert source.source_type == SourceType.JSON
        assert source.content == '{"test": "data"}'
        assert source.path == test_file
    
    def test_load_txt(self, tmp_path):
        """Test loading TXT file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content", encoding="utf-8")
        
        source = DocumentLoader.load(test_file)
        
        assert source.source_type == SourceType.TXT
        assert source.content == "test content"
    
    def test_load_nonexistent_file(self, tmp_path):
        """Test error on missing file."""
        missing = tmp_path / "missing.json"
        
        with pytest.raises(FileNotFoundError):
            DocumentLoader.load(missing)


class TestKnowledgeExtractor:
    """Test knowledge extraction."""
    
    def test_extract_from_json_vocabulary(self, tmp_path):
        """Test extracting concepts from JSON vocabulary."""
        test_file = tmp_path / "vocab.json"
        data = {
            "vocabulary": [
                {
                    "word": "ไป",
                    "meaning": "go",
                    "language": "thai",
                    "examples": ["ไป บ้าน"]
                }
            ]
        }
        test_file.write_text(json.dumps(data), encoding="utf-8")
        
        source = DocumentLoader.load(test_file)
        concepts, relations, examples = KnowledgeExtractor.extract(source)
        
        assert len(concepts) == 1
        assert concepts[0].term == "ไป"
        assert concepts[0].definition == "go"
        assert concepts[0].language == "thai"
        assert concepts[0].provenance is not None
        
        assert len(examples) == 1
        assert examples[0].concept_term == "ไป"
        assert examples[0].example_text == "ไป บ้าน"
    
    def test_extract_from_txt_simple(self, tmp_path):
        """Test extracting from plain text."""
        test_file = tmp_path / "notes.txt"
        test_file.write_text("word1: definition1\nword2 = definition2", encoding="utf-8")
        
        source = DocumentLoader.load(test_file)
        concepts, relations, examples = KnowledgeExtractor.extract(source)
        
        assert len(concepts) == 2
        assert concepts[0].term == "word1"
        assert concepts[0].definition == "definition1"
        assert concepts[0].provenance.line_number == 1
        
        assert concepts[1].term == "word2"
        assert concepts[1].definition == "definition2"
        assert concepts[1].provenance.line_number == 2
    
    def test_provenance_preserved_in_extraction(self, tmp_path):
        """CRITICAL: Test provenance not lost during extraction."""
        test_file = tmp_path / "test.json"
        data = {"concepts": [{"term": "test", "definition": "test def"}]}
        test_file.write_text(json.dumps(data), encoding="utf-8")
        
        source = DocumentLoader.load(test_file)
        concepts, _, _ = KnowledgeExtractor.extract(source)
        
        assert len(concepts) == 1
        assert concepts[0].provenance is not None
        assert concepts[0].provenance.source_path == str(test_file)
        assert concepts[0].provenance.source_type == SourceType.JSON


class TestKnowledgeIngestionPipeline:
    """Test complete ingestion pipeline."""
    
    def test_pipeline_ingest_json(self, tmp_path):
        """Test ingesting JSON source."""
        test_file = tmp_path / "knowledge.json"
        data = {
            "vocabulary": [
                {"word": "กิน", "meaning": "eat", "language": "thai"},
                {"word": "ดื่ม", "meaning": "drink", "language": "thai"},
            ]
        }
        test_file.write_text(json.dumps(data), encoding="utf-8")
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.ingest(test_file)
        
        assert result.success()
        assert result.concepts_extracted == 2
        assert result.provenance_preserved is True
        
        # Check candidate knowledge in working memory
        working = memory.working_memory()
        assert len(working) == 2
        assert "[CANDIDATE]" in working[0]
        assert "กิน" in working[0]
    
    def test_pipeline_extraction_not_learning(self, tmp_path):
        """CRITICAL: Test extraction does NOT equal learning."""
        test_file = tmp_path / "test.json"
        data = {"concepts": [{"term": "test", "definition": "test def"}]}
        test_file.write_text(json.dumps(data), encoding="utf-8")
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.ingest(test_file)
        
        # Extraction succeeded
        assert result.concepts_extracted == 1
        
        # But NOT learned yet
        assert result.concepts_learned == 0
        
        # And NOT consolidated yet
        assert result.concepts_consolidated == 0
        
        # Only in working memory as CANDIDATE
        working = memory.working_memory()
        assert "[CANDIDATE]" in working[0]
    
    def test_consolidate_requires_evidence(self, tmp_path):
        """CRITICAL: Test consolidation requires verified evidence."""
        test_file = tmp_path / "test.json"
        data = {"concepts": [{"term": "test", "definition": "def", "language": "en"}]}
        test_file.write_text(json.dumps(data), encoding="utf-8")
        
        source = DocumentLoader.load(test_file)
        concepts, _, _ = KnowledgeExtractor.extract(source)
        concept = concepts[0]
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Case 1: No evidence → rejected
        state_no_evidence = KnowledgeState("test")
        result = pipeline.consolidate_with_evidence(concept, state_no_evidence, evidence_verified=False)
        assert result is False
        
        # Case 2: Evidence but insufficient learning level → rejected
        state_learning = KnowledgeState("test")
        state_learning.level = KnowledgeLevel.LEARNING
        result = pipeline.consolidate_with_evidence(concept, state_learning, evidence_verified=True)
        assert result is False
        
        # Case 3: Evidence + sufficient learning level → accepted
        state_can_use = KnowledgeState("test")
        state_can_use.level = KnowledgeLevel.CAN_USE
        result = pipeline.consolidate_with_evidence(concept, state_can_use, evidence_verified=True)
        assert result is True
        
        # Verify consolidated to semantic memory
        assert memory.semantic_contains("test: def")
    
    def test_provenance_in_consolidated_memory(self, tmp_path):
        """CRITICAL: Test provenance preserved in consolidated memory."""
        test_file = tmp_path / "source.json"
        data = {"concepts": [{"term": "verified", "definition": "def", "language": "en"}]}
        test_file.write_text(json.dumps(data), encoding="utf-8")
        
        source = DocumentLoader.load(test_file)
        concepts, _, _ = KnowledgeExtractor.extract(source)
        concept = concepts[0]
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Consolidate with evidence
        state = KnowledgeState("verified")
        state.level = KnowledgeLevel.MASTERED
        pipeline.consolidate_with_evidence(concept, state, evidence_verified=True)
        
        # Check provenance in episodic memory
        # Provenance should be traceable
        assert len(memory.state.episodic) > 0
        # Should mention source file
        prov_found = any(str(test_file) in exp for exp in memory.state.episodic)
        assert prov_found, "Provenance not preserved in consolidated memory"
    
    def test_duplicate_source_handling(self, tmp_path):
        """Test ingesting same source twice doesn't create meaningless duplicates."""
        test_file = tmp_path / "dup.json"
        data = {"concepts": [{"term": "dup", "definition": "test"}]}
        test_file.write_text(json.dumps(data), encoding="utf-8")
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Ingest twice
        result1 = pipeline.ingest(test_file)
        result2 = pipeline.ingest(test_file)
        
        # Both succeed
        assert result1.success()
        assert result2.success()
        
        # Working memory has both (marked as candidates)
        # This is acceptable for v1 - deduplication can be added later
        working = memory.working_memory()
        assert len(working) == 2


class TestEndToEndScenarios:
    """Test complete scenarios."""
    
    def test_known_knowledge_path(self, tmp_path):
        """Test: known source → extract → learn → consolidate."""
        # Create source
        source_file = tmp_path / "known.json"
        data = {"vocabulary": [{"word": "water", "meaning": "น้ำ", "language": "english"}]}
        source_file.write_text(json.dumps(data), encoding="utf-8")
        
        # Ingest
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        result = pipeline.ingest(source_file)
        
        # Extraction phase complete
        assert result.concepts_extracted == 1
        assert result.provenance_preserved
        
        # Simulate learning (external Education System would do this)
        state = KnowledgeState("water")
        state.record_correct()
        state.record_correct()
        state.record_correct()
        state.level = KnowledgeLevel.CAN_USE
        
        # Consolidate with evidence
        source = DocumentLoader.load(source_file)
        concepts, _, _ = KnowledgeExtractor.extract(source)
        consolidated = pipeline.consolidate_with_evidence(concepts[0], state, evidence_verified=True)
        
        assert consolidated is True
    
    def test_ambiguous_knowledge_path(self, tmp_path):
        """Test: ambiguous knowledge remains marked as such."""
        # This would be handled by SemanticMeaning ambiguity_level
        # Pipeline extracts, Education System marks as AMBIGUOUS
        # v1: Just verify extraction doesn't force disambiguation
        
        source_file = tmp_path / "ambig.json"
        data = {"concepts": [{"term": "run", "definition": "multiple meanings"}]}
        source_file.write_text(json.dumps(data), encoding="utf-8")
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        result = pipeline.ingest(source_file)
        
        # Extracted as candidate
        assert result.concepts_extracted == 1
        
        # Would need Education System to determine ambiguity
        # v1: Pipeline doesn't force resolution
    
    def test_unknown_insufficient_evidence_path(self, tmp_path):
        """Test: insufficient evidence → not consolidated."""
        source_file = tmp_path / "unknown.json"
        data = {"concepts": [{"term": "obscure", "definition": "unclear"}]}
        source_file.write_text(json.dumps(data), encoding="utf-8")
        
        source = DocumentLoader.load(source_file)
        concepts, _, _ = KnowledgeExtractor.extract(source)
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Try to consolidate without evidence
        state = KnowledgeState("obscure")
        consolidated = pipeline.consolidate_with_evidence(concepts[0], state, evidence_verified=False)
        
        # Rejected
        assert consolidated is False
        
        # Not in semantic memory
        assert not memory.semantic_contains("obscure")
