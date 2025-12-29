#standard library
from pathlib import Path
import os
import sys
import subprocess

#vendor library
import daemon
import typer
import yaml
from rich.console import Console

#project library
import bocan.core as bocan


def main():
    bocan.console.print("[green]bo-update test[/green]")

if __name__ == "__main__":
    bocan.app()


#- [ ] Run in the background to keep project registry data up-to-date.
#- [ ] Maintain project registry by removing invalid entries.
#- [ ] Check if project tmux session is currently open.
#- [ ] Check git status.
#- [ ] Check synchronization between local and remote repositories.
