# eko/interface/cli.py
"""
CLI interface for eko-py.
Automatically loads .env file for local development.
"""

import typer
import asyncio
import os
from dotenv import load_dotenv  # ← Add this

from eko.domain.workflow import Workflow
from eko.infrastructure.llms.openai import OpenAIStep
from eko.usecases.execute_workflow import execute_workflow

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

if __name__ == "__main__":
    app()