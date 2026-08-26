import unittest

from runtime.learning import Learning
from runtime.memory import Memory
from runtime.research_learning import ResearchLearning
from runtime.web_research import ResearchResult


class TestResearchLearning(unittest.TestCase):
    def test_empty_web_content_is_rejected(self):
        learning = Learning(Memory())
        research_learning = ResearchLearning(learning)

        result = ResearchResult(
            topic="Python",
            source="https://example.com",
            content="",
        )

        candidate = research_learning.create_candidate(result)

        self.assertIsNone(candidate)

    def test_web_result_becomes_learning_candidate(self):
        learning = Learning(Memory())
        research_learning = ResearchLearning(learning)

        result = ResearchResult(
            topic="Python",
            source="https://example.com",
            content="Python is a programming language.",
        )

        candidate = research_learning.create_candidate(
            result,
            confidence=0.8,
        )

        self.assertIsNotNone(candidate)
        self.assertEqual(
            candidate.category,
            "WEB_RESEARCH",
        )
        self.assertEqual(
            candidate.confidence,
            0.8,
        )

    def test_accepted_web_result_enters_memory(self):
        memory = Memory()
        learning = Learning(memory)
        research_learning = ResearchLearning(learning)

        result = ResearchResult(
            topic="Python",
            source="https://example.com",
            content="Python is a programming language.",
        )

        evaluation = research_learning.evaluate(
            result,
            confidence=0.8,
        )

        self.assertTrue(evaluation.accepted)
        self.assertIn(
            "Python is a programming language.",
            memory.state.semantic,
        )


if __name__ == "__main__":
    unittest.main()
