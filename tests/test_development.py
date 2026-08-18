import unittest

from runtime.development import Development
from runtime.identity import Identity
from runtime.memory import Memory
from runtime.learning import Learning
from runtime.personality import Personality
from runtime.self_model import SelfModel
from runtime.prediction import Prediction
from runtime.identity_continuity import IdentityContinuity


class TestDevelopment(unittest.TestCase):
    def test_development_initializes(self):
        identity = Identity()
        memory = Memory()
        learning = Learning(memory=memory)
        personality = Personality()
        self_model = SelfModel()
        prediction = Prediction()
        identity_continuity = IdentityContinuity()

        development = Development(
            identity=identity,
            memory=memory,
            learning=learning,
            personality=personality,
            self_model=self_model,
            prediction=prediction,
            identity_continuity=identity_continuity,
        )

        self.assertIsNotNone(development)


if __name__ == "__main__":
    unittest.main()
