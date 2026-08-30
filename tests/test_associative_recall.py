import unittest

from runtime.associative_recall import AssociativeRecall
from runtime.memory import Memory


class TestAssociativeRecall(unittest.TestCase):

    def test_remember_and_recall(self):
        memory = Memory()
        recall = AssociativeRecall(memory)

        recall.remember("ชื่อ", "เอ๋")

        self.assertEqual(
            recall.recall("ชื่อ"),
            ["เอ๋"],
        )

    def test_missing_memory_returns_empty(self):
        memory = Memory()
        recall = AssociativeRecall(memory)

        self.assertEqual(
            recall.recall("ชื่อ"),
            [],
        )

    def test_recall_can_match_related_episodic_experience(self):
        memory = Memory()
        recall = AssociativeRecall(memory)

        memory.add_experience("ฉันชื่อ T1000")

        result = recall.recall("ฉันชื่ออะไร")

        self.assertIn("ฉันชื่อ T1000", result)

    def test_recall_can_match_preference_question(self):
        memory = Memory()
        recall = AssociativeRecall(memory)

        memory.add_experience("ฉันชอบสีแดง")

        result = recall.recall("สีโปรดของฉันคืออะไร")

        self.assertIn("ฉันชอบสีแดง", result)



    def test_unrelated_question_does_not_recall_unrelated_memory(self):
        memory = Memory()
        recall = AssociativeRecall(memory)

        memory.add_experience("ฉันชื่อ T1000")
        memory.add_experience("ฉันชอบสีแดง")

        result = recall.recall("ฉันชอบอาหารอะไร")

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
    def test_contextual_recall_prefers_matching_topic(self):
        memory = Memory()
        recall = AssociativeRecall(memory)

        memory.add_experience("ฉันชอบสีแดง")
        memory.add_experience("วันนี้ฉันกินข้าว")

        result = recall.recall("ฉันชอบสีอะไร")

        self.assertEqual(result, ["ฉันชอบสีแดง"])
