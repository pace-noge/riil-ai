# riil/config/schema.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class LLMSpec(BaseModel):
    provider: str
    model: str
    config: Dict[str, Any] = Field(default_factory=dict)


class StepSpec(BaseModel):
    prompt: str
    rules: List[str] = Field(default_factory=list)
    llm: LLMSpec
    output_key: str = "output"


class WorkflowSpec(BaseModel):
    name: str
    description: str = ""
    author: Optional[str] = None
    version: str = "0.1.0"
    tags: List[str] = Field(default_factory=list)
    steps: List[StepSpec]
