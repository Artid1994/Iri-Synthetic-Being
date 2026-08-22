import unittest

from runtime.goal import Goal
from runtime.intention import Intention
from runtime.teaching import Teaching
from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "ok"


class TestRuntimeStateConsistencyContract(unittest.TestCase):
    def test_registered_objects_remain_independent(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        goal = Goal(description="learn")
        intention = Intention(
            description="inspect",
            goal_id=goal.id,
        )
        teaching = Teaching(content="trees have leaves")

        runtime.add_goal(goal)
        runtime.add_intention(intention)
        runtime.add_teaching(teaching)

        self.assertEqual(runtime.goals, [goal])
        self.assertEqual(runtime.intentions, [intention])
        self.assertEqual(runtime.teachings, [teaching])

    def test_goal_completion_does_not_remove_related_intention(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        goal = Goal(description="learn")
        intention = Intention(
            description="inspect",
            goal_id=goal.id,
        )

        runtime.add_goal(goal)
        runtime.add_intention(intention)

        goal.complete()

        self.assertIn(goal, runtime.goals)
        self.assertIn(intention, runtime.intentions)
        self.assertIs(
            runtime.get_goal_for_intention(intention),
            goal,
        )

    def test_teaching_learning_does_not_remove_teaching(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        teaching = Teaching(content="trees have leaves")
        runtime.add_teaching(teaching)

        runtime.learn_teaching(teaching)

        self.assertIn(teaching, runtime.teachings)
        self.assertEqual(teaching.status, "ACCEPTED")


if __name__ == "__main__":
    unittest.main()
