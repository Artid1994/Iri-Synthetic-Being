"""
Integration tests: SchoolWorkflow + AutonomousSchool + Curriculum
Verify complete autonomous learning cycle
"""
import unittest
from pathlib import Path
import tempfile

from runtime.education.school_workflow import (
    SchoolWorkflow,
    TestItem,
    TestResult,
)
from runtime.autonomous_school import AutonomousSchool
from runtime.education.curriculum import Curriculum
from runtime.education.subject import Subject, SubjectType
from runtime.education.lesson import Lesson


class TestAutonomousSchoolIntegration(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = Path(self.temp_dir) / "school_state.json"
        
        # Create workflow
        self.workflow = SchoolWorkflow(state_file=self.state_file)
        
        # Create curriculum
        self.curriculum = Curriculum()
        
        subject = Subject(
            id="thai",
            name="Thai Language",
            subject_type=SubjectType.LANGUAGE,
        )
        self.curriculum.add_subject(subject)
        
        # Add lessons
        self.lesson1 = Lesson(
            subject_id="thai",
            level=1,
            title="Thai Consonants 1-3",
            objectives=["Learn ก ข ฃ"],
            id="thai_cons_1",
        )
        self.lesson2 = Lesson(
            subject_id="thai",
            level=1,
            title="Thai Consonants 4-6",
            objectives=["Learn ค ฅ ฆ"],
            id="thai_cons_2",
            prerequisites=["thai_cons_1"],
        )
        
        self.curriculum.add_lesson(self.lesson1)
        self.curriculum.add_lesson(self.lesson2)
        
        # Create autonomous school
        self.school = AutonomousSchool(self.workflow, self.curriculum)
    
    def test_autonomous_cycle_full(self):
        """INTEGRATION: Complete autonomous learning cycle without human intervention."""
        
        # Initial state
        self.assertEqual(self.school.current_phase, "IDLE")
        
        # Get first objective
        objective = self.school.get_current_objective()
        self.assertIsNotNone(objective)
        if objective:
            self.assertIn("Thai Consonants 1-3", objective)
        self.assertEqual(self.school.current_lesson_id, "thai_cons_1")
        self.assertEqual(self.school.current_phase, "BASELINE")
        
        # Phase 1: Baseline
        action = self.school.get_next_action()
        self.assertEqual(action, "ASSESS")
        
        # Simulate baseline test (poor performance)
        baseline_results = [
            TestResult("b1", "Q1", "", "k", False, "recall"),
            TestResult("b2", "Q2", "", "kh", False, "recall"),
            TestResult("b3", "Q3", "", "kh", False, "recall"),
        ]
        self.school.record_lesson_completion(
            "thai_cons_1", baseline_results, "baseline"
        )
        
        # Advance to teaching
        self.school.advance_phase()
        self.assertEqual(self.school.current_phase, "TEACHING")
        
        action = self.school.get_next_action()
        self.assertEqual(action, "TEACH")
        
        # Phase 2: Teaching (simulated)
        self.school.advance_phase()
        self.assertEqual(self.school.current_phase, "PRACTICE")
        
        # Phase 3: Practice
        action = self.school.get_next_action()
        self.assertEqual(action, "PRACTICE")
        
        self.school.advance_phase()
        self.assertEqual(self.school.current_phase, "POST_TEST")
        
        # Phase 4: Post-test (good performance)
        action = self.school.get_next_action()
        self.assertEqual(action, "ASSESS")
        
        posttest_results = [
            TestResult("p1", "Q1", "k", "k", True, "recall"),
            TestResult("p2", "Q2", "kh", "kh", True, "recall"),
            TestResult("p3", "Q3", "kh", "kh", True, "recall"),
        ]
        self.school.record_lesson_completion(
            "thai_cons_1", posttest_results, "immediate_recall"
        )
        
        # Verify learning gain calculated
        self.assertEqual(len(self.workflow.learning_gains), 1)
        gain = self.workflow.learning_gains[0]
        self.assertEqual(gain.baseline_score, 0.0)
        self.assertEqual(gain.posttest_score, 1.0)
        
        # Phase 5: Retention
        self.school.advance_phase()
        self.assertEqual(self.school.current_phase, "RETENTION")
        
        retention_results = [
            TestResult("r1", "Q1", "k", "k", True, "recall"),
            TestResult("r2", "Q2", "kh", "kh", True, "recall"),
            TestResult("r3", "Q3", "kh", "kh", True, "recall"),
        ]
        self.school.record_lesson_completion(
            "thai_cons_1", retention_results, "retention"
        )
        
        # Phase 6: Transfer
        self.school.advance_phase()
        self.assertEqual(self.school.current_phase, "TRANSFER")
        
        # Create transfer test with novel items
        original_items = [
            TestItem("orig1", "What sound does ก make?", "k", "recall"),
            TestItem("orig2", "What sound does ข make?", "kh", "recall"),
        ]
        transfer_items = self.school.create_transfer_test("thai_cons_1", original_items)
        
        # Verify transfer items are different
        self.assertNotEqual(transfer_items[0].prompt, original_items[0].prompt)
        
        transfer_results = [
            TestResult("t1", transfer_items[0].prompt, "k", "k", True, "transfer"),
            TestResult("t2", transfer_items[1].prompt, "kh", "kh", True, "transfer"),
            TestResult("t3", "Novel Q3", "kh", "kh", True, "transfer"),
        ]
        self.school.record_lesson_completion(
            "thai_cons_1", transfer_results, "transfer"
        )
        
        # Phase 7: Decision
        self.school.advance_phase()
        self.assertEqual(self.school.current_phase, "DECISION")
        
        action = self.school.get_next_action()
        
        # Should advance (all thresholds met)
        self.assertEqual(action, "ADVANCE")
        self.assertEqual(self.school.current_phase, "IDLE")
        self.assertIsNone(self.school.current_lesson_id)
        
        # Verify mastery decision
        self.assertEqual(len(self.workflow.mastery_decisions), 1)
        decision = self.workflow.mastery_decisions[0]
        self.assertEqual(decision.decision, "MASTERED")
        self.assertEqual(decision.next_action, "ADVANCE")
        
        # Verify lesson marked as mastered
        self.assertTrue(self.school.is_lesson_mastered("thai_cons_1"))
        
        # Next objective should be lesson 2
        objective = self.school.get_current_objective()
        self.assertIsNotNone(objective)
        if objective:
            self.assertIn("Thai Consonants 4-6", objective)
        self.assertEqual(self.school.current_lesson_id, "thai_cons_2")
    
    def test_remediation_cycle(self):
        """INTEGRATION: Autonomous remediation after failure."""
        
        # Start lesson
        self.school.get_current_objective()
        self.school.advance_phase()  # to TEACHING
        self.school.advance_phase()  # to PRACTICE
        self.school.advance_phase()  # to POST_TEST
        
        # Poor post-test performance
        poor_results = [
            TestResult("p1", "Q1", "", "k", False, "recall"),
            TestResult("p2", "Q2", "kh", "kh", True, "recall"),
            TestResult("p3", "Q3", "", "kh", False, "recall"),
        ]
        self.school.record_lesson_completion(
            "thai_cons_1", poor_results, "immediate_recall"
        )
        
        # Skip to decision
        self.school.current_phase = "DECISION"
        action = self.school.get_next_action()
        
        # Should go back to teaching (remediation)
        self.assertEqual(action, "TEACH")
        self.assertEqual(self.school.current_phase, "TEACHING")
        self.assertTrue(self.school.needs_remediation())
    
    def test_persistence_across_sessions(self):
        """INTEGRATION: Learning state persists across sessions."""
        
        # Complete baseline
        self.school.get_current_objective()
        baseline_results = [
            TestResult("b1", "Q1", "", "k", False, "recall"),
        ]
        self.school.record_lesson_completion(
            "thai_cons_1", baseline_results, "baseline"
        )
        
        # Verify persisted
        self.assertTrue(self.state_file.exists())
        
        # Create new session
        workflow2 = SchoolWorkflow(state_file=self.state_file)
        school2 = AutonomousSchool(workflow2, self.curriculum)
        
        # Verify state loaded
        self.assertEqual(len(workflow2.assessments), 1)
        self.assertEqual(workflow2.assessments[0].lesson_id, "thai_cons_1")
        self.assertEqual(workflow2.assessments[0].assessment_type, "baseline")
    
    def test_progress_summary(self):
        """INTEGRATION: Get complete progress summary."""
        
        # Master first lesson
        self.workflow.lesson_status["thai_cons_1"] = "MASTERED"
        
        # Start second lesson
        self.workflow.lesson_status["thai_cons_2"] = "CONTINUE_PRACTICE"
        
        summary = self.school.get_progress_summary()
        
        self.assertIn("thai_cons_1", summary["lessons_mastered"])
        self.assertIn("thai_cons_2", summary["lessons_in_progress"])
    
    def test_prerequisite_blocking(self):
        """INTEGRATION: Prerequisites block advancement."""
        
        # Try to get objective (should start with lesson 1)
        objective = self.school.get_current_objective()
        self.assertEqual(self.school.current_lesson_id, "thai_cons_1")
        
        # Manually try to start lesson 2 (should fail prerequisite check)
        self.school.current_lesson_id = None
        self.workflow.lesson_status["thai_cons_1"] = "NOT_STARTED"
        
        next_id = self.workflow.get_next_lesson_for_autonomous(self.curriculum)
        
        # Should still be lesson 1 (prerequisite not met)
        self.assertEqual(next_id, "thai_cons_1")
        
        # Mark lesson 1 as mastered in workflow (the authoritative source)
        self.workflow.lesson_status["thai_cons_1"] = "MASTERED"
        
        # Now lesson 2 should be available
        next_id = self.workflow.get_next_lesson_for_autonomous(self.curriculum)
        self.assertEqual(next_id, "thai_cons_2")


if __name__ == "__main__":
    unittest.main()
