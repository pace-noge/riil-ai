# eko/interface/cli.py
"""
CLI interface for eko-py.
Automatically loads .env file for local development.
"""
from typing import List

import typer
import asyncio
import os
from dotenv import load_dotenv  # ← Add this
from pathlib import Path

from riil.domain.workflow import Workflow
from riil.infrastructure.llms.openai import OpenAIStep
from riil.usecases.execute_workflow import execute_workflow
from riil.infrastructure.workflow.loader import load_workflow_from_yaml

# Load .env file if it exists (development only)
if os.path.exists(".env"):
    load_dotenv(override=True)

app = typer.Typer()


@app.command()
def run_joke(topic: str = "AI"):
    """Run joke workflow."""
    wf = Workflow("joke")
    wf.add_step(OpenAIStep("Tell me a joke about {topic}", output_key="joke"))
    try:
        result = asyncio.run(execute_workflow(wf, {"topic": topic}))
        typer.echo("\n" + result["joke"] + "\n")
    except Exception as e:
        typer.echo(f"❌ Error: {str(e)}", err=True)


@app.command()
def version():
    """Show version."""
    typer.echo("eko-py v0.1.0 (M1)")


@app.command()
def run(
    file: Path,
    inputs: List[str] = typer.Argument(None, help="Inputs in key=value format")
):
    """
    Run a workflow from YAML file.
    Accepts: key=value or --key=value
    """
    if not file.exists():
        typer.echo(f"❌ Workflow not found: {file}")
        raise typer.Exit(1)

    # Parse key=value or --key=value
    parsed_inputs = {}
    if inputs:
        for item in inputs:
            if "=" not in item:
                typer.echo(f"❌ Invalid input format: {item}. Use key=value")
                raise typer.Exit(1)
            # Strip leading -- if present
            if item.startswith("--"):
                item = item[2:]
            k, v = item.split("=", 1)
            parsed_inputs[k] = v

    try:
        wf = load_workflow_from_yaml(file)
        result = asyncio.run(execute_workflow(wf, parsed_inputs))
        typer.echo("\n" + result["output"] + "\n")
    except Exception as e:
        typer.echo(f"❌ Error: {str(e)}", err=True)
        raise typer.Exit(1)

@app.command()
def stream(
    file: Path,
    **inputs: str
):
    """Stream a workflow's output token by token."""
    if not file.exists():
        typer.echo(f"❌ Workflow not found: {file}")
        raise typer.Exit(1)
    try:
        wf = load_workflow_from_yaml(file)
        typer.echo("💬 Streaming response...\n")
        async def _stream():
            async for token in wf.stream(inputs):
                print(token, end="", flush=True)
            print()
        asyncio.run(_stream())
    except Exception as e:
        typer.echo(f"❌ Error: {str(e)}", err=True)

@app.command()
def list_workflows(
    dir: Path = Path("workflows")
):
    """List all available workflows."""
    if not dir.exists():
        typer.echo("📁 No workflows/ directory")
        return
    typer.echo("📄 Available Workflows:")
    for yml in sorted(dir.rglob("*.yaml")):
        rel = yml.relative_to(dir.parent if dir.parent.exists() else Path("."))
        typer.echo(f"  {rel}")

@app.command()
def import_workflow(
    file: Path,
    dest_dir: Path = Path("workflows/imported")
):
    """Import a shared workflow."""
    if not file.exists():
        typer.echo(f"❌ File not found: {file}")
        raise typer.Exit(1)
    dest_dir.mkdir(exist_ok=True, parents=True)
    dest = dest_dir / file.name
    dest.write_text(file.read_text())
    typer.echo(f"✅ Imported {file.name} to {dest_dir}/")


if __name__ == "__main__":
    app()