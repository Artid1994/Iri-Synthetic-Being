#!/usr/bin/env python3
"""
Regression tests for IRI chat defects discovered in interactive testing.

Tests semantic learning, question answering, control command filtering,
and voice serialization.
"""

import json
import os
import pytest
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "04_Cerebellum"))

from scripts.iri_chat import IriChat, Intent
from voice_serializer import VoiceSerializer


class TestSemanticLearning:
    """Test semantic knowledge extraction and persistence."""
    
    def setup_method(self):
        """Create test instance with mocked dependencies."""
        with patch('scripts.iri_chat.importlib.import_module'), \
             patch('scripts.iri_chat.InnerMonologue'), \
             patch('scripts.iri_chat.ParallelProcessor'):
            self.chat = IriChat()
            self.chat.voice_synthesizer = Mock()
            
    def test_extract_semantic_knowledge_from_teaching(self):
        """Test extraction of semantic knowledge from teaching statement."""
        teaching = """ชื่อของสิ่งนี้คือ ลูม่า
ลูม่าคือสัตว์สมมติที่ชอบนอนบนต้นไม้ตอนกลางวัน
และออกหาอาหารในเวลากลางคืน"""
        
        knowledge = self.chat._extract_semantic_knowledge(teaching)
        
        assert knowledge is not None
        assert 'entity' in knowledge
        assert knowledge['entity'] == 'ลูม่า'
        assert 'attributes' in knowledge
        assert len(knowledge['attributes']) > 0
        
        # Check extracted attributes
        attrs_text = ' '.join(knowledge['attributes'])
        assert 'สัตว์สมมติ' in attrs_text
        assert 'นอนบนต้นไม้' in attrs_text or 'ต้นไม้' in attrs_text
        
    def test_store_semantic_knowledge(self):
        """Test storing semantic knowledge to Hippocampus."""
        knowledge = {
            'entity': 'เซร่า',
            'attributes': ['สัตว์สมมติ', 'อาศัยอยู่ในถ้ำ', 'ออกหากินตอนเช้า'],
            'source': 'user_teaching',
            'timestamp': '2026-09-15T02:00:00'
        }
        
        # Store should not raise
        self.chat._store_semantic_knowledge(knowledge)
        
        # Verify file was created
        knowledge_file = self.chat.project_root / "03_Hippocampus" / "semantic_knowledge.json"
        assert knowledge_file.exists()
        
        # Verify content
        with open(knowledge_file, 'r', encoding='utf-8') as f:
            stored = json.load(f)
        
        assert len(stored) > 0
        # Find our entity
        found = False
        for item in stored:
            if item.get('entity') == 'เซร่า':
                found = True
                assert 'สัตว์สมมติ' in item['attributes']
                break
        assert found, "Stored knowledge not found in semantic_knowledge.json"


class TestQuestionAnswering:
    """Test answering from semantic knowledge."""
    
    def setup_method(self):
        """Create test instance with semantic knowledge."""
        with patch('scripts.iri_chat.importlib.import_module'), \
             patch('scripts.iri_chat.InnerMonologue'), \
             patch('scripts.iri_chat.ParallelProcessor'):
            self.chat = IriChat()
            self.chat.voice_synthesizer = Mock()
            
        # Inject test knowledge
        test_knowledge = [
            {
                'entity': 'ลูม่า',
                'attributes': ['สัตว์สมมติ', 'นอนบนต้นไม้ตอนกลางวัน', 'ออกหาอาหารในเวลากลางคืน'],
                'source': 'user_teaching',
                'timestamp': '2026-09-15T01:00:00'
            }
        ]
        
        knowledge_file = self.chat.project_root / "03_Hippocampus" / "semantic_knowledge.json"
        knowledge_file.parent.mkdir(parents=True, exist_ok=True)
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(test_knowledge, f, ensure_ascii=False, indent=2)
    
    def test_answer_what_is_question(self):
        """Test answering 'what is X' from semantic knowledge."""
        question = "ลูม่าคืออะไร"
        intent = Intent(type='question', confidence=0.9, entities=['ลูม่า'])
        
        response = self.chat.generate_response(question, intent)
        
        # Should answer from knowledge, not dump transcript
        assert 'ลูม่า' in response
        assert 'สัตว์สมมติ' in response
        assert '[Artid]' not in response  # Not a transcript dump
        assert 'conversation_' not in response  # Not a file path
        
    def test_answer_attribute_question(self):
        """Test answering attribute question from semantic knowledge."""
        question = "ลูม่าชอบทำอะไรตอนกลางวัน"
        intent = Intent(type='question', confidence=0.9, entities=['ลูม่า', 'กลางวัน'])
        
        response = self.chat.generate_response(question, intent)
        
        assert 'นอน' in response or 'ต้นไม้' in response
        assert '[Artid]' not in response  # Not a transcript
        
    def test_answer_entity_recall_question(self):
        """Test recalling which entity was taught."""
        question = "สัตว์ที่ฉันเพิ่งสอนเธอชื่ออะไร"
        intent = Intent(type='question', confidence=0.9, entities=['สัตว์', 'สอน'])
        
        response = self.chat.generate_response(question, intent)
        
        assert 'ลูม่า' in response
        assert '[Artid]' not in response


