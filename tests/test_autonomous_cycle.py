import unittest

from runtime.body_command import BodyCommand
from runtime.robot_feedback import RobotFeedback


class FakeRuntime:
    def __init__(self):
        self.observed = False
        self.thought = ""
        self.command = None
        self.feedback = None
        self.learned = False

    def observe(self):
        self.observed = True
        return "tree is near the house"

    def think(self, observation):
        self.thought = observation
        return "tree is near the house"

    def decide(self, reasoning):
        self.command = BodyCommand(
            action="observe",
            value=reasoning,
        )
        return self.command

    def act(self, command):
        self.feedback = RobotFeedback(
            success=True,
            action=command.action,
            value=command.value,
        )
        return self.feedback

    def learn(self, feedback):
        self.learned = feedback.success


class TestAutonomousCycle(unittest.TestCase):
    def test_one_cycle_completes_observe_think_decide_act_learn(self):
        runtime = FakeRuntime()

        observation = runtime.observe()
        reasoning = runtime.think(observation)
        command = runtime.decide(reasoning)
        feedback = runtime.act(command)
        runtime.learn(feedback)

        self.assertTrue(runtime.observed)
        self.assertEqual(reasoning, "tree is near the house")
        self.assertIsNotNone(command)
        self.assertTrue(feedback.success)
        self.assertTrue(runtime.learned)


if __name__ == "__main__":
    unittest.main()
