# eko/infrastructure/utils/json_repair.py
"""
Lightweight JSON repair for malformed LLM outputs.
"""

import re
import json
from typing import Any


def repair_json(text: str) -> str:
    """
    Attempt to repair common JSON syntax errors.
    Inspired by json-repair, simplified for core use.
    """
    # Remove text before first { and after last }
    first = text.find("{")
    last = text.rfind("}")
    if first == -1 or last == -1:
        raise ValueError("No JSON object found")
    text = text[first : last + 1]

    # Fix missing commas
    text = re.sub(r'"\s*"', '","', text)
    text = re.sub(r'}\s*{', '},{', text)
    text = re.sub(r']\s*\[', '],[', text)
    text = re.sub(r'}\s*"', '}, "', text)
    text = re.sub(r']\s*"', '], "', text)

    # Fix trailing commas
    text = re.sub(r',(\s*[}\]])', r'\1', text)

    # Ensure strings are quoted
    text = re.sub(r':\s*([A-Za-z0-9_]+)([,\}\]])', r': "\1"\2', text)

    return text
