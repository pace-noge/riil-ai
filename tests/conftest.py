# tests/conftest.py
"""pytest fixtures."""
import pytest


@pytest.fixture
def sample_inputs():
    return {"topic": "Python"}
