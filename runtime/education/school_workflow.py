"""
Education System: School Workflow
Complete learning cycle with baseline, teaching, assessment, and persistence
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import time
import random


@dataclass
class TestItem:
    """A single test question/task."""
    item_id: str
    prompt: str
    correct_answer: str
    item_type: str  # "recall", "comprehension", "production", "transfer"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestResult:
    """Result of a single test item."""
    item_id: str
    prompt: str
    student_answer: str
    correct_answer: str
    is_correct: bool
    item_type: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class AssessmentRecord:
    """Complete assessment with all test results."""
    assessment_id: str
    assessment_type: str  # "baseline", "immediate_recall", "retention", "transfer"
    lesson_id: str
    timestamp: float
    items: List[TestResult]
    score: float  # 0.0 to 1.0
    total_items: int
    correct_items: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "assessment_id": self.assessment_id,
            "assessment_type": self.assessment_type,
            "lesson_id": self.lesson_id,
            "timestamp": self.timestamp,
            "items": [asdict(item) for item in self.items],
            "score": self.score,
            "total_items": self.total_items,
            "correct_items": self.correct_items,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AssessmentRecord:
        items = [TestResult(**item) for item in data["items"]]
        return cls(
            assessment_id=data["assessment_id"],
            assessment_type=data["assessment_type"],
            lesson_id=data["lesson_id"],
            timestamp=data["timestamp"],
            items=items,
            score=data["score"],
            total_items=data["total_items"],
            correct_items=data["correct_items"],
        )


@dataclass
class LearningGain:
    """Measured improvement from baseline to post-test."""
    lesson_id: str
    baseline_score: float
    posttest_score: float
    gain: float
    gain_percentage: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class MasteryDecision:
    """Decision based on evidence."""
    lesson_id: str
    decision: str  # "MASTERED", "REMEDIATE", "CONTINUE_PRACTICE"
    evidence: Dict[str, float]  # scores by assessment type
    timestamp: float
    next_action: str  # "ADVANCE", "RETEACH", "PRACTICE"


class SchoolWorkflow:
    """
    Complete learning workflow with guarantees:
    BASELINE → TEACH → PRACTICE → POST-TEST → LEARNING GAIN 
    → RETENTION → TRANSFER → MASTERED/REMEDIATE → PERSIST
    """
    
    MASTERY_THRESHOLD = 0.8
    RETENTION_THRESHOLD = 0.75
    TRANSFER_THRESHOLD = 0.70
    
    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = state_file or Path("03_Hippocampus/school_state.json")
        
        # Persistent records
        self.assessments: List[AssessmentRecord] = []
        self.learning_gains: List[LearningGain] = []
        self.mastery_decisions: List[MasteryDecision] = []
        self.lesson_status: Dict[str, str] = {}  # lesson_id -> status
        
        self.load_state()
    
    def create_baseline_test(
        self,
        lesson_id: str,
        test_items: List[TestItem],
    ) -> str:
        """
        Create baseline test before teaching.
        Returns: assessment_id
        """
        assessment_id = f"baseline_{lesson_id}_{int(time.time())}"
        return assessment_id
    
    def record_assessment(
        self,
        assessment_id: str,
        assessment_type: str,
        lesson_id: str,
        test_results: List[TestResult],
    ) -> AssessmentRecord:
        """
        Record complete assessment with all test results.
        Persists to state immediately.
        """
        correct = sum(1 for r in test_results if r.is_correct)
        total = len(test_results)
        score = correct / total if total > 0 else 0.0
        
        record = AssessmentRecord(
            assessment_id=assessment_id,
            assessment_type=assessment_type,
            lesson_id=lesson_id,
            timestamp=time.time(),
            items=test_results,
            score=score,
            total_items=total,
            correct_items=correct,
        )
        
        self.assessments.append(record)
        self.save_state()
        
        return record
    
    def calculate_learning_gain(
        self,
        lesson_id: str,
    ) -> Optional[LearningGain]:
        """
        Calculate learning gain from baseline to post-test.
        Returns None if baseline or post-test missing.
        """
        baseline = self._get_latest_assessment(lesson_id, "baseline")
        posttest = self._get_latest_assessment(lesson_id, "immediate_recall")
        
        if not baseline or not posttest:
            return None
        
        gain = posttest.score - baseline.score
        gain_pct = (gain / baseline.score * 100) if baseline.score > 0 else float('inf')
        
        learning_gain = LearningGain(
            lesson_id=lesson_id,
            baseline_score=baseline.score,
            posttest_score=posttest.score,
            gain=gain,
            gain_percentage=gain_pct,
        )
        
        self.learning_gains.append(learning_gain)
        self.save_state()
        
        return learning_gain
    
    def make_mastery_decision(
        self,
        lesson_id: str,
    ) -> MasteryDecision:
        """
        Make mastery decision based on all available evidence.
        
        Decision rules:
        - MASTERED: immediate_recall >= 80%, retention >= 75%, transfer >= 70%
        - REMEDIATE: any score < 50% OR 3+ failed attempts
        - CONTINUE_PRACTICE: between thresholds, needs more practice
        """
        evidence = {}
        
        # Collect all assessment scores
        immediate = self._get_latest_assessment(lesson_id, "immediate_recall")
        retention = self._get_latest_assessment(lesson_id, "retention")
        transfer = self._get_latest_assessment(lesson_id, "transfer")
        
        if immediate:
            evidence["immediate_recall"] = immediate.score
        if retention:
            evidence["retention"] = retention.score
        if transfer:
            evidence["transfer"] = transfer.score
        
        # Decision logic
        if not evidence:
            decision = "CONTINUE_PRACTICE"
            next_action = "PRACTICE"
        elif (
            evidence.get("immediate_recall", 0) >= self.MASTERY_THRESHOLD
            and evidence.get("retention", 0) >= self.RETENTION_THRESHOLD
            and evidence.get("transfer", 0) >= self.TRANSFER_THRESHOLD
        ):
            decision = "MASTERED"
            next_action = "ADVANCE"
        elif any(score < 0.5 for score in evidence.values()):
            decision = "REMEDIATE"
            next_action = "RETEACH"
        else:
            decision = "CONTINUE_PRACTICE"
            next_action = "PRACTICE"
        
        mastery_decision = MasteryDecision(
            lesson_id=lesson_id,
            decision=decision,
            evidence=evidence,
            timestamp=time.time(),
            next_action=next_action,
        )
        
        self.mastery_decisions.append(mastery_decision)
        self.lesson_status[lesson_id] = decision
        self.save_state()
        
        return mastery_decision
    
    def get_next_lesson_for_autonomous(
        self,
        curriculum,
    ) -> Optional[str]:
        """
        Get next lesson ID based on IRI's current learning state.
        Used by autonomous_loop.py to continue learning without human prompts.
        
        Returns:
            lesson_id or None if all lessons mastered
        """
        # Find lessons in progress or not started
        for lesson_id, lesson in curriculum.lessons.items():
            # Skip if already mastered in workflow
            if self.is_mastered(lesson_id):
                continue
            
            # Check prerequisites - must be mastered in workflow
            prereqs_met = all(
                self.is_mastered(prereq) for prereq in lesson.prerequisites
            )
            
            if not prereqs_met:
                continue
            
            # Return first unmastered lesson with met prerequisites
            return lesson_id
        
        return None
    
    def needs_remediation(self, lesson_id: str) -> bool:
        """Check if lesson needs remediation."""
        decision = self._get_latest_mastery_decision(lesson_id)
        if not decision:
            return False
        return decision.decision == "REMEDIATE"
    
    def is_mastered(self, lesson_id: str) -> bool:
        """Check if lesson is mastered."""
        # Check both lesson_status and latest mastery decision
        if self.lesson_status.get(lesson_id) == "MASTERED":
            return True
        
        decision = self._get_latest_mastery_decision(lesson_id)
        if not decision:
            return False
        return decision.decision == "MASTERED"
    
    def generate_transfer_items(
        self,
        original_items: List[TestItem],
        transform: str = "rephrase",
    ) -> List[TestItem]:
        """
        Generate novel transfer test items.
        Prevents answer leakage by using different phrasing/context.
        
        Args:
            original_items: Original test items
            transform: Type of transformation ("rephrase", "reverse", "apply")
        
        Returns:
            New test items for transfer assessment
        """
        transfer_items = []
        
        for item in original_items:
            if transform == "rephrase":
                # Different phrasing for same question
                new_prompt = self._rephrase_prompt(item.prompt)
            elif transform == "reverse":
                # Reverse question (e.g., "What makes sound X?" vs "What sound does Y make?")
                new_prompt = self._reverse_prompt(item.prompt, item.correct_answer)
            elif transform == "apply":
                # Application in new context
                new_prompt = self._apply_context(item.prompt, item.correct_answer)
            else:
                new_prompt = item.prompt
            
            transfer_item = TestItem(
                item_id=f"transfer_{item.item_id}_{int(time.time())}",
                prompt=new_prompt,
                correct_answer=item.correct_answer,
                item_type="transfer",
                metadata={"original_item": item.item_id, "transform": transform},
            )
            transfer_items.append(transfer_item)
        
        return transfer_items
    
    def _rephrase_prompt(self, prompt: str) -> str:
        """Rephrase a prompt to test transfer."""
        # Simple rephrasing patterns
        if "What sound does" in prompt and "make?" in prompt:
            # "What sound does ก make?" → "Which sound is produced by ก?"
            char = prompt.split("What sound does ")[1].split(" make?")[0]
            return f"Which sound is produced by {char}?"
        elif "What is the sound of" in prompt:
            char = prompt.split("What is the sound of ")[1].rstrip("?")
            return f"The character {char} produces which sound?"
        else:
            return prompt
    
    def _reverse_prompt(self, prompt: str, answer: str) -> str:
        """Create reverse question."""
        if "What sound does" in prompt:
            char = prompt.split("What sound does ")[1].split(" make?")[0]
            return f"Which character makes the sound {answer}?"
        return prompt
    
    def _apply_context(self, prompt: str, answer: str) -> str:
        """Apply to new context."""
        if "What sound does" in prompt:
            char = prompt.split("What sound does ")[1].split(" make?")[0]
            return f"If you see {char} at the start of a word, what sound do you pronounce?"
        return prompt
    
    def _get_latest_assessment(
        self,
        lesson_id: str,
        assessment_type: str,
    ) -> Optional[AssessmentRecord]:
        """Get most recent assessment of given type for lesson."""
        matching = [
            a for a in self.assessments
            if a.lesson_id == lesson_id and a.assessment_type == assessment_type
        ]
        if not matching:
            return None
        return max(matching, key=lambda a: a.timestamp)
    
    def _get_latest_mastery_decision(
        self,
        lesson_id: str,
    ) -> Optional[MasteryDecision]:
        """Get most recent mastery decision for lesson."""
        matching = [d for d in self.mastery_decisions if d.lesson_id == lesson_id]
        if not matching:
            return None
        return max(matching, key=lambda d: d.timestamp)
    
    def save_state(self) -> None:
        """Save all state to persistent file."""
        state = {
            "version": "1.0.0",
            "type": "school_workflow_state",
            "timestamp": time.time(),
            "assessments": [a.to_dict() for a in self.assessments],
            "learning_gains": [asdict(g) for g in self.learning_gains],
            "mastery_decisions": [asdict(d) for d in self.mastery_decisions],
            "lesson_status": self.lesson_status,
        }
        
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self) -> None:
        """Load state from persistent file."""
        if not self.state_file.exists():
            return
        
        try:
            with open(self.state_file) as f:
                state = json.load(f)
            
            self.assessments = [
                AssessmentRecord.from_dict(a) for a in state.get("assessments", [])
            ]
            self.learning_gains = [
                LearningGain(**g) for g in state.get("learning_gains", [])
            ]
            self.mastery_decisions = [
                MasteryDecision(**d) for d in state.get("mastery_decisions", [])
            ]
            self.lesson_status = state.get("lesson_status", {})
        except Exception:
            # If load fails, start fresh
            pass
