from abc import abstractmethod
from typing import Generator, Tuple

from mcs_benchmark_data._loader import _Loader
from mcs_benchmark_data._model import _Model


class _BufferingLoader(_Loader):
    def __init__(self, **kwds):
        _Loader.__init__(self, **kwds)
        self.__models = []

    def flush(self):
        return self._flush(tuple(self.__models))

    @abstractmethod
    def _flush(self, models: Tuple[_Model, ...]):
        raise NotImplementedError

    def load(self, *, models: Generator[_Model, None, None]):
        self.__models.extend(models)