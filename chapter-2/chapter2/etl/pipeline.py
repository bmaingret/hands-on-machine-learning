"""Define the preprocessing pipeline that will create data files
usable to build features."""

import logging

from chapter2 import conf, etl

logger = logging.getLogger(__name__)


def run():
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """

    logger.info("prep data set from raw data for feature building")

    housing_path = conf.datasources.get_data("housing")
    housing = etl.io.load_data(housing_path)
    train, test = etl.preprocessing.train_test_split(housing)

    train_save_path = etl.io.get_path(
        data_subdir=conf.DataDirectory.INTERIM, filename="housing_train.csv"
    )
    etl.io.save_data(dataframe=train, path=train_save_path)

    test_save_path = etl.io.get_path(
        data_subdir=conf.DataDirectory.INTERIM, filename="housing_test.csv"
    )
    etl.io.save_data(dataframe=test, path=test_save_path)

    etl.preprocessing.clean(train)
    train_cleaned_path = etl.io.get_path(
        data_subdir=conf.DataDirectory.INTERIM, filename="housing_train_prepared.csv"
    )
    etl.io.save_data(dataframe=train, path=train_cleaned_path)


if __name__ == "__main__":
    run()
