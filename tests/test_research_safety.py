import unittest

from runtime.research_safety import ResearchSafetyGate
from runtime.web_research import ResearchResult


class TestResearchSafetyGate(unittest.TestCase):
    def make_result(self, content="Python is a language."):
        return ResearchResult(
            topic="Python",
            source="https://example.com",
            content=content,
        )

    def test_valid_research_is_accepted(self):
        gate = ResearchSafetyGate()

        result = gate.evaluate(self.make_result())

        self.assertTrue(result.accepted)
        self.assertEqual(
            result.reason,
            "RESEARCH_ACCEPTED",
        )

    def test_empty_content_is_rejected(self):
        gate = ResearchSafetyGate()

        result = gate.evaluate(
            self.make_result(content="")
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.reason,
            "EMPTY_RESEARCH_CONTENT",
        )

    def test_protected_category_is_rejected(self):
        gate = ResearchSafetyGate()

        result = gate.evaluate(
            self.make_result(),
            category="CORE",
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.reason,
            "PROTECTED_CATEGORY",
        )

    def test_invalid_result_is_rejected(self):
        gate = ResearchSafetyGate()

        result = gate.evaluate(object())

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.reason,
            "INVALID_RESEARCH_RESULT",
        )


if __name__ == "__main__":
    unittest.main()
