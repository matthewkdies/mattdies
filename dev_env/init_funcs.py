import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


@dataclass(slots=True)
class EnvLine:
    """Handles the name and value of a line in the env files."""
    name: str = field(default_factory=str)
    value: str = field(default_factory=str)

    @classmethod
    def from_str(cls, env_line: str) -> "EnvLine":
        """Creates an EnvLine from a string.

        Args:
            env_line (str): A line from the env file.

        Returns:
            EnvLine: An EnvLine object based on the string.
        """
        name, value = env_line.split("=")
        logger.debug("Env line=\"%s\", name=\"%s\", value=\"%s\".", env_line, name, value)
        return EnvLine(name=name, value=value)


@dataclass(slots=True)
class EnvFile:
    """Handles the lines and path of an env file."""
    env_lines: list[EnvLine]
    path: Path

    @classmethod
    def from_filepath(cls, env_filepath: Path) -> "EnvFile":
        """Gets an EnvFile object from an env file path.

        Args:
            env_filepath (Path): The path to the env file.

        Returns:
            EnvFile: An EnvFile object.
        """
        with env_filepath.open("r", encoding="utf-8") as infile:
            env_lines = [EnvLine.from_str(line.strip()) for line in infile.readlines()]
        logger.debug("Env lines=%s.", env_lines)
        return EnvFile(env_lines=env_lines, path=env_filepath)

    def add_env_vars(self, env_vars: dict[str, str]) -> None:
        """Adds environment variables to the env file.

        Args:
            env_vars (dict[str, str]): A dictionary mapping names to values of env vars.
        """
        existing_names = [env_line.name for env_line in self.env_lines]
        for name, value in env_vars.items():
            if name in existing_names:
                logger.info("Overwriting env var \"%s\" to \"%s\".", name, value)
                old_env_line = [env_line for env_line in self.env_lines if env_line.name == name][0]
                self.env_lines.remove(old_env_line)
            env_line = EnvLine(name=name, value=value)
            self.env_lines.append(env_line)
            logger.debug("Added env line=%s", env_line)

    def __to_str(self) -> str:
        """Converts the env file to a string for writing.

        Returns:
            str: A string representation of the env file.
        """
        out_str = str()
        for env_line in self.env_lines:
            out_str += f"{env_line.name.upper()}={env_line.value}\n"
        return out_str

    def write_env_file(self) -> None:
        """Writes the env file."""
        with self.path.open("w", encoding="utf-8") as outfile:
            outfile.write(self.__to_str())


def write_env_file(project_name: str, env_vars: Optional[dict[str,str]] = None) -> None:
    """Ensures an env file exists with the minimum required value.

    Args:
        project_name (str): The name of the current project.
        env_vars (Optional[dict[str,str]], optional): Env vars to add to the file. Defaults to None.
    """
    # sets the env vars to add
    min_env_vars = {"PROJECT": project_name}
    if not env_vars:
        env_vars = min_env_vars
    env_vars.update(min_env_vars)

    # get or create env file
    env_filepath = (Path(__file__).parent / ".env").resolve()
    if not env_filepath.exists():
        env_filepath.touch()

    # updates env file accordingly
    env_file = EnvFile.from_filepath(env_filepath)
    env_file.add_env_vars(env_vars)
    env_file.write_env_file()


def main(workspace_path: str) -> None:
    """Does all of the necessary functions as an init command before building container.

    Args:
        workspace_path (str): The path to the 'workspace' directory within the project.
    """
    project_name = Path(workspace_path).stem.lower()
    write_env_file(project_name)


if __name__ == "__main__":
    main(" ".join(sys.argv[1:]))
