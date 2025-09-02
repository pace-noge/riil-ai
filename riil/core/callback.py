# riil/core/callback.py
"""
Abstract base class for observability callbacks.
Supports logging, tracing, metrics, alerts.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Callback(ABC):
    """
    Base class for observability hooks.
    Users can implement their own for logging, tracing, etc.
    """

    @abstractmethod
    async def on_step_start(self, step, inputs: Dict[str, Any], context: Dict[str, Any]):
        """Called before step runs."""
        pass

    @abstractmethod
    async def on_step_end(self, step, outputs: Dict[str, Any], context: Dict[str, Any]):
        """Called after step completes."""
        pass

    @abstractmethod
    async def on_error(self, step, error: Exception, context: Dict[str, Any]):
        """Called if step raises an exception."""
        pass

    async def on_workflow_start(self, workflow, inputs: Dict[str, Any]):
        """Optional: called at start."""
        pass

    async def on_workflow_end(self, workflow, outputs: Dict[str, Any]):
        """Optional: called at end."""
        pass