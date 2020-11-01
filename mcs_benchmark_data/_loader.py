from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator, Optional

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._pipeline_phase import _PipelinePhase
from mcs_benchmark_data.path import DATA_DIR_PATH


class _Loader(_PipelinePhase):
    def flush(self):
        """
        Flush any buffered data.
        """

    @abstractmethod
    def load(self, *, models: Generator[_Model, None, None]):
        """
        Load models from the given generator.
        :param models: generator of models to load, normally the result of the transformer
        """

    @property
    def _loaded_data_dir_path(self) -> Path:
        """
        Directory to use to store loaded data.
        The directory is created on demand when this method is called.
        A loader does not have to use this directory. It can load data into an external database, for example.
        """

        loaded_data_dir_path = DATA_DIR_PATH / self._pipeline_id / "loaded"
        loaded_data_dir_path = loaded_data_dir_path.absolute()
        loaded_data_dir_path.mkdir(parents=True, exist_ok=True)
        return loaded_data_dir_path
