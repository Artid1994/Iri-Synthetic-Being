"""
Tests for SchoolWorkflow: Complete learning cycle with all guarantees
"""
import unittest
from pathlib import Path
import tempfile
import json

from runtime.education.school_workflow import (
    SchoolWorkflow,
    TestItem,
    TestResult,
    AssessmentRecord,
    LearningGain,
    MasteryDecision,
)
from runtime.education.subject import SubjectType


class TestSchoolWorkflow(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = Path(self.temp_dir) / "test_school_state.json"
        self.workflow = SchoolWorkflow(state_file=self.state_file)
    
    def test_baseline_persistence(self):
        """GUARANTEE: Baseline test results persist."""
        lesson_id = "thai_consonants_1"
        
        # Create baseline test
        baseline_results = [
            TestResult(
                item_id="baseline_1",
                prompt="What sound does ก make?",
                student_answer="",
                correct_answer="k",
                is_correct=False,
                item_type="recall",
            ),
            TestResult(
                item_id="baseline_2",
                prompt="What sound does ข make?",
                student_answer="kh",
                correct_answer="kh",
                is_correct=True,
                item_type="recall",
            ),
        ]
        
        # Record baseline
        record = self.workflow.record_assessment(
            assessment_id="baseline_test_1",
            assessment_type="baseline",
            lesson_id=lesson_id,
            test_results=baseline_results,
        )
        
        # Verify persisted
        self.assertEqual(record.score, 0.5)
        self.assertEqual(record.correct_items, 1)
        self.assertEqual(record.total_items, 2)
        
        # Verify file exists
        self.assertTrue(self.state_file.exists())
        
        # Reload and verify
        workflow2 = SchoolWorkflow(state_file=self.state_file)
        self.assertEqual(len(workflow2.assessments), 1)
        self.assertEqual(workflow2.assessments[0].assessment_type, "baseline")
        self.assertEqual(workflow2.assessments[0].score, 0.5)
    
    def test_posttest_persistence(self):
        """GUARANTEE: Post-test results persist."""
        lesson_id = "thai_consonants_1"
        
        posttest_results = [
            TestResult(
                item_id="post_1",
                prompt="What sound does ก make?",
                student_answer="k",
                correct_answer="k",
                is_correct=True,
                item_type="recall",
            ),
            TestResult(
                item_id="post_2",
                prompt="What sound does ข make?",
                student_answer="kh",
                correct_answer="kh",
                is_correct=True,
                item_type="recall",
            ),
        ]
        
        record = self.workflow.record_assessment(
            assessment_id="posttest_1",
            assessment_type="immediate_recall",
            lesson_id=lesson_id,
            test_results=posttest_results,
        )
        
        self.assertEqual(record.score, 1.0)
        self.assertEqual(len(self.workflow.assessments), 1)
    
    def test_learning_gain_calculation(self):
        """GUARANTEE: Learning gain calculated from baseline and post-test."""
        lesson_id = "thai_consonants_1"
        
        # Baseline: 50%
        baseline_results = [
            TestResult("b1", "Q1", "wrong", "k", False, "recall"),
            TestResult("b2", "Q2", "kh", "kh", True, "recall"),
        ]
        self.workflow.record_assessment(
            "baseline_1", "baseline", lesson_id, baseline_results
        )
        
        # Post-test: 100%
        post_results = [
            TestResult("p1", "Q1", "k", "k", True, "recall"),
            TestResult("p2", "Q2", "kh", "kh", True, "recall"),
        ]
        self.workflow.record_assessment(
            "post_1", "immediate_recall", lesson_id, post_results
        )
        
        # Calculate gain
        gain = self.workflow.calculate_learning_gain(lesson_id)
        
        self.assertIsNotNone(gain)
        if gain:
            self.assertEqual(gain.baseline_score, 0.5)
            self.assertEqual(gain.posttest_score, 1.0)
            self.assertEqual(gain.gain, 0.5)
            self.assertEqual(gain.gain_percentage, 100.0)  # 50% improvement is 100% gain
        
        # Verify persisted
        self.assertEqual(len(self.workflow.learning_gains), 1)
    
    def test_transfer_test_novel_items(self):
        """GUARANTEE: Transfer tests use novel item formats."""
        original_items = [
            TestItem(
                item_id="orig_1",
                prompt="What sound does ก make?",
                correct_answer="k",
                item_type="recall",
            ),
            TestItem(
                item_id="orig_2",
                prompt="What sound does ข make?",
                correct_answer="kh",
                item_type="recall",
            ),
        ]
        
        # Generate transfer items (rephrased)
        transfer_items = self.workflow.generate_transfer_items(
            original_items, transform="rephrase"
        )
        
        self.assertEqual(len(transfer_items), 2)
        
        # Verify items are different
        self.assertNotEqual(transfer_items[0].prompt, original_items[0].prompt)
        self.assertNotEqual(transfer_items[1].prompt, original_items[1].prompt)
        
        # But answers are same
        self.assertEqual(transfer_items[0].correct_answer, original_items[0].correct_answer)
        self.assertEqual(transfer_items[1].correct_answer, original_items[1].correct_answer)
        
        # Verify item type
        self.assertEqual(transfer_items[0].item_type, "transfer")
        
        # Check specific transformations
        self.assertIn("Which sound is produced by", transfer_items[0].prompt)
    
    def test_mastery_decision_from_evidence(self):
        """GUARANTEE: Mastery decisions based on actual evidence."""
        lesson_id = "thai_consonants_1"
        
        # Record assessments
        self.workflow.record_assessment(
            "imm_1",
            "immediate_recall",
            lesson_id,
            [TestResult(f"i{i}", f"Q{i}", "a", "a", True, "recall") for i in range(10)],
        )
        self.workflow.record_assessment(
            "ret_1",
            "retention",
            lesson_id,
            [TestResult(f"r{i}", f"Q{i}", "a", "a", True, "recall") for i in range(8)] +
            [TestResult(f"r{i}", f"Q{i}", "wrong", "a", False, "recall") for i in range(2)],
        )
        self.workflow.record_assessment(
            "trans_1",
            "transfer",
            lesson_id,
            [TestResult(f"t{i}", f"Q{i}", "a", "a", True, "transfer") for i in range(7)] +
            [TestResult(f"t{i}", f"Q{i}", "wrong", "a", False, "transfer") for i in range(3)],
        )
        
        # Make decision
        decision = self.workflow.make_mastery_decision(lesson_id)
        
        # Verify evidence
        self.assertEqual(decision.evidence["immediate_recall"], 1.0)
        self.assertEqual(decision.evidence["retention"], 0.8)
        self.assertEqual(decision.evidence["transfer"], 0.7)
        
        # Verify decision (all thresholds met)
        self.assertEqual(decision.decision, "MASTERED")
        self.assertEqual(decision.next_action, "ADVANCE")
        
        # Verify persisted
        self.assertEqual(len(self.workflow.mastery_decisions), 1)
    
    def test_remediation_after_failure(self):
        """GUARANTEE: Remediation triggered after low scores."""
        lesson_id = "thai_consonants_1"
        
        # Record poor performance
        self.workflow.record_assessment(
            "imm_1",
            "immediate_recall",
            lesson_id,
            [TestResult(f"i{i}", f"Q{i}", "wrong", "a", False, "recall") for i in range(8)] +
            [TestResult(f"i{i}", f"Q{i}", "a", "a", True, "recall") for i in range(2)],
        )
        
        decision = self.workflow.make_mastery_decision(lesson_id)
        
        # Should trigger remediation (20% < 50%)
        self.assertEqual(decision.decision, "REMEDIATE")
        self.assertEqual(decision.next_action, "RETEACH")
        self.assertTrue(self.workflow.needs_remediation(lesson_id))
    
    def test_autonomous_continuation(self):
        """GUARANTEE: Autonomous loop can get next lesson from IRI state."""
        from runtime.education.curriculum import Curriculum
        from runtime.education.subject import Subject
        from runtime.education.lesson import Lesson
        
        # Create curriculum
        curriculum = Curriculum()
        subject = Subject(
            id="thai",
            name="Thai Language",
            subject_type=SubjectType.LANGUAGE
        )
        curriculum.add_subject(subject)
        
        lesson1 = Lesson(
            subject_id="thai",
            level=1,
            title="Consonants 1-3",
            objectives=["Learn ก ข ฃ"],
            id="thai_1",
        )
        lesson2 = Lesson(
            subject_id="thai",
            level=1,
            title="Consonants 4-6",
            objectives=["Learn ค ฅ ฆ"],
            id="thai_2",
            prerequisites=["thai_1"],
        )
        curriculum.add_lesson(lesson1)
        curriculum.add_lesson(lesson2)
        
        # Initially, should return first lesson
        next_lesson = self.workflow.get_next_lesson_for_autonomous(curriculum)
        self.assertEqual(next_lesson, "thai_1")
        
        # Mark first lesson as mastered
        self.workflow.lesson_status["thai_1"] = "MASTERED"
        curriculum.mastery_tracker.record_attempt("thai_1", 0.9)
        
        # Should now return second lesson
        next_lesson = self.workflow.get_next_lesson_for_autonomous(curriculum)
        self.assertEqual(next_lesson, "thai_2")
        
        # Mark second as mastered
        self.workflow.lesson_status["thai_2"] = "MASTERED"
        
        # Should return None (all done)
        next_lesson = self.workflow.get_next_lesson_for_autonomous(curriculum)
        self.assertIsNone(next_lesson)
    
    def test_state_persistence_full_cycle(self):
        """GUARANTEE: Complete cycle persists to IRI state."""
        lesson_id = "thai_consonants_1"
        
        # Full cycle
        # 1. Baseline
        self.workflow.record_assessment(
            "baseline_1", "baseline", lesson_id,
            [TestResult(f"b{i}", f"Q{i}", "wrong", "a", False, "recall") for i in range(2)]
        )
        
        # 2. Post-test
        self.workflow.record_assessment(
            "post_1", "immediate_recall", lesson_id,
            [TestResult(f"p{i}", f"Q{i}", "a", "a", True, "recall") for i in range(2)]
        )
        
        # 3. Learning gain
        gain = self.workflow.calculate_learning_gain(lesson_id)
        
        # 4. Retention
        self.workflow.record_assessment(
            "ret_1", "retention", lesson_id,
            [TestResult(f"r{i}", f"Q{i}", "a", "a", True, "recall") for i in range(2)]
        )
        
        # 5. Transfer
        self.workflow.record_assessment(
            "trans_1", "transfer", lesson_id,
            [TestResult(f"t{i}", f"Q{i}", "a", "a", True, "transfer") for i in range(2)]
        )
        
        # 6. Mastery decision
        decision = self.workflow.make_mastery_decision(lesson_id)
        
        # Reload from disk
        workflow2 = SchoolWorkflow(state_file=self.state_file)
        
        # Verify everything persisted
        self.assertEqual(len(workflow2.assessments), 4)
        self.assertEqual(len(workflow2.learning_gains), 1)
        self.assertEqual(len(workflow2.mastery_decisions), 1)
        self.assertEqual(workflow2.lesson_status[lesson_id], "MASTERED")
    
    def test_answer_leakage_prevention(self):
        """GUARANTEE: Transfer tests use different formats to prevent leakage."""
        original = [
            TestItem("1", "What sound does ก make?", "k", "recall"),
        ]
        
        # Test different transformations
        rephrase = self.workflow.generate_transfer_items(original, "rephrase")
        self.assertIn("Which sound is produced by", rephrase[0].prompt)
        self.assertNotIn("What sound does", rephrase[0].prompt)
        
        reverse = self.workflow.generate_transfer_items(original, "reverse")
        self.assertIn("Which character makes the sound", reverse[0].prompt)
        
        apply = self.workflow.generate_transfer_items(original, "apply")
        self.assertIn("If you see", apply[0].prompt)
        self.assertIn("what sound do you pronounce", apply[0].prompt)


if __name__ == "__main__":
    unittest.main()
