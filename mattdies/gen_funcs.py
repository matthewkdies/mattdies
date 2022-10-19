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


def get_login() -> tuple[str, str]:
    """Gets system user and pwd.

    Returns:
        tuple[str, str]: System user and pwd.
    """
    with Path("secrets/user").open("r",encoding="utf-8") as pwd_infile:
        user = pwd_infile.read()
    with Path("secrets/pwd").open("r",encoding="utf-8") as pwd_infile:
        pwd = pwd_infile.read()
    return user, pwd
