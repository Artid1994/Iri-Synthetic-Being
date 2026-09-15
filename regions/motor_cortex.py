"""
Motor cortex region implementation.

Specialized for action planning and execution.
"""
from brain.population import NeuronPopulation
from config.anatomy_settings import MOTOR_CORTEX


class MotorCortex:
    """
    Motor cortex: action planning and motor commands.

    Activated when decisions produce actions.
    """

    def __init__(self):
        self.population = NeuronPopulation(MOTOR_CORTEX)
        self.region_name = MOTOR_CORTEX.name
        self.neuron_count = MOTOR_CORTEX.neuron_count

        # Track action executions
        self._action_count = 0

    def execute_action(self, action_type: str) -> bool:
        """
        Execute an action (activates neurons).

        Args:
            action_type: Type of action

        Returns:
            True if executed
        """
        import numpy as np

        # Activate motor neurons for action
        chunk_index = 0
        activation = np.ones(MOTOR_CORTEX.chunk_size, dtype=np.float32) * 0.8
        self.population.step_chunk(chunk_index, activation)

        self._action_count += 1
        return True

    @property
    def action_count(self) -> int:
        """Number of actions executed."""
        return self._action_count