class TestControlCommandFiltering:
    """Test that control commands don't become ordinary memory."""
    
    def setup_method(self):
        """Create test instance."""
        with patch('scripts.iri_chat.importlib.import_module'), \
             patch('scripts.iri_chat.InnerMonologue'), \
             patch('scripts.iri_chat.ParallelProcessor'):
            self.chat = IriChat()
            self.chat.voice_synthesizer = Mock()
    
    def test_exit_not_saved_to_episodic_memory(self):
        """Test that 'exit' command is not saved to conversation memory."""
        intent = Intent(type='exit', confidence=1.0, entities=['exit'])
        response = self.chat.generate_response("exit", intent)
        
        # Save should be filtered
        self.chat.save_conversation_turn("exit", response, intent.type)
        
        # Check conversation log
        conv_dir = self.chat.project_root / "03_Hippocampus" / "conversations"
        if conv_dir.exists():
            for conv_file in conv_dir.glob("conversation_*.json"):
                with open(conv_file, 'r', encoding='utf-8') as f:
                    conv = json.load(f)
                    for turn in conv:
                        assert turn['user'].lower() != 'exit', "Control command 'exit' was saved to memory"
    
    def test_quit_not_saved_to_episodic_memory(self):
        """Test that 'quit' command is not saved to conversation memory."""
        intent = Intent(type='exit', confidence=1.0, entities=['quit'])
        response = self.chat.generate_response("quit", intent)
        
        self.chat.save_conversation_turn("quit", response, intent.type)
        
        # Verify not in memory
        conv_dir = self.chat.project_root / "03_Hippocampus" / "conversations"
        if conv_dir.exists():
            for conv_file in conv_dir.glob("conversation_*.json"):
                with open(conv_file, 'r', encoding='utf-8') as f:
                    conv = json.load(f)
                    for turn in conv:
                        assert turn['user'].lower() != 'quit'


class TestVoiceSerialization:
    """Test voice output serialization to prevent overlapping playback."""
    
    def test_voice_serializer_cancels_previous(self):
        """Test that new playback cancels previous playback."""
        serializer = VoiceSerializer()
        
        # Mock process that simulates running playback
        mock_proc1 = Mock()
        mock_proc1.poll.return_value = None  # Still running
        mock_proc1.wait.return_value = None  # Simulate blocking wait
        
        # Mock process 2
        mock_proc2 = Mock()
        mock_proc2.poll.return_value = None
        mock_proc2.wait.return_value = None
        
        # Start first playback
        with patch('voice_serializer.subprocess.Popen', return_value=mock_proc1):
            serializer.play('/tmp/test1.mp3', os.environ.copy())
            time.sleep(0.2)  # Give worker time to start processing
        
        # Start second playback (should cancel first)
        with patch('voice_serializer.subprocess.Popen', return_value=mock_proc2):
            serializer.play('/tmp/test2.mp3', os.environ.copy())
            time.sleep(0.2)  # Give worker time to cancel and start new
        
        # First process should have been terminated
        mock_proc1.terminate.assert_called()
        
        serializer.shutdown()
    
    def test_voice_serializer_shutdown_kills_active(self):
        """Test that shutdown kills any active playback."""
        serializer = VoiceSerializer()
        
        mock_proc = Mock()
        mock_proc.poll.return_value = None  # Still running
        mock_proc.wait.return_value = None  # Simulate blocking
        
        with patch('voice_serializer.subprocess.Popen', return_value=mock_proc):
            serializer.play('/tmp/test.mp3', os.environ.copy())
            time.sleep(0.2)  # Give worker time to start
        
        # Shutdown should kill process
        serializer.shutdown()
        mock_proc.terminate.assert_called()
    
    def test_voice_serializer_cleanup_callback(self):
        """Test that cleanup callback is called after playback completes."""
        serializer = VoiceSerializer()
        
        cleanup_called = []
        def cleanup(path):
            cleanup_called.append(path)
        
        # Mock process that completes immediately
        mock_proc = Mock()
        mock_proc.poll.return_value = 0  # Completed
        mock_proc.wait.return_value = 0
        
        with patch('subprocess.Popen', return_value=mock_proc):
            serializer.play('/tmp/test.mp3', os.environ.copy(), cleanup)
            time.sleep(0.2)  # Wait for thread to process
        
        # Cleanup should have been called
        assert len(cleanup_called) > 0
        assert cleanup_called[0] == '/tmp/test.mp3'
        
        serializer.shutdown()


class TestIntentClassification:
    """Test intent classification for teaching vs questions."""
    
    def setup_method(self):
        """Create test instance."""
        with patch('scripts.iri_chat.importlib.import_module'), \
             patch('scripts.iri_chat.InnerMonologue'), \
             patch('scripts.iri_chat.ParallelProcessor'):
            self.chat = IriChat()
            self.chat.voice_synthesizer = Mock()
    
    def test_classify_teaching_statement(self):
        """Test classifying a teaching statement."""
        teaching = "ชื่อของสิ่งนี้คือ ลูม่า\nลูม่าคือสัตว์สมมติ"
        intent = self.chat.classify_input(teaching)
        
        assert intent.type == 'statement'
        assert intent.confidence > 0.5
    
    def test_classify_what_is_question(self):
        """Test classifying a 'what is' question."""
        question = "ลูม่าคืออะไร"
        intent = self.chat.classify_input(question)
        
        assert intent.type == 'question'
        assert intent.confidence > 0.5
    
    def test_classify_exit_command(self):
        """Test classifying exit command."""
        for cmd in ['exit', 'quit', 'bye', 'ออก']:
            intent = self.chat.classify_input(cmd)
            assert intent.type == 'exit', f"Failed to classify '{cmd}' as exit"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
