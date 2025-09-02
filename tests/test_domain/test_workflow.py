# tests/test_domain/test_workflow.py
"""Test Workflow class."""
import pytest
from riil.domain.workflow import Workflow
from riil.domain.step import Step


class MockStep(Step):
    def __init__(self, output):
        self.output = output

    async def run(self, inputs):
        return {"output": self.output}


@pytest.mark.asyncio
async def test_workflow_runs_sequentially():
    wf = Workflow("test")
    wf.add_step(MockStep("hello"))
    wf.add_step(MockStep("world"))
    result = await wf.run({})
    assert result["output"] == "world"
    assert result.get("step0_output") is None


@pytest.mark.asyncio
async def test_workflow_maintains_context():
    class ContextStep(Step):
        async def run(self, inputs):
            return {"output": inputs.get("topic", "none")}
    wf = Workflow("ctx")
    wf.add_step(ContextStep())
    result = await wf.run({"topic": "test"})
    assert result["output"] == "test"
