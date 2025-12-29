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
import bocan.core as bocan

@bocan.app.command()
def main():
    bocan.console.print("[green]bo-new test[/green]")

if __name__ == "__main__":
    bocan.app()
