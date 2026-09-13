"""
Example usage of the IRI Development Multi-Agent Workflow Orchestrator.
"""

from pathlib import Path
from dev_workflow import WorkflowOrchestrator


def example_simple_task():
    """Example: Simple task with reasonable limits."""
    
    orchestrator = WorkflowOrchestrator(
        task_id="example-001",
        goal="Add logging to the Identity module",
        acceptance_criteria=[
            "All public methods log entry and exit",
            "Log level is configurable",
            "Tests verify logging behavior",
            "No breaking changes to existing tests",
        ],
        total_token_budget=50000,
        context_limit=100000,
        max_iterations=5,
        max_fix_iterations=3,
    )
    
    # In v1, this would execute the workflow
    # In production, this would invoke delegate_task
    print("Orchestrator initialized:")
    print(f"  Task: {orchestrator.state.task_id}")
    print(f"  Goal: {orchestrator.state.goal}")
    print(f"  Token Budget: {orchestrator.state.total_token_budget}")
    print(f"  Context Limit: {orchestrator.state.context_limit}")
    print(f"  Max Iterations: {orchestrator.state.max_iterations}")
    
    # Save initial state
    state_path = Path("logs/workflow_states/example-001.json")
    orchestrator.save_state(state_path)
    print(f"\nState saved to: {state_path}")
    
    # Get summary
    print("\n" + orchestrator.get_summary())


def example_budget_constrained():
    """Example: Task with tight budget constraints."""
    
    orchestrator = WorkflowOrchestrator(
        task_id="example-002",
        goal="Fix critical security vulnerability in authentication",
        acceptance_criteria=[
            "Vulnerability is patched",
            "No bypass paths remain",
            "Security tests pass",
            "Red team verification passes",
        ],
        total_token_budget=20000,  # Tight budget
        context_limit=50000,
        max_iterations=3,
        max_fix_iterations=2,
    )
    
    print("Budget-constrained task:")
    print(f"  Token Budget: {orchestrator.state.total_token_budget}")
    print(f"  Iterations: {orchestrator.state.max_iterations}")
    
    # Check if initial prompt fits budget
    test_prompt = orchestrator._build_prompt()
    approved, msg, tokens, optimized = orchestrator.auditor.audit_prompt(
        test_prompt,
        expected_output_size=2000,
    )
    
    print(f"\nInitial prompt audit:")
    print(f"  Approved: {approved}")
    print(f"  Estimated tokens: {tokens}")
    print(f"  Message: {msg}")


def example_context_aware():
    """Example: Task with context management."""
    
    orchestrator = WorkflowOrchestrator(
        task_id="example-003",
        goal="Refactor Memory subsystem for better performance",
        acceptance_criteria=[
            "Memory operations are 2x faster",
            "All existing tests pass",
            "No memory leaks",
            "Benchmarks document improvement",
        ],
        total_token_budget=100000,
        context_limit=80000,  # Smaller context
        max_iterations=10,
    )
    
    # Simulate context growth
    orchestrator.context_governor.update(50000)
    
    status = orchestrator.context_governor.get_status()
    can_continue, ctx_status, msg = orchestrator.context_governor.can_continue(
        estimated_growth=15000
    )
    
    print("Context-aware execution:")
    print(f"  Context used: {orchestrator.context_governor.context_used}")
    print(f"  Context status: {status.value}")
    print(f"  Can continue: {can_continue}")
    print(f"  Message: {msg}")


def example_workflow_state():
    """Example: Working with workflow state."""
    
    orchestrator = WorkflowOrchestrator(
        task_id="example-004",
        goal="Implement new cognitive trigger",
        acceptance_criteria=[
            "Trigger detects target pattern",
            "Trigger integrates with CognitiveEngine",
            "Tests verify trigger behavior",
        ],
        total_token_budget=60000,
    )
    
    # Simulate some progress
    orchestrator.state.iteration = 2
    orchestrator.state.tokens_used = 15000
    orchestrator.budget_governor.used = 15000
    
    # Get state snapshot
    state_dict = orchestrator.state.to_dict()
    
    print("Workflow state:")
    print(f"  Iteration: {state_dict['iteration']}/{state_dict['max_iterations']}")
    print(f"  Tokens used: {state_dict['tokens_used']}/{state_dict['total_token_budget']}")
    print(f"  Tokens remaining: {state_dict['tokens_remaining']}")
    print(f"  Status: {state_dict['status']}")


if __name__ == "__main__":
    print("=" * 70)
    print("IRI Development Multi-Agent Workflow Orchestrator - Examples")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("Example 1: Simple Task")
    print("=" * 70)
    example_simple_task()
    
    print("\n" + "=" * 70)
    print("Example 2: Budget-Constrained Task")
    print("=" * 70)
    example_budget_constrained()
    
    print("\n" + "=" * 70)
    print("Example 3: Context-Aware Execution")
    print("=" * 70)
    example_context_aware()
    
    print("\n" + "=" * 70)
    print("Example 4: Workflow State Management")
    print("=" * 70)
    example_workflow_state()
