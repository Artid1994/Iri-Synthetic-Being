import unittest

from runtime.learning_exercise_generator import (
    LearningExerciseGenerator,
    LearningExerciseProposal,
)


class TestLearningExerciseVerificationType(unittest.TestCase):
    def test_proposal_requires_verification_type(self):
        with self.assertRaises(ValueError):
            LearningExerciseProposal.parse(
                "Question: Calculate exp(-1).\n"
                "Expected Answer: 0.367879"
            )

    def test_proposal_parses_numerical_verification(self):
        proposal = LearningExerciseProposal.parse(
            "Question: Calculate exp(-1).\n"
            "Expected Answer: 0.367879\n"
            "Verification Type: NUMERICAL"
        )

        self.assertEqual(
            proposal.verification_type,
            "NUMERICAL",
        )

    def test_generator_requires_verification_type(self):
        inference = lambda prompt: (
            "Question: Calculate exp(-1).\n"
            "Expected Answer: 0.367879"
        )

        generator = LearningExerciseGenerator(inference)

        with self.assertRaises(ValueError):
            generator.generate(
                "The exponential function is used in decay models."
            )


if __name__ == "__main__":
    unittest.main()
