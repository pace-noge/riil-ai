# riil/infrastructure/callbacks/resolver.py
"""
Registry for callback types used in YAML.
"""

from typing import Dict, Callable, Any

_callback_factories: Dict[str, Callable] = {}


def register_callback(name: str, factory: Callable[[Dict[str, Any]], 'Callback']):
    """
    Register a callback factory.
    Can be used in YAML workflows.
    """
    _callback_factories[name] = factory


def resolve_callback(config: Dict[str, Any]) -> 'Callback':
    """
    Create a callback from config.
    """
    cb_type = config["type"]
    if cb_type not in _callback_factories:
        raise ValueError(f"Unknown callback type: {cb_type}")
    return _callback_factories[cb_type](config.get("config", {}))
