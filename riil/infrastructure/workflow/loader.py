# riil/infrastructure/workflow/loader.py
"""
Loads and validates workflows from YAML/JSON files.
Maps configuration to executable Workflow objects.
"""

from pathlib import Path
import yaml
from typing import Dict, Any
from pydantic import ValidationError

from riil.config.schema import WorkflowSpec, StepSpec
from riil.domain.workflow import Workflow
from riil.infrastructure.llms.resolver import resolve_step


def load_workflow_from_yaml(path: Path) -> Workflow:
    """
    Load a workflow from a YAML file and return an executable Workflow instance.

    The YAML must match the WorkflowSpec schema:
    - name: string
    - steps: list of step specs with prompt, llm.provider, etc.

    Raises:
        ValueError: If file is invalid, missing, or config is malformed
        IOError: If file cannot be read
    """
    if not path.exists():
        raise ValueError(f"Workflow file not found: {path}")

    try:
        raw_text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw_text)
        if not data:
            raise ValueError("YAML file is empty")

        # Validate against schema
        spec = WorkflowSpec.model_validate(data)

        # Create workflow
        wf = Workflow(spec.name)

        # Load and add each step
        for idx, step_spec in enumerate(spec.steps):
            step_config = _build_step_config(step_spec, path, idx)
            try:
                llm_step = resolve_step(step_spec.llm.provider, step_config)
                wf.add_step(llm_step)
            except Exception as e:
                raise ValueError(f"Failed to create step {idx} with provider '{step_spec.llm.provider}': {str(e)}") from e

        return wf

    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax in {path}: {str(e)}") from e
    except ValidationError as e:
        raise ValueError(f"Workflow validation error in {path}: {e}") from e
    except Exception as e:
        if "Workflow file not found" not in str(e):
            raise ValueError(f"Failed to load workflow from {path}: {str(e)}") from e
        raise


def _build_step_config(step_spec: StepSpec, source_path: Path, step_index: int) -> Dict[str, Any]:
    """
    Build the configuration dictionary for resolve_step.
    Extracts prompt, model, output_key, and provider-specific config.
    """
    if not step_spec.prompt or not step_spec.prompt.strip():
        raise ValueError(f"Step {step_index} in {source_path} is missing or empty 'prompt' field")

    if not step_spec.llm.provider:
        raise ValueError(f"Step {step_index} in {source_path} is missing 'llm.provider'")

    if not step_spec.llm.model:
        raise ValueError(f"Step {step_index} in {source_path} is missing 'llm.model'")

    return {
        "prompt": step_spec.prompt,
        "model": step_spec.llm.model,
        "output_key": step_spec.output_key,
        "config": step_spec.llm.config
    }