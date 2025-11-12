from pathlib import Path
import os
import sys
import subprocess
import typer
from rich.console import Console

app = typer.Typer()
console = Console(file=sys.stderr)

PROJECTS_FILE = Path.home() / ".config" / "bo" / "projects.txt"

@app.command()
def main():
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

    result = subprocess.run(
        ["fzf", "--prompt=Select project > ", "--height=40%", "--reverse"],
        input = "\n".join(projects),
        text = True,
        capture_output = True,
    )

    selection = result.stdout.strip()

    if not selection:
        console.print("[dim]No project selected.[/dim]")
        return

    console.print(f"[green]Selected: [/green] {selection}")

    project_path = Path(selection)
    tmuxp_file_yaml = project_path / ".tmuxp.yaml"
    tmuxp_file_yml = project_path / ".tmuxp.yml"

    if tmuxp_file_yaml.exists() or tmuxp_file_yml.exists():
        tmuxp_file = tmuxp_file_yaml if tmuxp_file_yaml.exists() else tmuxp_file_yml
        console.print(f"[blue]Found tmuxp config: [/blue] {tmuxp_file}")
        console.print("[green]Launching tmux session...[/green/]")

        inside_tmux = "TMUX" in os.environ

        cmd = ["tmuxp", "load", str(tmuxp_file)]
        if inside_tmux:
            cmd += ["--yes"]

        subprocess.run(cmd)

    else:
        console.print(f"[yellow]No .tmuxp.yaml found in {project_path}[/yellow]")
        print(project_path, end="")

if __name__ == "__main__":
    app()
