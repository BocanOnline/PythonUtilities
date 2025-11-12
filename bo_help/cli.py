from pathlib import Path
import sys
import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

app = typer.Typer()
console = Console(file=sys.stderr)

def find_developer_md(start_dir: Path | None = None) -> Path | None:
    """Search upward from current directory for DEVELOPER.md"""
    current = start_dir or Path.cwd()

    for parent in [current, *current.parents]:
        candidate = parent / "DEVELOPER.md"
        if candidate.exists():
            return candidate

    return None

def parse_developer_md(path: Path) -> tuple[dict, str]:
    """Split YAML front matter and markdown body"""
    text = path.read_text(encoding="utf-8").strip()

    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    yaml_block = parts[1].strip()
    markdown_body = parts[2].strip()

    try:
        metadata = yaml.safe_load(yaml_block) or {}
    except yaml.YAMLError as e:
        console.print(f"[red]yaml parsing error in {path.name}:[/red] {e}")
        metadata = {}

    return metadata, markdown_body

def render_help(metadata: dict, body: str):
    """Render the parsed metadata and body with rich formatting"""
    project_name = metadata.get("project", "Unknown Project")
    description = metadata.get("description", "")
    language = metadata.get("language", "")
    environment = metadata.get("environment", "")
    requires = metadata.get("requires", [])
    startup = metadata.get("startup", [])
    other = metadata.get("other", [])

    title = []
    title.append(f"[bold cyan]Project: {project_name}[/bold cyan]\nDescription: {description}\n")

    if language:
        title.append(f"[cyan]Language: [/cyan]{language}")

    if environment:
        title.append(f"[cyan]Development Environment: [/cyan]{environment}")

    guide = "\n".join(title)
   
    if requires:
        guide += "\n[cyan]Requires:[/cyan] " + ", ".join(requires)
   
    if startup:
        guide += "\n\n[bold green]Startup Commands:\n[/bold green]" 
        for line in startup:
            parts = line.split("--")
            cmd = parts[0].strip()
            desc = f"[dim] {parts[1].strip()}\n[/dim]"
            guide += "".join(cmd) + "".join(desc)

    if other:
        guide += "\n[bold yellow]Other Commands:\n[/bold yellow]" 
        for line in other:
            parts = line.split("--")
            cmd = parts[0].strip()
            desc = f"[dim] {parts[1].strip()}\n[/dim]"
            guide += "".join(cmd) + "".join(desc)

    console.print(
        Panel(guide, title="Developer Guide", expand=False, border_style="cyan")
    )

#    if body.strip():
#        console.rule("[bold cyan]Markdown Body[/bold cyan]")
#        md = Markdown(body)
#        with console.pager():
#            console.print(md)

@app.command()
def main():
    """Locate the DEVELOPER.md file for the current project."""
    path = find_developer_md()

    if not path:
        console.print("[red]No DEVELOPER.md found for this project.[/red]")
        raise typer.Exit(1)
    
    metadata, body = parse_developer_md(path)
    render_help(metadata, body)   

    raise typer.Exit(0)

if __name__ == "__main__":
    app()
