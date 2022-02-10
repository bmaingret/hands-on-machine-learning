"""Helpers io functions"""

import logging
import pathlib

import pandas as pd

logger = logging.getLogger(__name__)


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
