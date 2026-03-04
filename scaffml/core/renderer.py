from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from typing import Dict


def render_template_file(template_path: Path, output_path: Path, context: Dict) -> None:
    """
    Render a Jinja2 template to a target file.

    Args:
        template_path (Path): Path to the .j2 template file.
        output_path (Path): Path where the rendered file will be written.
        context (dict): Dictionary of variables to pass into the template.

    Behavior:
        - Creates parent directories of output_path if they do not exist.
        - Overwrites the file if it already exists.
        - Supports nested directories for templates.
    """
    # Ensure template exists
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    # Setup Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=False,  # For code files, autoescape is typically off
        keep_trailing_newline=True
    )

    # Load and render the template
    template: Template = env.get_template(template_path.name)
    content: str = template.render(context)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write rendered content safely with UTF-8 encoding
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)