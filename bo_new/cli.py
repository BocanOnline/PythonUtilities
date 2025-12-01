
from pathlib import Path
import os
import sys
import subprocess
import typer
import yaml
from rich.console import Console

app = typer.Typer()
console = Console(file=sys.stderr)

@app.command()
def main():
    console.print("[green]bo-new test[/green]")

if __name__ == "__main__":
    app()
