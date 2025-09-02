# eko/domain/step.py
"""
Abstract base class for all executable steps.
"""

from abc import ABC
from typing import Dict, Any, AsyncGenerator

Inputs = Dict[str, Any]
Outputs = Dict[str, Any]
OutputStream = AsyncGenerator[str, None]


class Step(ABC):
    """
    Abstract base class for any executable step in a workflow.
    All steps must implement `run`.
    """
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement run()")

    async def stream(self, inputs: Inputs) -> OutputStream:
        """
        Default implementation: run and yield full output.
        Override in LLM steps for token-by-token streaming.
        """
        result = await self.run(inputs)
        yield result["output"]
