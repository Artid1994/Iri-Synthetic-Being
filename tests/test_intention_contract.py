import unittest

from runtime.intention import Intention


class TestIntentionContract(unittest.TestCase):
    def test_new_intention_starts_pending(self):
        intention = Intention(description="inspect the object")

        self.assertTrue(intention.id)
        self.assertEqual(intention.description, "inspect the object")
        self.assertEqual(intention.status, "PENDING")

    def test_intention_rejects_empty_description(self):
        with self.assertRaises(ValueError):
            Intention(description="")

    def test_intention_can_activate(self):
        intention = Intention(description="inspect")

        intention.activate()

        self.assertEqual(intention.status, "ACTIVE")

    def test_intention_can_complete(self):
        intention = Intention(description="inspect")

        intention.activate()
        intention.complete()

        self.assertEqual(intention.status, "COMPLETED")


if __name__ == "__main__":
    unittest.main()
