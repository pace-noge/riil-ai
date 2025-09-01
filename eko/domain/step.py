# eko/domain/step.py
"""
Abstract base class for all executable steps.
"""

from abc import ABC
from typing import Dict, Any


class Step(ABC):
    """
    Abstract base class for any executable step in a workflow.
    All steps must implement `run`.
    """
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement run()")
