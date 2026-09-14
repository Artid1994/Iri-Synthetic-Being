"""
Autonomous Loop Adapter for School Workflow
Connects AutonomousLoopController with SchoolWorkflow
"""
from pathlib import Path

from runtime.autonomous_school import AutonomousSchool
from runtime.education.school_workflow import SchoolWorkflow, TestResult
from runtime.education.curriculum import Curriculum


class SchoolWorkflowAdapter:
    """
    Adapter: AutonomousLoopController → AutonomousSchool → SchoolWorkflow
    
    Enables autonomous_loop.py to drive complete learning cycles.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        
        # Initialize workflow
        state_file = self.project_root / "03_Hippocampus" / "school_state.json"
        self.workflow = SchoolWorkflow(state_file=state_file)
        
        # Initialize curriculum (loaded from curriculum data)
        self.curriculum = self._load_curriculum()
        
        # Initialize autonomous school
        self.school = AutonomousSchool(self.workflow, self.curriculum)
    
    def _load_curriculum(self) -> Curriculum:
        """Load curriculum from knowledge base."""
        # TODO: Implement curriculum loading from knowledge_base/
        return Curriculum()
    
    def get_current_learning_objective(self) -> str:
        """Get current learning objective for autonomous loop."""
        return self.school.get_current_objective() or "No active learning objective"
    
    def get_next_action(self) -> str:
        """Get next action for autonomous loop."""
        return self.school.get_next_action()
    
    def execute_action(self, action: str, **kwargs) -> dict:
        """
        Execute learning action.
        
        Returns:
            result with status and next_action
        """
        if action == "ASSESS":
            # Conduct assessment (delegated to teaching system)
            return {"status": "AWAITING_ASSESSMENT", "phase": self.school.current_phase}
        
        elif action == "TEACH":
            # Teach lesson (delegated to teaching system)
            return {"status": "AWAITING_TEACHING", "lesson": self.school.current_lesson_id}
        
        elif action == "PRACTICE":
            # Practice lesson (delegated to practice system)
            return {"status": "AWAITING_PRACTICE", "lesson": self.school.current_lesson_id}
        
        elif action == "ADVANCE":
            # Lesson mastered, advance automatically
            self.school.current_lesson_id = None
            self.school.current_phase = "IDLE"
            return {"status": "ADVANCED", "next_objective": self.get_current_learning_objective()}
        
        else:
            return {"status": "IDLE"}
    
    def record_assessment_results(self, lesson_id: str, results: list, assessment_type: str):
        """Record assessment results from teaching system."""
        test_results = [
            TestResult(
                item_id=r["item_id"],
                prompt=r["prompt"],
                student_answer=r["student_answer"],
                correct_answer=r["correct_answer"],
                is_correct=r["is_correct"],
                item_type=r.get("item_type", "recall"),
            )
            for r in results
        ]
        
        self.school.record_lesson_completion(lesson_id, test_results, assessment_type)
        self.school.advance_phase()
