from __future__ import annotations

import subprocess
from pathlib import Path

TV_SHOW_DIRS = [Path("/volume1/TV Shows"), Path("/volume2/TV Shows2")]
MOVIE_DIRS = [Path("/volume1/Movies"), Path("/volume2/Movies2")]
PARSED_MOVIES_PATH = Path("/volume2/Other/parsed_movies.txt")
PARSED_EPS_PATH = Path("/volume2/Other/parsed_eps.txt")


class SubRemovalException(Exception):
    """An exception class for the removal of subtitles failing."""


def check_files(parsed_movies_path: Path, parsed_eps_path: Path) -> None:
    if not parsed_movies_path.exists():
        raise SubRemovalException(f"The {parsed_movies_path=} does not exist!")
    if not parsed_eps_path.exists():
        raise SubRemovalException(f"The {parsed_eps_path=} does not exist!")


def get_movies(parsed_movies_path: Path) -> list(Path):
    with parsed_movies_path.open("r", encoding="utf-8") as infile:
        parsed_movies = [line for line in infile.readlines() if line]
    movies = []
    for movie_dir in MOVIE_DIRS:
        for movie in movie_dir.glob("**/*.mkv"):
            movie_str = str(movie)
            if movie_str not in parsed_movies and "#recycle" not in movie_str:
                movies.append(movie.absolute())
    return movies


def get_tv_episodes(parsed_eps_path: Path) -> list(Path):
    with parsed_eps_path.open("r", encoding="utf-8") as infile:
        parsed_eps = [line for line in infile.readlines() if line]
    tv_episodes = []
    for tv_show_dir in TV_SHOW_DIRS:
        for tv_episode in tv_show_dir.glob("**/*.mkv"):
            ep_str = str(tv_episode)
            if tv_episode not in parsed_eps and "#recycle" not in ep_str:
                tv_episodes.append(tv_episode.absolute())
    return tv_episodes


def remove_movie_subs(movie_paths: list[Path], parsed_movies_path: Path) -> None:
    for movie_path in movie_paths:
        subprocess.run(
            [
                "/usr/local/bin/mkvmerge",
                "-o",
                "temp.mkv",
                "--no-subtitles",
                str(movie_path),
            ],
            check=True,
            shell=False,
        )
        movie_path.unlink()
        Path("temp.mkv").rename(str(movie_path))
        with parsed_movies_path.open("a", encoding="utf-8") as outfile:
            outfile.write(f"{movie_path}\n")


def remove_tv_eps_subs(episode_paths: list[Path], parsed_eps_path: Path) -> None:
    for episode_path in episode_paths:
        subprocess.run(
            [
                "/usr/local/bin/mkvmerge",
                "-o",
                "temp.mkv",
                "--no-subtitles",
                str(episode_path),
            ],
            check=True,
            shell=False,
        )
        episode_path.unlink()
        Path("temp.mkv").rename(str(episode_path))
        with parsed_eps_path.open("a", encoding="utf-8") as outfile:
            outfile.write(f"{episode_path}\n")


def main() -> None:
    movies_to_process = get_movies(PARSED_MOVIES_PATH)
    episodes_to_process = get_tv_episodes(PARSED_EPS_PATH)
    remove_movie_subs(movies_to_process, PARSED_MOVIES_PATH)
    remove_tv_eps_subs(episodes_to_process, PARSED_EPS_PATH)


if __name__ == "__main__":
    main()
