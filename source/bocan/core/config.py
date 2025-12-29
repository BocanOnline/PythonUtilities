#standard library
from pathlib import Path
import os
import sys
import subprocess

#vendor library
import typer
import yaml
from rich.console import Console

#project library


app = typer.Typer()
console = Console(file=sys.stderr)

registry_path = Path.home() / ".config" / "bo" / "bo-registry.yaml"
backlog_path  = Path.home() / ".config" / "bo" / "bo-backlog.yaml"

RESET = "\x1b[0m"
FG_GREEN = "\x1b[32m"
FG_YELLOW = "\x1b[33m"
FG_RED = "\x1b[31m"
FG_CYAN = "\x1b[36m"
FG_MAGENTA = "\x1b[35m"
FG_BLUE = "\x1b[34m"

def color(text: str, fg: str) -> str:
    return f"{fg}{text}{RESET}"

def config():
    console.print("[green]bo-core config() test[/green]")
