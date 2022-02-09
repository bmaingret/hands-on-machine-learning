"""Helpers io functions"""

import logging
import pathlib

import pandas as pd

from chapter2 import conf

logger = logging.getLogger(__name__)


def get_path(
    data_subdir: conf.DataDirectory,
    filename: str,
    root_data_dir=conf.ROOT_DATA_DIR,
) -> pathlib.Path:
    """Construct a path from a DataSources subdir and a filename.
    Default will use the root directory from conf.

    Args:
        data_subdir (conf.DataDirectory): subdirectory, as defined in conf.DataDirectory
        filename (str): [description]
        root_data_dir ([type], optional): [description]. Defaults to conf.ROOT_DATA_DIR.

    Returns:
        pathlib.Path: [description]
    """
    save_path = (
        pathlib.Path(root_data_dir).joinpath(data_subdir.value).joinpath(filename)
    )
    return save_path


def save_data(dataframe: pd.DataFrame, path: pathlib.Path):
    """Save dataframe to root_data_dir into a subdirectory specified by data_subdir

    Args:
        dataframe (pd.DataFrame): [description]
        root_data_dir (str): [description]
        data_subdir (conf.DataDirectory): [description]
        name (str): [description]
    """
    logger.info(f"saving dataframe to {path}")
    dataframe.rename_axis("index").to_csv(path)


def load_data(path: pathlib.Path) -> pd.DataFrame:
    """Load csv data from a data directory and return a DataFrame

    Args:
        root_data_dir (str): [description]
        data_subdir (conf.DataDirectory): [description]
        name (str): [description]

    Returns:
        pd.DataFrame: [description]
    """
    return pd.read_csv(path)
