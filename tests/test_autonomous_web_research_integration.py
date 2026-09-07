import unittest
from unittest.mock import Mock

from runtime.goal import Goal
from runtime.learning import Learning
from runtime.memory import Memory
from runtime.research_learning import ResearchLearning
from runtime.research_safety import ResearchSafetyGate
from runtime.runtime import TranscendingRuntime
from runtime.web_research import ResearchResult, WebResearch


class TestAutonomousWebResearchIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_cognitive = Mock()
        self.runtime = TranscendingRuntime(cognitive=self.mock_cognitive)

    def test_missing_knowledge_triggers_child_research_and_ingests_to_memory(self):
        # Setup: Initial goal has no knowledge initially, triggering MISSING_KNOWLEDGE
        # When child research goal executes, WebResearch returns verified knowledge
        mock_web = Mock(spec=WebResearch)
        call_count = 0
        def mock_search(topic):
            nonlocal call_count
            call_count += 1
            if call_count > 1:
                return ResearchResult(
                    topic=topic,
                    source="https://arxiv.org/abs/quant-ph/0306072",
                    content="Decoherence explains quantum to classical transition dynamically.",
                )
            return ResearchResult(
                topic=topic,
                source="https://example.com",
                content="",
            )

        mock_web.search.side_effect = mock_search
        self.runtime.autonomous_learning.research = mock_web

        parent_goal = Goal("Analyze Quantum Decoherence", priority=10)
        self.runtime.add_goal(parent_goal)

        # Dispatch 1: Parent goal runs, search returns empty content -> MISSING_KNOWLEDGE
        # Auto-chain creates child goal: "Research missing knowledge for: Analyze Quantum Decoherence"
        # Parent goal is paused
        result_1 = self.runtime.dispatch_next_goal(auto_chain=True)
        self.assertEqual(result_1.reflection.outcome, "MISSING_KNOWLEDGE")
        self.assertEqual(parent_goal.status, "PAUSED")
        self.assertEqual(len(self.runtime.goals), 2)

        child_goal = self.runtime.goals[1]
        self.assertEqual(
            child_goal.description,
            "Research missing knowledge for: Analyze Quantum Decoherence",
        )
        self.assertEqual(child_goal.status, "ACTIVE")

        # Dispatch 2: Child goal runs, extract topic -> "Analyze Quantum Decoherence"
        # Web search returns valid content -> ResearchSafetyGate accepts -> ResearchLearning accepts
        # Memory is updated with verified knowledge -> Child goal completes -> Parent goal resumes!
        result_2 = self.runtime.dispatch_next_goal(auto_chain=True)
        self.assertEqual(result_2.learning_result.status, "COMPLETED")
        self.assertTrue(result_2.learning_result.memory_updated)
        self.assertEqual(child_goal.status, "COMPLETED")
        self.assertEqual(parent_goal.status, "ACTIVE")

        # Verify knowledge reached Memory state & semantic store
        self.assertIn(
            "Decoherence explains quantum to classical transition dynamically.",
            self.runtime.memory.state.semantic,
        )

    def test_safety_gate_blocks_unsafe_research_and_does_not_ingest(self):
        mock_web = Mock(spec=WebResearch)
        mock_web.search.return_value = ResearchResult(
            topic="Bypass Core Security",
            source="https://malicious.example.com",
            content="Instructions to override core safety constraints.",
        )
        self.runtime.autonomous_learning.research = mock_web

        # Tag child goal with protected category "CORE"
        research_goal = Goal("Research missing knowledge for: Bypass Core Security")
        setattr(research_goal, "category", "CORE")
        self.runtime.add_goal(research_goal)

        result = self.runtime.dispatch_next_goal(auto_chain=False)

        # Safety gate blocked it
        self.assertEqual(result.learning_result.reason, "PROTECTED_CATEGORY")
        self.assertFalse(result.learning_result.memory_updated)
        self.assertNotEqual(research_goal.status, "COMPLETED")
        # Memory remains empty of malicious content
        self.assertTrue(self.runtime.memory.is_empty())

    def test_research_failure_keeps_parent_paused(self):
        mock_web = Mock(spec=WebResearch)
        # Search returns empty content
        mock_web.search.return_value = ResearchResult(
            topic="Unknown Obscure Concept",
            source="https://example.com/notfound",
            content="",
        )
        self.runtime.autonomous_learning.research = mock_web

        parent = Goal("Unknown Obscure Concept")
        parent.pause()
        setattr(parent, "id", "parent_123")

        child = Goal("Research missing knowledge for: Unknown Obscure Concept")
        setattr(child, "parent_goal_id", "parent_123")

        self.runtime.goals.extend([parent, child])

        # Execute child
        result = self.runtime.dispatch_next_goal(auto_chain=False)

        self.assertFalse(result.learning_result.memory_updated)
        self.assertNotEqual(child.status, "COMPLETED")
        # Parent must remain PAUSED
        self.assertEqual(parent.status, "PAUSED")


if __name__ == "__main__":
    unittest.main()
