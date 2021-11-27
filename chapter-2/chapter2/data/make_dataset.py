# -*- coding: utf-8 -*-
import pathlib
import click
from dotenv import find_dotenv, load_dotenv
import os
import pandas as pd
from sklearn import model_selection
from chapter2.conf import datasources, DataDirectory
import logging


logger = logging.getLogger(__name__)

def _save_path(root_data_dir, data_subdir, name):
    save_path = pathlib.Path(root_data_dir).joinpath(data_subdir).joinpath(name)
    return save_path

def save_data(dataframe, root_data_dir, data_subdir: DataDirectory, name):
    save_path = _save_path(root_data_dir, data_subdir.value, name)
    logger.info(f"saving {name} dataframe to {save_path}")
    dataframe.rename_axis("index").to_csv(save_path)
    return

def load_data(root_data_dir, data_subdir: DataDirectory, name):
    save_path = _save_path(root_data_dir, data_subdir.value, name)
    return pd.read_csv(save_path)

def train_test_split(dataframe):
    train, test = model_selection.train_test_split(dataframe, test_size=0.2, random_state=0)
    return train, test


@click.command()
@click.argument('data_root_dir', type=click.Path(exists=True))
def make_dataset(data_root_dir):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    logger.info('making final data set from raw data')

    housing_path = datasources.get_data("housing")
    housing = pd.read_csv(housing_path)
    train, test = train_test_split(housing)
    save_data(train, data_root_dir, DataDirectory.INTERIM, "housing_train.csv")
    save_data(test, data_root_dir, DataDirectory.INTERIM, "housing_test.csv")

if __name__ == '__main__':


    load_dotenv(find_dotenv())

    make_dataset()
