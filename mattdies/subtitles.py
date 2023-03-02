import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from py_opensubtitles.open_subtitles import OpenSubtitles


logger = logging.getLogger(__name__)
logging.basicConfig()


MOVIES_DIR = Path("/Movies")
TV_SHOWS_DIR = Path("/TV Shows")
SUPPORTED_FORMATS = [".asf", ".avi", ".mov", ".mp4", ".mpeg", ".mpegts", ".ts", ".mkv", ".wmv", ]


@dataclass
class Movie:
    dir_path: Path
    movie_path: Path
    has_subtitles: bool


@dataclass
class TVShowSeason:
    dir_path: Path
    episode_paths: list[Path]
    has_all_subtitles: bool


@dataclass
class TVShow:
    dir_path: Path
    seasons: list[TVShowSeason]


def get_movies(movies_dir: Optional[Path] = MOVIES_DIR) -> list[Movie]:
    movies = []
    for movie_dir_path in movies_dir.glob("*/"):
        if not movie_dir_path.is_dir() or movie_dir_path.name == "#recycle":
            continue
        cur_movie_files = movie_dir_path.glob("*.*")
        has_subtitles = any(filepath.suffix == ".srt" for filepath in cur_movie_files)
        movie_paths = [filepath for filepath in cur_movie_files if filepath.suffix.lower() in SUPPORTED_FORMATS]
        if len(movie_paths) != 1:
            logger.warning("Multiple movie files detected for %s. Choosing the first file.", movie_dir_path.name)
        movie_path = movie_paths[0]
        movies.append(
            Movie(
                dir_path=movie_dir_path,
                movie_path=movie_path,
                has_subtitles=has_subtitles
            )
        )
    return movies


def get_movie_subtitles(movie: Movie, open_subs: OpenSubtitles) -> None:
    # query_data = {
    #     "sublanguageid": "en",
    #     "query": movie.movie_path.name,
    #     "moviebytesize": movie_file.size,
    # }
    subtitle_data = open_subs.get_subtitle_file_info(movie.movie_path, "en")
    # subtitle_id = subtitle_data[0].get('IDSubtitleFile')
    # subtitle_path = ost.download_subtitles([subtitle_id], output_directory=str(movie.dir_path), extension="srt")[subtitle_id]
    # os.rename(subtitle_path, movie.movie_path.with_suffix(".srt"))


def get_tv_show_subtitles(tv_show: TVShow, open_subs: OpenSubtitles) -> None:
    ...


def get_subtitles(movies: list[Movie], tv_shows: list[TVShow]) -> None:
    open_subs = OpenSubtitles()
    open_subs.login()
    for movie in movies:
        get_movie_subtitles(movie, open_subs)
    for tv_show in tv_shows:
        get_tv_show_subtitles(tv_show, open_subs)


if __name__ == "__main__":
    MOVIES = get_movies(Path("/media/matthewkdies/easystore/Media/Movies"))
    get_subtitles(MOVIES, [])
