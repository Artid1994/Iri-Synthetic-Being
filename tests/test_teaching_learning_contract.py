import unittest

from runtime.learning import Learning
from runtime.memory import Memory
from runtime.teaching import Teaching


class TestTeachingLearningContract(unittest.TestCase):
    def test_learning_can_evaluate_teaching(self):
        memory = Memory()
        learning = Learning(memory)
        teaching = Teaching(content="trees have leaves")

        evaluation = learning.evaluate_teaching(teaching)

        self.assertTrue(evaluation.accepted)

    def test_accepted_teaching_enters_semantic_memory(self):
        memory = Memory()
        learning = Learning(memory)
        teaching = Teaching(content="trees have leaves")

        learning.evaluate_teaching(teaching)

        self.assertTrue(
            memory.semantic_contains("trees have leaves")
        )

    def test_invalid_teaching_does_not_enter_memory(self):
        memory = Memory()
        learning = Learning(memory)

        evaluation = learning.evaluate_teaching(object())

        self.assertFalse(evaluation.accepted)
        self.assertEqual(evaluation.reason, "INVALID_TEACHING")
        self.assertTrue(memory.is_empty())


if __name__ == "__main__":
    unittest.main()
