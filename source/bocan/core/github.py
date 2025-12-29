#standard library
from pathlib import Path
import subprocess

#vendor library

#project library
import bocan.core as bocan


def format_github_status(project_path: Path) -> str:
    """
    Return a short github status string for display in fzf.
    """
    return "\u2713 github" if project_has_github_remote(project_path) else "\u2715 github"

def project_has_github_remote(project_path: Path) -> bool:
    """
    Return true if path has a git remote URL.
    """
    if not bocan.project_is_git_repo(project_path):
        return False
    result = subprocess.run(
        [
            "git",
            "-C",
            str(project_path),
            "remote",
            "-v"
        ],
        capture_output = True,
        text = True
    )

    for line in result.stdout.splitlines():
        if "github.com" in line:
            return True

    return False 
