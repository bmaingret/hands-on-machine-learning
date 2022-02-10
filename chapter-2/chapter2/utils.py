"""Defines data directory structures and sources, and env variables
"""

import logging
import pathlib

import dotenv

logger = logging.getLogger(__name__)


def project_dir():
    """Helper function that return the project directory path/

    Returns:
        pathlib.Path: directory path
    """
    return pathlib.Path(__file__).resolve().parents[1]


def load_dotenv():
    """Helper function to load .env file."""
    dotenv.load_dotenv(dotenv.find_dotenv())


def build_path(root_data_dir: str, data_subdir: str, filename: str) -> pathlib.Path:
    """Construct a path from a DataSources subdir and a filename.
    Default will use the root directory from conf.

    Args:
        data_subdir (conf.DataDirectory): subdirectory, as defined in conf.DataDirectory
        filename (str): [description]
        root_data_dir (str): [description].

    Returns:
        pathlib.Path: [description]
    """
    save_path = pathlib.Path(root_data_dir).joinpath(data_subdir).joinpath(filename)
    return save_path
