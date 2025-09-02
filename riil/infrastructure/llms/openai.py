# eko/infrastructure/llms/openai.py
"""
OpenAIStep with schema validation, JSON repair, and retry.
"""

import os
import asyncio
from typing import Optional
from pydantic import BaseModel
from openai import AsyncOpenAI
from eko.infrastructure.llms.base import LLM
from eko.infrastructure.utils.json_repair import repair_json
from eko.domain.types import Inputs, Outputs


class OpenAIStep(LLM):
    """
    Step that calls OpenAI with optional output schema enforcement.
    Features:
    - Schema validation
    - JSON repair
    - Retry on parse failure
    """

    def __init__(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        output_schema: Optional[type[BaseModel]] = None,
        max_retries: int = 1,
        output_key: str = "output"
    ):
        self.prompt = prompt
        self.model = model
        self.output_schema = output_schema
        self.max_retries = max_retries
        self.output_key = output_key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENAI_API_KEY not set")
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def run(self, inputs: Inputs) -> Outputs:
        """Execute step with schema handling."""
        formatted_prompt = self.prompt.format(**inputs)

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": formatted_prompt}]
                )
                raw_output = response.choices[0].message.content

                if self.output_schema:
                    # Try direct parse
                    try:
                        parsed = self.output_schema.model_validate_json(raw_output)
                        return {
                            "output": parsed.model_dump(),
                            "raw_output": raw_output,
                            "validated": True
                        }
                    except:
                        # Try repair
                        try:
                            fixed = repair_json(raw_output)
                            parsed = self.output_schema.model_validate_json(fixed)
                            return {
                                "output": parsed.model_dump(),
                                "raw_output": raw_output,
                                "repaired": True
                            }
                        except Exception as e:
                            if attempt >= self.max_retries:
                                raise ValueError(f"Failed to parse/repair JSON after {attempt+1} attempts: {str(e)}")
                            # Retry with correction prompt
                            formatted_prompt = (
                                f"The following output is invalid JSON:\n{raw_output}\n"
                                "Please return only valid JSON matching the expected structure."
                            )
                            await asyncio.sleep(0.1)
                            continue
                else:
                    return {"output": raw_output}

            except Exception as e:
                if attempt >= self.max_retries:
                    raise
                await asyncio.sleep(0.1)
                continue

        raise RuntimeError("Unreachable")
