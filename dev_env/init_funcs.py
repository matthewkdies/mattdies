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


DEFAULT_ENV: dict[str, str] = {"PROJECT_NAME"}

@dataclass(slots=True)
class EnvLine:
    name: str = field(default_factory=str)
    value: str = field(default_factory=str)

    @classmethod
    def from_str(self, env_line: str) -> "EnvLine":
        name, value = env_line.split("=")
        logger.debug("Env line=\"%s\", name=\"%s\", value=\"%s\".", env_line, name, value)
        return EnvLine(name=name, value=value)
    

@dataclass(slots=True)
class EnvFile:
    env_lines: list[EnvLine]
    path: Path

    @classmethod
    def from_filepath(self, env_filepath: Path) -> "EnvFile":
        with env_filepath.open("r", encoding="utf-8") as infile:
            env_lines = [EnvLine.from_str(line.strip()) for line in infile.readlines()]
        logger.debug("Env lines=%s.", env_lines)
        return EnvFile(env_lines=env_lines, path=env_filepath)
    
    def add_env_vars(self, env_vars: dict[str, str]) -> None:
        existing_names = [env_line.name for env_line in self.env_lines]
        for name, value in env_vars.items():
            if name in existing_names:
                logger.info("Overwriting env var \"%s\" to \"%s\".", name, value)
                previous_env_line = [env_line for env_line in self.env_lines if env_line.name == name][0]
                self.env_lines.remove(previous_env_line)
            env_line = EnvLine(name=name, value=value)
            self.env_lines.append(env_line)
            logger.debug("Added env line=%s", env_line)

    def to_str(self) -> str:
        out_str = str()
        for env_line in self.env_lines:
            out_str += f"{env_line.name.upper()}={env_line.value}\n"
        return out_str

    def write_env_file(self) -> None:
        with self.path.open("w", encoding="utf-8") as outfile:
            outfile.write(self.to_str())


def write_env_file(project_name: str, env_vars: Optional[dict[str,str]] = None) -> None:
    min_env_vars = {"PROJECT": project_name}
    if not env_vars:
        env_vars = min_env_vars
    env_vars.update(min_env_vars)
    env_filepath = (Path(__file__).parent / ".env").resolve()
    if not env_filepath.exists():
        env_filepath.touch()
    env_file = EnvFile.from_filepath(env_filepath)
    env_file.add_env_vars(env_vars)
    env_file.write_env_file()


def main(workspace_path: str) -> None:
    project_name = Path(workspace_path).stem.lower()
    write_env_file(project_name)


if __name__ == "__main__":
    main(" ".join(sys.argv[1:]))
