import logging
from abc import abstractmethod
from typing import Generator
from pathlib import Path

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._pipeline_phase import _PipelinePhase


class _Transformer(_PipelinePhase):
    """
    Abstract base class for transformers.
    See the transform method.
    """

    def __init__(
        self,
        extracted_data_dir_path: Path,
        **kwds,
    ):
        _Transformer.__init__(self, **kwds)
        self._extracted_data_dir_path = extracted_data_dir_path

    @abstractmethod
    def transform(self, **kwds) -> Generator[_Model, None, None]:
        """
        Transform previously-extracted data into models.
        :param kwds: merged dictionary of initial extract kwds and the result of extract
        :return: generator of models
        """
