import logging
from abc import ABC


class _PipelinePhase(ABC):
    def __init__(self, *, pipeline_id: str, **kwds):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__pipeline_id = pipeline_id

    @property
    def _logger(self):
        return self.__logger

    @property
    def _pipeline_id(self):
        return self.__pipeline_id
