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

def format_tmux_status(project_path: Path) -> str:
    """
    Return a short tmux status string for display in fzf.
    """
    if project_has_tmux_session(project_path):
        return "\u25CF tmux"
    else:
        return "\u25CB tmux"

def project_has_tmux_session(project_path: Path) -> bool:
    """
    console.print("[green]bo-new test[/green]")
    Return True if there is an active tmux session associated with this project.
    Uses project directory name if no set session name.
    """
    tmuxp_file_yaml = project_path / ".tmuxp.yaml"
    tmuxp_file_yml = project_path / ".tmuxp.yml"

    if tmuxp_file_yaml.exists() or tmuxp_file_yml.exists():
        tmuxp_file = tmuxp_file_yaml if tmuxp_file_yaml.exists() else tmuxp_file_yml
#        console.print(f"[blue]Found tmuxp config: [/blue] {tmuxp_file}")
       
        session_name = get_tmux_session_name(tmuxp_file, project_path)
    else:
        session_name = project_path.name

#    console.print(f"[dim]tmux session name:[/dim] {session_name}")  
    has_session = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        )

    return has_session.returncode == 0 
    
def get_tmux_session_name(tmuxp_file: Path, project_path: Path) -> str:
    """
    Read the tmuxp config and return the session name.
    Uses project directory name if no set session name.
    """

    try:
        data = yaml.safe_load(tmuxp_file.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        bocan.console.print(f"[red]Error parsing {tmuxp_file.name}:[/red] {e}")
        return project_path.name

    if isinstance(data, dict):
        name = data.get("session_name") or data.get("session-name")
        if not name is None:
            return name.strip()

    return project_path.name
