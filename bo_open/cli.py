from pathlib import Path
import os
import sys
import subprocess
import typer
import yaml
from rich.console import Console

app = typer.Typer()
console = Console(file=sys.stderr)

PROJECTS_FILE = Path.home() / ".config" / "bo" / "projects.txt"

"""
TODO: Move these helper functions to their own modules within bo_core
"""

RESET = "\x1b[0m"
FG_GREEN = "\x1b[32m"
FG_YELLOW = "\x1b[33m"
FG_RED = "\x1b[31m"
FG_CYAN = "\x1b[36m"
FG_MAGENTA = "\x1b[35m"
FG_BLUE = "\x1b[34m"

def color(text: str, fg: str) -> str:
    return f"{fg}{text}{RESET}"

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
        console.print(f"[red]Error parsing {tmuxp_file.name}:[/red] {e}")
        return project_path.name

    if isinstance(data, dict):
        name = data.get("session_name") or data.get("session-name")
        if not name is None:
            return name.strip()

    return project_path.name

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

def format_github_status(project_path: Path) -> str:
    """
    Return a short github status string for display in fzf.
    """
    return "\u2713 github" if project_has_github_remote(project_path) else "\u2715 github"

def project_has_github_remote(project_path: Path) -> bool:
    """
    Return true if path has a git remote URL.
    """
    if not project_is_git_repo(project_path):
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

@app.command()
def main(
    
    sessions_only: bool = typer.Option(
        False,
        "--sessions-only",
        "-s",
        help="Show only projects with an active tmux session.",
        )
):
    """List and select registered projects via fzf."""

    if not PROJECTS_FILE.exists():
        console.print(f"[red]No project registry found at {PROJECTS_FILE}[/red]")
        console.print("[yellow]Run bo_setup to initialize project registry[/yellow]")
        raise typer.Exit(1)

    with PROJECTS_FILE.open("r") as f:
        raw_projects = [line.strip() for line in f if line.strip()]

    if not raw_projects:
        console.print("[yellow]No projects found in registry.[/yellow]")
        console.print("[yellow]Run bo_setup to initialize project registry[/yellow]")
        console.print("[yellow]Run bo_add to create a new project[/yellow]")
        raise typer.Exit(0)

    projects = sorted(set(raw_projects), key=lambda s: s.lower())

    if projects != raw_projects:
       console.print("[dim]Sorting project registry...[/dim]")
       with PROJECTS_FILE.open("w") as f:
           f.write("\n".join(projects) + "\n")
    
    if sessions_only:
        filtered: list[str] = []

        for proj in projects:
            project_path = Path(proj).expanduser().resolve()
            if project_has_tmux_session(project_path):
                filtered.append(str(project_path))

        projects = filtered

        if not projects:
            console.print("[yellow]No projects with active tmux sessions found.[/yellow]")
            raise typer.Exit(0)

    status_list = []
    for proj in projects:
        project_path = Path(proj)
        label = project_path.name
        tmux  = format_tmux_status(project_path)
        git   = format_git_status(project_path)
        github= format_github_status(project_path)
    
        status_list.append((proj, label, tmux, git, github))

    width_label = max(len(s[1]) for s in status_list)
    width_tmux  = max(len(s[2]) for s in status_list)
    width_git   = max(len(s[3]) for s in status_list)
    width_github= max(len(s[4]) for s in status_list)

    rows = []
    for proj, label, tmux, git, github in status_list:
        if "\u25CF" in tmux:
            tmux_form = color(tmux, FG_GREEN)
        else:
            tmux_form = color(tmux, FG_BLUE)
        if "\u2713" in git:
            git_form = color(git, FG_GREEN)
        elif "\u00B1" in git:
            git_form = color(git, FG_RED)
        else:
            git_form = color(git, FG_YELLOW)
        if "\u2713" in github:
            github_form = color(github, FG_GREEN)
        else:
            github_form = color(github, FG_YELLOW)

        line = (
            f"{label:<{width_label}}    "
            f"{tmux_form:<{width_tmux}}    "
            f"{git_form:<{width_git}}    "
            f"{github_form:<{width_github}}    "
            f"{proj}    "
        )
        rows.append(line)

    result = subprocess.run(
        [
            "fzf",
            "--ansi",
            "--prompt=Select project > ", 
            "--height=40%", 
            "--reverse",
            "--delimiter=\t"
        ],
        input = "\n".join(rows),
        text = True,
        capture_output = True,
    )

    selection = result.stdout.strip()
    if not selection:
        console.print("[dim]No project selected.[/dim]")
        return
#    console.print(f"[green]Selected: [/green] {selection}")
    parts = selection.split()
    raw_path = parts[7]
    project_path = Path(raw_path).resolve()
    
    """
    TODO: I see a possible refactor with the below 15 lines to use the 
    project_has_tmux_session function to prevent code duplication.
    """

    tmuxp_file_yaml = project_path / ".tmuxp.yaml"
    tmuxp_file_yml = project_path / ".tmuxp.yml"

    if tmuxp_file_yaml.exists() or tmuxp_file_yml.exists():
        tmuxp_file = tmuxp_file_yaml if tmuxp_file_yaml.exists() else tmuxp_file_yml
#        console.print(f"[blue]Found tmuxp config: [/blue] {tmuxp_file}")
       
        session_name = get_tmux_session_name(tmuxp_file, project_path)
#        console.print(f"[dim]tmux session name:[/dim] {session_name}") 
        
        has_session = subprocess.run(
            ["tmux", "has-session", "-t", session_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            )
        
        inside_tmux = "TMUX" in os.environ
        
        if has_session.returncode == 0:
#            console.print("[green]Session already running.[/green]")
            if inside_tmux:
#                console.print("[dim]Switching tmux session...[/dim]")
                subprocess.run(["tmux", "switch-client", "-t", session_name])
            else:
#                console.print("[dim]Attaching to tmux session...[/dim]")
                subprocess.run(["tmux", "attach-session", "-t", session_name])

        else:
#            console.print("[green]Launching tmux session...[/green]")
            subprocess.run(["tmuxp", "load", str(tmuxp_file)])

    else:
        console.print(f"[yellow]No .tmuxp.yaml found in {project_path}[/yellow]")
        print(project_path, end="")

if __name__ == "__main__":
    app()
