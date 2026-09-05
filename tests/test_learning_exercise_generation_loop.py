import unittest

from runtime.learning_exercise_generation_loop import (
    LearningExerciseGenerationLoop,
)


class FakeGenerator:
    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = 0

    def generate(self, knowledge):
        self.calls += 1

        output = self.outputs.pop(0)

        if isinstance(output, Exception):
            raise output

        return output


class FakeRunner:
    def __init__(self, results):
        self.results = list(results)
        self.calls = 0

    def run(self, spec, answer):
        self.calls += 1
        return self.results.pop(0)


class TestLearningExerciseGenerationLoop(unittest.TestCase):

    def test_successful_generation_returns_result(self):
        generator = FakeGenerator([
            "SPEC",
        ])

        runner = FakeRunner([
            type(
                "Result",
                (),
                {
                    "passed": True,
                    "reason": "ANSWER_CORRECT",
                },
            )(),
        ])

        loop = LearningExerciseGenerationLoop(
            generator=generator,
            runner=runner,
            max_attempts=3,
        )

        result = loop.run(
            knowledge="test knowledge",
            answer="test answer",
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.attempts, 1)
        self.assertEqual(result.reason, "ANSWER_CORRECT")
        self.assertEqual(generator.calls, 1)
        self.assertEqual(runner.calls, 1)

    def test_generation_failure_retries(self):
        generator = FakeGenerator([
            ValueError("INVALID_LEARNING_EXERCISE_SPEC"),
            "SPEC",
        ])

        runner = FakeRunner([
            type(
                "Result",
                (),
                {
                    "passed": True,
                    "reason": "ANSWER_CORRECT",
                },
            )(),
        ])

        loop = LearningExerciseGenerationLoop(
            generator=generator,
            runner=runner,
            max_attempts=3,
        )

        result = loop.run(
            knowledge="test knowledge",
            answer="test answer",
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.attempts, 2)
        self.assertEqual(result.reason, "ANSWER_CORRECT")
        self.assertEqual(generator.calls, 2)

    def test_max_attempts_stops_loop(self):
        generator = FakeGenerator([
            ValueError("INVALID_LEARNING_EXERCISE_SPEC"),
            ValueError("INVALID_LEARNING_EXERCISE_SPEC"),
            ValueError("INVALID_LEARNING_EXERCISE_SPEC"),
        ])

        runner = FakeRunner([])

        loop = LearningExerciseGenerationLoop(
            generator=generator,
            runner=runner,
            max_attempts=3,
        )

        result = loop.run(
            knowledge="test knowledge",
            answer="test answer",
        )

        self.assertFalse(result.accepted)
        self.assertEqual(result.attempts, 3)
        self.assertEqual(
            result.reason,
            "MAX_ATTEMPTS_REACHED",
        )
        self.assertEqual(generator.calls, 3)
        self.assertEqual(runner.calls, 0)

    def test_failed_answer_retries_generation(self):
        generator = FakeGenerator([
            "SPEC",
            "SPEC",
        ])

        runner = FakeRunner([
            type(
                "Result",
                (),
                {
                    "passed": False,
                    "reason": "ANSWER_INCORRECT",
                },
            )(),
            type(
                "Result",
                (),
                {
                    "passed": True,
                    "reason": "ANSWER_CORRECT",
                },
            )(),
        ])

        loop = LearningExerciseGenerationLoop(
            generator=generator,
            runner=runner,
            max_attempts=3,
        )

        result = loop.run(
            knowledge="test knowledge",
            answer="test answer",
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.attempts, 2)
        self.assertEqual(result.reason, "ANSWER_CORRECT")
        self.assertEqual(generator.calls, 2)
        self.assertEqual(runner.calls, 2)


if __name__ == "__main__":
    unittest.main()
