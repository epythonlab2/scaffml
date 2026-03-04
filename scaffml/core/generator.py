import yaml
import sys
from pathlib import Path
from importlib import resources
from typing import Dict, Any
from scaffml.core.renderer import render_template_file
from rich.console import Console
console = Console()

class ProjectGenerator:
    """
    Generates a professional ML project scaffold based on a YAML-defined
    structure and Jinja2 templates.

    Attributes:
        project_name (str): The name of the project (as provided by user).
        features (dict): Optional feature flags (e.g., {"docker": True}).
        pkg_name (str): Sanitized Python package name derived from project_name.
        base_path (Path): The root path where the project will be created.
        template_root (Path): Path to the project templates within the package.
    """

    def __init__(self, project_name: str, features: Dict[str, Any] | None = None):
        """
        Initialize the ProjectGenerator.

        Args:
            project_name (str): Name of the ML project.
            features (dict, optional): Feature flags such as Docker support.
        """
        self.project_name = project_name
        self.features = features or {}

        # Sanitize for Python package imports
        self.pkg_name = project_name.lower().replace("-", "_").replace(" ", "_")

        self.base_path = Path.cwd() / project_name

        # Resolve template path from installed package or local development
        try:
            self.template_root = resources.files("scaffml") / "templates" / "ml_project"
        except Exception:
            self.template_root = Path(__file__).resolve().parent.parent / "templates" / "ml_project"

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _check_collision(self) -> None:
        """
        Checks if the target project folder already exists and is non-empty.
        Exits if it does to avoid overwriting.
        """
        if self.base_path.exists() and any(self.base_path.iterdir()):
            console.print(f"[bold red]❌ Error:[/bold red] Directory '{self.project_name}' already exists and is not empty.")
            sys.exit(1)


    # ------------------------------------------------------------------
    # Structure Generation
    # ------------------------------------------------------------------

    def generate_structure(self, structure: Dict[str, Any], current_path: Path) -> None:
        """
        Recursively creates directories and blank files for the project
        based on the YAML-defined structure. Skips files that are rendered
        via Jinja templates.

        Args:
            structure (dict): Nested dictionary defining folders and files.
            current_path (Path): Current directory path for recursion.
        """
        for name, content in structure.items():
            # Replace any dynamic placeholders in directory names
            actual_name = name.replace("{{project_name}}", self.pkg_name)
            path = current_path / actual_name

            if isinstance(content, dict):
                # Create directory
                path.mkdir(parents=True, exist_ok=True)

                if not content:
                    # Preserve empty directories in Git
                    (path / ".gitkeep").touch()
                else:
                    # Recursively generate nested directories/files
                    self.generate_structure(content, path)
            else:
                # Ensure parent directories exist
                path.parent.mkdir(parents=True, exist_ok=True)

                # Skip file creation if a corresponding Jinja template exists
                rel_path = path.relative_to(self.base_path)
                template_path = self.template_root / "files" / f"{rel_path}.j2"
                if not template_path.exists():
                    path.touch(exist_ok=True)  # Create blank file (e.g., __init__.py)

    # ------------------------------------------------------------------
    # Template Rendering
    # ------------------------------------------------------------------

    def generate_files(self) -> None:
        """
        Renders all .j2 templates found in the /files directory into the
        project folder, replacing placeholders with the project name and feature flags.
        """
        files_src = self.template_root / "files"
        if not files_src.exists():
            return  # No templates to render

        for template_file in files_src.rglob("*.j2"):
            # Relative path inside files/ directory
            rel_path = template_file.relative_to(files_src)

            # Replace placeholders in the output file path
            output_str = str(rel_path).replace("{{project_name}}", self.pkg_name)
            output_path = self.base_path / Path(output_str).with_suffix("")

            # Skip Dockerfile if Docker feature is not enabled
            if "Dockerfile" in str(rel_path) and not self.features.get("docker"):
                continue

            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Render template with context
            render_template_file(
                template_file,
                output_path,
                {
                    "project_name": self.project_name,
                    "pkg_name": self.pkg_name,
                    "include_docker": self.features.get("docker", False)
                }
            )

    # ------------------------------------------------------------------
    # Main Generation Entry Point
    # ------------------------------------------------------------------

    def generate(self) -> None:
        """
        Main entry point for project generation. Performs validation,
        creates the folder structure, and renders all templates.
        """
        self._check_collision()
        console.print(f"\n[bold blue]🚀 scaffml:[/bold blue] Building [cyan]{self.project_name}[/cyan]...")

        self.base_path.mkdir(parents=True, exist_ok=True)
        structure_path = self.template_root / "structure.yaml"

        try:
            with open(structure_path, "r", encoding="utf-8") as f:
                structure = yaml.safe_load(f)
        except Exception as e:
            console.print(f"[bold red]❌ Error loading structure.yaml:[/bold red] {e}")
            sys.exit(1)

        try:
            self.generate_structure(structure, self.base_path)
            self.generate_files()
            console.print(f"[bold green]✨ Success![/bold green] Project created at: [underline]{self.base_path.resolve()}[/underline]")
        except Exception as e:
            console.print(f"[bold red]❌ Error during project generation:[/bold red] {e}")
            sys.exit(1)