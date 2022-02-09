"""Defines data directory structures and sources, and env variables
"""

import logging
import os
import pathlib
from enum import Enum

import dotenv

from chapter2.etl.datasources import Datasources

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


class DataDirectory(Enum):
    """Enum for intermediate data directories"""

    RAW = "raw"
    INTERIM = "interim"
    PROCESSED = "processed"


load_dotenv()
ROOT_DATA_DIR = pathlib.Path(os.getenv("ROOT_DATA_DIR"))

datasources = Datasources(data_dir=ROOT_DATA_DIR.joinpath(DataDirectory.RAW.value))
datasources.add_datasource(
    name="housing",
    download_url="https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.tgz",
    download_filename="housing.tgz",
    output_filename="housing.csv",
)
