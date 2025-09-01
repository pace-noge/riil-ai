# tests/test_infrastructure/test_openai.py
"""Test OpenAIStep with schema and repair."""
import pytest
from unittest.mock import AsyncMock, patch
from pydantic import BaseModel
from eko.infrastructure.llms.openai import OpenAIStep


class TestSchema(BaseModel):
    name: str
    value: int


@pytest.mark.asyncio
@patch("openai.AsyncOpenAI")
async def test_openai_step_with_schema_valid(mock_client):
    mock_response = AsyncMock()
    mock_response.choices[0].message.content = '{"name": "test", "value": 42}'
    mock_client.return_value.chat.completions.create.return_value = mock_response

    with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        step = OpenAIStep("test", output_schema=TestSchema)
        result = await step.run({})
        assert result["output"]["name"] == "test"
        assert result["output"]["value"] == 42


@pytest.mark.asyncio
@patch("openai.AsyncOpenAI")
async def test_openai_step_repair_json(mock_client):
    mock_response = AsyncMock()
    mock_response.choices[0].message.content = '{"name": "test", "value": 42'
    mock_client.return_value.chat.completions.create.side_effect = [
        mock_response,  # first call: malformed
        mock_response,  # retry
    ]

    with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        step = OpenAIStep("test", output_schema=TestSchema, max_retries=1)
        result = await step.run({})
        assert "repaired" in result
