# eko/domain/prompt.py
"""
Safe prompt templating with rule injection support.
"""

from string import Template
from typing import List


class Prompt:
    """
    Represents a prompt template that can be formatted with inputs.
    Supports optional rule injection for role/tone/format.
    """

    def __init__(self, template: str, rule_names: List[str] = None):
        if not template:
            raise ValueError("Prompt template cannot be None or empty")
        self.template = Template(template)
        self.rule_names = rule_names or []

    def format(self, inputs: dict) -> str:
        """
        Format the prompt with inputs.
        Rule injection is handled externally.
        """
        return self.template.substitute(**inputs)
