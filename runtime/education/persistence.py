"""
Education System: Persistence
Saves and loads curriculum state, mastery records, and learning history
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import asdict

from runtime.education.mastery_tracker import MasteryRecord
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel, ErrorType


class EducationPersistence:
    """Handles persistence of education system state."""
    
    def __init__(self, storage_dir: Optional[Path] = None) -> None:
        if storage_dir is None:
            storage_dir = Path.home() / "Projects" / "THE_TRANSCENDING_FORM" / "03_Hippocampus"
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.mastery_file = self.storage_dir / "education_mastery.json"
        self.knowledge_file = self.storage_dir / "education_knowledge.json"
        self.history_file = self.storage_dir / "education_history.json"
    
    def save_mastery_records(
        self,
        records: Dict[str, MasteryRecord],
    ) -> None:
        """Save mastery records to disk."""
        data = {
            lesson_id: {
                "lesson_id": record.lesson_id,
                "mastery_score": record.mastery_score,
                "attempts": record.attempts,
                "last_attempt": record.last_attempt,
                "mastered": record.mastered,
            }
            for lesson_id, record in records.items()
        }
        
        self.mastery_file.write_text(json.dumps(data, indent=2))
    
    def load_mastery_records(self) -> Dict[str, MasteryRecord]:
        """Load mastery records from disk."""
        if not self.mastery_file.exists():
            return {}
        
        data = json.loads(self.mastery_file.read_text())
        return {
            lesson_id: MasteryRecord(**record_data)
            for lesson_id, record_data in data.items()
        }
    
    def save_knowledge_states(
        self,
        states: Dict[str, KnowledgeState],
    ) -> None:
        """Save knowledge states to disk."""
        data = {
            concept_id: {
                "concept_id": state.concept_id,
                "level": state.level.value,
                "correct_count": state.correct_count,
                "incorrect_count": state.incorrect_count,
                "last_error_type": state.last_error_type.value if state.last_error_type else None,
                "last_practiced": state.last_practiced,
            }
            for concept_id, state in states.items()
        }
        
        self.knowledge_file.write_text(json.dumps(data, indent=2))
    
    def load_knowledge_states(self) -> Dict[str, KnowledgeState]:
        """Load knowledge states from disk."""
        if not self.knowledge_file.exists():
            return {}
        
        data = json.loads(self.knowledge_file.read_text())
        states = {}
        
        for concept_id, state_data in data.items():
            # Convert string back to enum
            state_data["level"] = KnowledgeLevel(state_data["level"])
            if state_data.get("last_error_type"):
                state_data["last_error_type"] = ErrorType(state_data["last_error_type"])
            
            states[concept_id] = KnowledgeState(**state_data)
        
        return states
    
    def append_learning_event(
        self,
        event: Dict,
    ) -> None:
        """Append a learning event to history."""
        history = []
        if self.history_file.exists():
            history = json.loads(self.history_file.read_text())
        
        history.append(event)
        
        # Keep last 1000 events
        if len(history) > 1000:
            history = history[-1000:]
        
        self.history_file.write_text(json.dumps(history, indent=2))
    
    def load_learning_history(
        self,
        limit: Optional[int] = None,
    ) -> List[Dict]:
        """Load learning history."""
        if not self.history_file.exists():
            return []
        
        history = json.loads(self.history_file.read_text())
        
        if limit:
            return history[-limit:]
        
        return history
