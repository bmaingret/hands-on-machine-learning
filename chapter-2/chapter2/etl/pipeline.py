"""Define the preprocessing pipeline that will create data files
usable to build features."""

import logging
import os
import pathlib

from chapter2 import utils
from chapter2.etl import io, preprocessing
from chapter2.etl.datasources import DataDirectory, Datasources

logger = logging.getLogger(__name__)


def run():
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """

    logger.info("prep data set from raw data for feature building")

    utils.load_dotenv()
    root_data_dir = pathlib.Path(os.getenv("ROOT_DATA_DIR"))

    datasources = Datasources(data_dir=root_data_dir.joinpath(DataDirectory.RAW.value))
    datasources.add_datasource(
        name="housing",
        download_url="https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.tgz",
        download_filename="housing.tgz",
        output_filename="housing.csv",
    )

    housing_path = datasources.get_data("housing")
    housing = io.load_data(housing_path)
    train, test = preprocessing.train_test_split(housing)

    train_save_path = utils.build_path(
        root_data_dir=root_data_dir,
        data_subdir=DataDirectory.INTERIM.value,
        filename="housing_train.csv",
    )
    io.save_data(dataframe=train, path=train_save_path)

    test_save_path = utils.build_path(
        root_data_dir=root_data_dir,
        data_subdir=DataDirectory.INTERIM.value,
        filename="housing_test.csv",
    )
    io.save_data(dataframe=test, path=test_save_path)

    preprocessing.clean(train)
    train_cleaned_path = utils.build_path(
        root_data_dir=root_data_dir,
        data_subdir=DataDirectory.INTERIM.value,
        filename="housing_train_prepared.csv",
    )
    io.save_data(dataframe=train, path=train_cleaned_path)


if __name__ == "__main__":
    run()
