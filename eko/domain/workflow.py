# eko/domain/workflow.py
"""
Workflow engine that orchestrates a sequence of steps.
"""

from typing import List
from eko.domain.step import Step
from eko.domain.types import Inputs, Outputs


class Workflow:
    """
    A sequence of steps executed in order.
    Maintains context between steps.
    """

    def __init__(self, name: str):
        self.name = name
        self.steps: List[Step] = []

    def add_step(self, step: Step):
        """Add a step to the workflow."""
        self.steps.append(step)
        return self

    async def run(self, inputs: Inputs) -> Outputs:
        """
        Execute all steps in sequence.
        Each step's output is merged into the context.
        """
        context = inputs.copy()
        for step in self.steps:
            result = await step.run(context)
            output_key = getattr(step, "output_key", "output")
            context[output_key] = result["output"]
        return context
