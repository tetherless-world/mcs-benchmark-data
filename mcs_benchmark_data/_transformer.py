import logging
from abc import ABC, abstractmethod
from typing import Generator

from mcs_benchmark_data._model import _Model


class _Transformer(ABC):
    """
    Abstract base class for transformers.
    See the transform method.
    """

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def transform(self, **kwds) -> Generator[_Model, None, None]:
        """
        Transform previously-extracted data into models (e.g., nodes and edges).
        :param kwds: merged dictionary of initial extract kwds and the result of extract
        :return: generator of models
        """
    