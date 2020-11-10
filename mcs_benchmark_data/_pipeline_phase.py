import logging
from abc import ABC
from pathlib import Path

from mcs_benchmark_data.path import DATA_DIR_PATH


class _PipelinePhase(ABC):
    def __init__(
        self, *, pipeline_id: str, data_dir_path: Path = DATA_DIR_PATH, **kwds
    ):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__pipeline_id = pipeline_id
        self.__data_dir_path = data_dir_path

    @property
    def _logger(self):
        return self.__logger

    @property
    def _pipeline_id(self):
        return self.__pipeline_id

    @property
    def _pipeline_data_dir_path(self) -> Path:
        """
        Directory to use to store data.
        The directory is created on demand when this method is called.
        Paths into this directory can be passed to the transformer via the kwds return from extract.
        """
        pipeline_data_dir_path = self.__data_dir_path / self.__pipeline_id
        pipeline_data_dir_path = pipeline_data_dir_path.absolute()
        pipeline_data_dir_path.mkdir(parents=True, exist_ok=True)
        return pipeline_data_dir_path
