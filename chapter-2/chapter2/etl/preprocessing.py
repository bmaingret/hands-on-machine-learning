# -*- coding: utf-8 -*-
"""Defines the initial preprocessing/cleaning step from the raw files."""

import logging

import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.impute import SimpleImputer

logger = logging.getLogger(__name__)


def train_test_split(housing: pd.DataFrame):
    """Split our data and return one train DataFrame and one test DataFrame
    containing both X and y.

    Args:
        housing (pd.DataFrame): [description]

    Returns:
        [type]: [description]
    """
    housing_y = housing["median_house_value"]
    housing_x = housing.drop(["median_house_value"], axis=1)
    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        housing_x,
        housing_y,
        test_size=0.2,
        random_state=0,
        stratify=housing["ocean_proximity"],
    )
    logger.debug(y_train.shape)
    logger.debug(x_train.shape)
    return pd.concat([x_train, y_train], axis=1), pd.concat([x_test, y_test], axis=1)


def _impute(housing: pd.DataFrame):
    imputer = SimpleImputer(strategy="median")
    numerical_columns = [
        col for col in housing.columns if housing[col].dtype in ["int64", "float64"]
    ]
    housing[numerical_columns] = imputer.fit_transform(housing[numerical_columns])


def _drop_500k(housing: pd.DataFrame):
    housing_len = housing.shape[0]
    house_value_500k_index = housing[housing["median_house_value"] > 500000].index

    housing.drop(index=house_value_500k_index, inplace=True)
    logger.info(f"500k cutoff: {housing_len-housing.shape[0]} records removed")


def _drop_outliers(housing: pd.DataFrame):
    housing_len = housing.shape[0]

    rooms_per_household = housing["total_rooms"] / housing["households"]
    rooms_per_household_cutoff = np.percentile(rooms_per_household, 99.99)
    rooms_per_household_mask = rooms_per_household < rooms_per_household_cutoff

    bedrooms_room_ratio = housing["total_bedrooms"] / housing["total_rooms"]
    bedrooms_room_ratio_cutoff = 1
    bedrooms_room_ratio_mask = bedrooms_room_ratio < bedrooms_room_ratio_cutoff

    # Careful we want to drop when mask is False, so we negate it
    drop_index = housing.index[~rooms_per_household_mask | ~bedrooms_room_ratio_mask]
    housing.drop(index=drop_index, inplace=True)
    logger.info(f"outliers: {housing_len-housing.shape[0]} records removed")


def clean(housing: pd.DataFrame):
    """Modifiy housing **in place**"""
    _impute(housing)
    _drop_500k(housing)
    _drop_outliers(housing)
