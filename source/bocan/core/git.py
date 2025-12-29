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


def format_git_status(project_path: Path) -> str:
    """
    Return a short git status string for display in fzf.
    """
    if not project_is_git_repo(project_path):
        return "? git"

    result = subprocess.run(
        [
            "git",
            "-C",
            str(project_path),
            "status",
            "--porcelain"
        ],
        capture_output = True,
        text = True
    )

    if result.stdout.strip():
        return "\u00B1 git"
    else:
        """
        empty output means clean working tree
        """
        return "\u2713 git"

def project_is_git_repo(project_path: Path) -> bool:
    """
    Return true if path is inside a Git repository.
    """
    result = subprocess.run(
        [
            "git",
            "-C",
            str(project_path),
            "rev-parse",
            "--is_inside_worktree"
        ],
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL
    )
    return result.returncode == 0

