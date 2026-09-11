#!/usr/bin/env python3
"""
Test autonomous goal integration with forced IDLE state.
"""
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta

# Add path
sys.path.insert(0, str(Path(__file__).parent))

from autonomous_loop import AutonomousLoop, CircadianState
from goal_engine import GoalEngine
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def test_goal_execution():
    """Test goal execution in autonomous loop."""
    logger.info("="*60)
    logger.info("Autonomous Goal Integration Test")
    logger.info("="*60)
    
    # Initialize loop with project root
    project_root = Path(__file__).parent.parent
    loop = AutonomousLoop(project_root)
    
    # Verify goal exists
    goals = loop.goal_engine.list_goals()
    logger.info(f"Loaded {len(goals)} goals")
    
    if goals:
        goal = goals[0]
        logger.info(f"Test goal: {goal.title}")
        logger.info(f"  Priority: {goal.priority.value}")
        logger.info(f"  Status: {goal.status.value}")
        logger.info(f"  Subtasks: {len(goal.subtasks)}")
    
    # Force IDLE state to trigger goal execution
    logger.info("\nForcing IDLE state for goal execution test...")
    loop.context.last_interaction = datetime.now() - timedelta(minutes=5)
    loop.context.state = CircadianState.IDLE
    loop.context.last_state_change = datetime.now()
    
    # Execute goals manually for testing
    logger.info("\nExecuting goals in IDLE mode...")
    try:
        loop._execute_goals()
        logger.info("\nGoal execution cycle complete")
    except Exception as e:
        logger.error(f"Goal execution failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Check updated goal status
    logger.info("\nChecking updated goal state...")
    goals = loop.goal_engine.list_goals()
    if goals:
        goal = goals[0]
        logger.info(f"Goal status: {goal.status.value}")
        completed = sum(1 for t in goal.subtasks if t.status.value == 'completed')
        logger.info(f"Subtasks completed: {completed}/{len(goal.subtasks)}")
        
        # Show last executed subtask
        for task in goal.subtasks:
            if task.result:
                logger.info(f"\nLast executed subtask: {task.title}")
                logger.info(f"  Status: {task.status.value}")
                logger.info(f"  Result: {task.result[:100]}...")
                break
    
    logger.info("\n" + "="*60)
    logger.info("Test complete")
    logger.info("="*60)

if __name__ == "__main__":
    test_goal_execution()
