"""A collection of function calls that I generally use and wish were a bit simpler."""

from pathlib import Path


def path_parents(path: Path) -> list[Path]:
    """Gets the `list(path.parents) value.

    Args:
        path (Path): A Path object.

    Returns:
        list[Path]: A list of the path object's parents.
    """
    return list(path.parents)
    