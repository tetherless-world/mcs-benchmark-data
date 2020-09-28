import logging
from abc import abstractmethod
from typing import Generator

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._pipeline_phase import _PipelinePhase


class _Transformer(_PipelinePhase):
    """
    Abstract base class for transformers.
    See the transform method.
    """

    @abstractmethod
    def transform(self, **kwds) -> Generator[_Model, None, None]:
        """
        Transform previously-extracted data into models.
        :param kwds: merged dictionary of initial extract kwds and the result of extract
        :return: generator of models
        """
