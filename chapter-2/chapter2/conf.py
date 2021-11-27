from enum import Enum
from pathlib import Path
from chapter2.data.datasources import Datasources

def get_project_dir():
    return Path(__file__).resolve().parents[1]

class DataDirectory(Enum):
    RAW = "raw"
    INTERIM = "interim"
    PROCESSED = "processed"

ROOT_DATA_DIR = get_project_dir().joinpath("data")
RAW_DATA_DIR = ROOT_DATA_DIR.joinpath(DataDirectory.RAW.value)

datasources = Datasources(data_dir=RAW_DATA_DIR)
datasources.add_datasource(
    name = "housing",
    download_url= "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.tgz",
    download_filename = "housing.tgz",
    output_filename = "housing.csv")
