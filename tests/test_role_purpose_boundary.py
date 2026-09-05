import unittest

from runtime.agency_contract import Role, Purpose, SafetyBoundary
from runtime.goal import Goal
from runtime.identity import Identity
from runtime.intention import Intention


class TestAgencyContract(unittest.TestCase):
    def test_role_definition_and_validation(self):
        role = Role(name="ASSISTANT", description="Assists user in technical tasks")
        self.assertEqual(role.name, "ASSISTANT")
        self.assertEqual(role.description, "Assists user in technical tasks")

        with self.assertRaises(ValueError):
            Role(name="")
        with self.assertRaises(ValueError):
            Role(name="   ")

    def test_purpose_definition_and_validation(self):
        purpose = Purpose(
            declaration="Harmonious co-evolution through embodied cognition",
            rationale="To explore knowledge safely",
        )
        self.assertEqual(purpose.declaration, "Harmonious co-evolution through embodied cognition")
        self.assertEqual(purpose.rationale, "To explore knowledge safely")

        with self.assertRaises(ValueError):
            Purpose(declaration="")
        with self.assertRaises(ValueError):
            Purpose(declaration="   ")

    def test_safety_boundary_validation_and_methods(self):
        boundary = SafetyBoundary(
            allowed_actions=("move", "respond"),
            max_rate=2.5,
            restricted_targets=("system_core", "network_admin"),
        )
        self.assertTrue(boundary.is_action_allowed("move"))
        self.assertTrue(boundary.is_action_allowed("respond"))
        self.assertFalse(boundary.is_action_allowed("delete_disk"))

        self.assertTrue(boundary.is_target_restricted("system_core"))
        self.assertFalse(boundary.is_target_restricted("general_sensor"))

        with self.assertRaises(ValueError):
            SafetyBoundary(max_rate=0.0)
        with self.assertRaises(ValueError):
            SafetyBoundary(allowed_actions=())

    def test_explicit_architectural_distinctions(self):
        identity = Identity()
        role = Role(name="RESEARCH_AGENT")
        purpose = Purpose(declaration="Advance verified cognitive engineering")
        goal = Goal(description="Consolidate Phase 7")
        intention = Intention(description="Write unit tests for agency contract", goal_id=goal.id)
        boundary = SafetyBoundary()

        # 1. Identity != Role
        self.assertNotEqual(type(identity), type(role))
        self.assertFalse(hasattr(identity, "name"))
        self.assertTrue(hasattr(identity.state, "stage"))

        # 2. Role != Purpose
        self.assertNotEqual(type(role), type(purpose))
        self.assertTrue(hasattr(role, "name"))
        self.assertTrue(hasattr(purpose, "declaration"))

        # 3. Purpose != Goal
        self.assertNotEqual(type(purpose), type(goal))
        self.assertTrue(hasattr(purpose, "declaration"))
        self.assertTrue(hasattr(goal, "status"))

        # 4. Goal != Intention
        self.assertNotEqual(type(goal), type(intention))
        self.assertEqual(intention.goal_id, goal.id)
        self.assertTrue(hasattr(goal, "priority"))
        self.assertTrue(hasattr(intention, "goal_id"))

        # 5. Boundary != Role / Purpose / Identity
        self.assertNotEqual(type(boundary), type(role))
        self.assertNotEqual(type(boundary), type(purpose))
        self.assertNotEqual(type(boundary), type(identity))
        self.assertTrue(hasattr(boundary, "allowed_actions"))


if __name__ == "__main__":
    unittest.main()
