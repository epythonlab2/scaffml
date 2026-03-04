import typer
from scaffml.core.generator import ProjectGenerator
from importlib import metadata
from rich import print
from rich.console import Console

console = Console()

app = typer.Typer(
    help="scaffml – Professional ML Project Structure Generator",
    no_args_is_help=True,
    add_completion=False
)

# -----------------------------
# Version command
# -----------------------------
@app.command()
def version():
    """Show the current scaffml version."""
    try:
        v = metadata.version("scaffml")
        print(f"[bold cyan]scaffml v{v}[/bold cyan]")
    except Exception:
        console.print("[bold red]❌ Unable to determine scaffml version[/bold red]")


# -----------------------------
# Create command
# -----------------------------
@app.command("create")
def create(
    name: str = typer.Argument(..., help="Name of the ML project"),
    docker: bool = typer.Option(False, "--docker", "-d", help="Include Docker support")
):
    """
    Create a new ML project with an optional Docker setup.
    """
    generator = ProjectGenerator(
        project_name=name,
        features={"docker": docker}
    )

    try:
        generator.generate()
        console.print(f"\n✅ Project [bold blue]'{name}'[/bold blue] created successfully!\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]\n")
        raise typer.Exit(code=1)


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    app()