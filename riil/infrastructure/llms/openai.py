# riil/infrastructure/llms/openai.py
import os
from typing import Dict, Any
from openai import AsyncOpenAI
from riil.infrastructure.llms.base import LLM
from riil.domain.types import Inputs, Outputs


class OpenAIStep(LLM):
    def __init__(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        output_key: str = "output"
    ):
        if not prompt:
            raise ValueError("prompt is required")
        self.prompt = prompt
        self.model = model
        self.output_key = output_key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENAI_API_KEY not set")
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def run(self, inputs: Inputs) -> Outputs:
        try:
            # ✅ Safe formatting
            formatted_prompt = self.prompt.format(**inputs)
        except KeyError as e:
            raise ValueError(f"Missing input for prompt: {e}")
        except Exception as e:
            raise ValueError(f"Failed to format prompt: {str(e)}")

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": formatted_prompt}]
        )
        content = response.choices[0].message.content
        return {
            "output": content,
            "output_key": self.output_key
        }


# ✅ Factory function — must use config["prompt"]
def create_openai_step(config: dict) -> OpenAIStep:
    """
    Factory for OpenAIStep from config.
    Called by resolver.
    """
    prompt = config.get("prompt")
    if not prompt:
        raise ValueError("Missing 'prompt' in OpenAIStep config")

    return OpenAIStep(
        prompt=prompt,
        model=config.get("model", "gpt-3.5-turbo"),
        output_key=config.get("output_key", "output")
    )


# ✅ Register it
from riil.infrastructure.llms.resolver import register_step_type
register_step_type("openai", create_openai_step)