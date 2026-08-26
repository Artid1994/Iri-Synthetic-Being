import unittest

from runtime.memory import Memory


class TestWorkingMemory(unittest.TestCase):
    def test_working_memory_starts_empty(self):
        memory = Memory()

        self.assertEqual(
            memory.working_memory(),
            [],
        )

    def test_working_memory_can_store_item(self):
        memory = Memory()

        memory.add_working("tree detected")

        self.assertEqual(
            memory.working_memory(),
            ["tree detected"],
        )

    def test_working_memory_preserves_order(self):
        memory = Memory()

        memory.add_working("tree")
        memory.add_working("person")
        memory.add_working("house")

        self.assertEqual(
            memory.working_memory(),
            ["tree", "person", "house"],
        )

    def test_working_memory_ignores_blank_item(self):
        memory = Memory()

        memory.add_working("   ")

        self.assertEqual(
            memory.working_memory(),
            [],
        )

    def test_working_memory_can_clear(self):
        memory = Memory()

        memory.add_working("tree")
        memory.add_working("person")

        memory.clear_working()

        self.assertEqual(
            memory.working_memory(),
            [],
        )

    def test_working_memory_has_bounded_capacity(self):
        memory = Memory()

        memory.add_working("one", capacity=2)
        memory.add_working("two", capacity=2)
        memory.add_working("three", capacity=2)

        self.assertEqual(
            memory.working_memory(),
            ["two", "three"],
        )


if __name__ == "__main__":
    unittest.main()
