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
def main(
    
    sessions_only: bool = typer.Option(
        False,
        "--sessions-only",
        "-s",
        help="Show only projects with an active tmux session.",
        )
):
    """Open and parse projects registry file."""
    
    if not bocan.registry_path.exists():
        bocan.console.print(f"[red]No project registry found at {bocan.registry_path}[/red]")
        raise typer.Exit(1)

    raw_list = []
    formatted_list = []
    
    with open(bocan.registry_path, 'r') as registry:
        projects = yaml.safe_load_all(registry)
        
        for project in projects:
            path = project['path']
            name = project['name']
            git_status = project['git status']
            github_status = project['github status']
            github_remote = project['github remote']
            github_remote_url = project['github remote url']
            tmux_status = project['tmux status']
            language = project['language']
            framework = project['framework']
            build_system = project['build system']
            interface = project['interface']          

            raw_list.append((name, language, framework, tmux_status, git_status, github_status, path))

    width_name          = max(len(r[0]) for r in raw_list)
    width_language      = max(len(r[1]) for r in raw_list)
    width_framework     = max(len(r[2]) for r in raw_list)
    #width_interface     = max(len(r[3]) for r in raw_list)
    #width_build_system  = max(len(r[4]) for r in raw_list)
    width_tmux_status   = max(len(r[3]) for r in raw_list)
    width_git_status    = max(len(r[4]) for r in raw_list)
    width_github_status = max(len(r[5]) for r in raw_list)
    
    for name, language, framework, tmux_status, git_status, github_status, path in raw_list:
        
        line = (
            f"{name:<{width_name}}    "
            f"{language:<{width_language}}    "
            f"{framework:<{width_framework}}    "
            #f"{interface:<{width_interface}}    "
            #f"{build_system:<{width_build_system}}    "
            f"{tmux_status:<{width_tmux_status}}    "
            f"{git_status:<{width_git_status}}    "
            f"{github_status:<{width_github_status}}    "
            f"{path}    "
        )
        
        formatted_list.append(line)
        

        """

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

        """

    result = subprocess.run(
        [
            "fzf",
            "--ansi",
            "--prompt=Select project > ", 
            "--height=60%", 
            "--reverse",
            "--delimiter=\t"
        ],
        input = "\n".join(formatted_list),
        text = True,
        capture_output = True,
    )

    selection = result.stdout.strip()
    if not selection:
        bocan.console.print("[dim]No project selected.[/dim]")
        return
    #console.print(f"{selection}") 

    parts = selection.split()
    raw_path = parts[-1]
    project_path = Path(raw_path).resolve()
    #console.print(f"[green]Selected: [/green] {project_path}")

    tmuxp_file_yaml = project_path / ".tmuxp.yaml"
    tmuxp_file_yml = project_path / ".tmuxp.yml"

    #console.print(f"{tmuxp_file_yaml}")

    if tmuxp_file_yaml.exists() or tmuxp_file_yml.exists():
        tmuxp_file = tmuxp_file_yaml if tmuxp_file_yaml.exists() else tmuxp_file_yml
#        console.print(f"[blue]Found tmuxp config: [/blue] {tmuxp_file}")
       
        session_name = bocan.get_tmux_session_name(tmuxp_file, project_path)
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
        bocan.console.print(f"[yellow]No .tmuxp.yaml found in {project_path}[/yellow]")
        print(project_path)
    
if __name__ == "__main__":
    bocan.app()
