"""Build features required by the model."""

import numpy as np
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def make_preprocessor():
    """ "Create an sklearn pipeline used to prepare and build the feature"""
    numeric_pipeline = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
    categorical_pipeline = make_pipeline(OneHotEncoder())
    preprocessor = make_column_transformer(
        (numeric_pipeline, make_column_selector(dtype_include=np.number)),
        (categorical_pipeline, ["ocean_proximity"]),
        remainder="passthrough",
    )

    return preprocessor
