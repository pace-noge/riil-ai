# eko/usecases/execute_workflow.py
"""
Use case: Execute a workflow with inputs.
"""

from typing import Dict, Any
from riil.domain.workflow import Workflow


async def execute_workflow(workflow: Workflow, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a workflow and return the final context.
    Can be extended with logging, observability, etc.
    """
    return await workflow.run(inputs)
