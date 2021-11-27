import os
import pathlib
import tarfile
import requests
import logging
from typing import Dict
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Datasource:
    name: str
    download_url: str
    download_filename: str
    output_filename: str


@dataclass
class Datasources:
    data_dir: pathlib.Path
    datasources: Dict[str, Datasource] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)

    def add_datasource(
        self, name, download_url, download_filename, output_filename
    ) -> None:
        if name in self.datasources.keys():
            raise ValueError("name already exists")

        self.datasources[name] = Datasource(
            name=name,
            download_url=download_url,
            download_filename=download_filename,
            output_filename=output_filename,
        )

    def get_datasource(self, name: str) -> Datasource:
        return self.datasources[name]

    def get_data(self, name: str) -> pathlib.Path:
        ds = self.get_datasource(name)
        self._download_data(ds)
        return self._target_file_path(ds)

    def _target_file_path(self, datasource) -> pathlib.Path:
        return self.data_dir.joinpath(datasource.output_filename)

    def _download_path(self, datasource) -> pathlib.Path:
        return self.data_dir.joinpath(datasource.download_filename)

    def _download_data(self, datasource: Datasource):
        download_path = self._download_path(datasource)
        if not os.path.exists(download_path):
            logger.info(f"downloading {datasource.download_url}")
            r = requests.get(datasource.download_url)
            with open(download_path, "wb") as f:
                logger.info(f"writing file {download_path}")
                f.write(r.content)

        if not tarfile.is_tarfile(download_path):
            return

        target_file_path = self._target_file_path(datasource)
        if not os.path.exists(target_file_path):
            logger.info(f"extracting {download_path} to {target_file_path}")
            housing_tgz = tarfile.open(download_path)
            housing_tgz.extractall(path=self.data_dir)
            housing_tgz.close()

        return
