import unittest

from runtime.action_mapper import ActionMapper
from runtime.body_command import BodyCommand


class TestActionMapper(unittest.TestCase):
    def test_respond_maps_to_body_command(self):
        command = ActionMapper.map_decision("RESPOND")

        self.assertIsInstance(command, BodyCommand)
        self.assertEqual(command.action, "respond")

    def test_move_mapping_remains_unchanged(self):
        command = ActionMapper.map_decision("MOVE")

        self.assertIsInstance(command, BodyCommand)
        self.assertEqual(command.action, "move")
        self.assertEqual(command.value, (1.0, 0.0))


if __name__ == "__main__":
    unittest.main()
