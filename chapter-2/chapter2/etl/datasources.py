"""Define helpers to manage the datasource for this project.
    A datasource is made of a name, a download URL, a download filename
    and an output filename.
    The Datasources class allows to create datasource, retrieve data
"""

import logging
import os
import pathlib
import tarfile
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

import requests

logger = logging.getLogger(__name__)


class DataDirectory(Enum):
    """Enum for intermediate data directories"""

    RAW = "raw"
    INTERIM = "interim"
    PROCESSED = "processed"


@dataclass(frozen=True)
class Datasource:
    """Datasource is made of:
    * a name that describe it
    * a download url where the data can be downloaded programmatically
    * a filename that will downloaded
    * an output filename used to save the file
    """

    name: str
    download_url: str
    download_filename: str
    output_filename: str


@dataclass
class Datasources:
    """Manage datasources, and allow to download. Basic caching functionnality.

    Raises:
        ValueError: When adding a new datasource with a name that already exists.
    """

    data_dir: pathlib.Path
    datasources: Dict[str, Datasource] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)

    def add_datasource(
        self, name: str, download_url: str, download_filename: str, output_filename: str
    ) -> None:
        """Add a datasource if it doesn't already exists.

        Args:
            name (str): datasource name
            download_url (str): datasource download URL
            download_filename (str): datasource download filename
            output_filename (str): datasource output filename

        Raises:
            ValueError: If a datasource with name==name already exists
        """
        if name in self.datasources:
            raise ValueError("name already exists")

        self.datasources[name] = Datasource(
            name=name,
            download_url=download_url,
            download_filename=download_filename,
            output_filename=output_filename,
        )

    def get_datasource(self, name: str) -> Datasource:
        """Return a datasource object. No checks are done, will raise an error.

        Args:
            name (str): name of the datasource

        Returns:
            Datasource: datasource object
        """
        return self.datasources[name]

    def get_data(self, name: str) -> pathlib.Path:
        """Download data if required, and return a pathlib object pointing to
        the saved data.

        Args:
            name (str): datasource name

        Returns:
            pathlib.Path: pathlib path to downloaded datasource
        """
        datasource = self.get_datasource(name)
        self._download_data(datasource)
        return self._target_file_path(datasource)

    def _target_file_path(self, datasource) -> pathlib.Path:
        return self.data_dir.joinpath(datasource.output_filename)

    def _download_path(self, datasource) -> pathlib.Path:
        return self.data_dir.joinpath(datasource.download_filename)

    def _download_data(self, datasource: Datasource):
        download_path = self._download_path(datasource)
        if not os.path.exists(download_path):
            logger.info(f"downloading {datasource.download_url}")
            request_return = requests.get(datasource.download_url)
            with open(download_path, "wb") as download_file:
                logger.info(f"writing file {download_path}")
                download_file.write(request_return.content)

        if not tarfile.is_tarfile(download_path):
            return

        target_file_path = self._target_file_path(datasource)
        if not os.path.exists(target_file_path):
            logger.info(f"extracting {download_path} to {target_file_path}")
            with tarfile.open(download_path) as housing_tgz:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(housing_tgz, path=self.data_dir)
                housing_tgz.close()
        return


# def _save_path(root_data_dir, data_subdir, name):
#     save_path = pathlib.Path(root_data_dir).joinpath(data_subdir).joinpath(name)
#     return save_path
