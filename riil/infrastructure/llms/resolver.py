# eko/infrastructure/llms/resolver.py
"""
Registry for dynamic step resolution.
"""

from typing import Callable, Dict
from riil.domain.step import Step

_step_factories: Dict[str, Callable] = {}


def register_step_type(name: str, factory: Callable):
    """Register a step factory."""
    _step_factories[name] = factory


def resolve_step(provider: str, config: dict) -> Step:
    """Resolve provider to step."""
    if provider not in _step_factories:
        raise ValueError(f"Unknown provider: {provider}")
    return _step_factories[provider](config)