from pathlib import Path

def create_directory(path: Path) -> None:
    """
    Safely create a directory and all its parent directories if they do not exist.

    Args:
        path (Path): The directory path to create.

    Behavior:
        - If the directory already exists, nothing happens.
        - Creates all parent directories as needed.
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(f"Failed to create directory '{path}': {e}")