# riil/domain/workflow.py
import uuid
from typing import List
from .step import Step
from .types import Inputs, Outputs
from riil.core.callback import Callback


class Workflow:
    def __init__(self, name: str, callbacks: List[Callback] = None):
        self.name = name
        self.steps: List[Step] = []
        self.callbacks = callbacks or []

    def add_step(self, step: Step):
        self.steps.append(step)
        return self

    async def run(self, inputs: Inputs) -> Outputs:
        # Add trace context
        context = inputs.copy()
        context["__trace_id"] = str(uuid.uuid4())

        # Notify start
        for cb in self.callbacks:
            await cb.on_workflow_start(self, inputs)

        for step in self.steps:
            # Add step context
            step_id = str(uuid.uuid4())
            context["__step_id"] = step_id

            for cb in self.callbacks:
                await cb.on_step_start(step, context, context)

            try:
                result = await step.run(context)
                output_key = getattr(step, "output_key", "output")
                context[output_key] = result["output"]

                for cb in self.callbacks:
                    await cb.on_step_end(step, result, context)
            except Exception as e:
                for cb in self.callbacks:
                    await cb.on_error(step, e, context)
                raise

        # Notify end
        for cb in self.callbacks:
            await cb.on_workflow_end(self, context)

        return context
