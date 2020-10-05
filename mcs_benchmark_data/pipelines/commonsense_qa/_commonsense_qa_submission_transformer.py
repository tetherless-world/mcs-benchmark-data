import json
import os
from pathlib import Path
from typing import Generator
from abc import abstractmethod
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.dev_score import DevScore


class _CommonsenseQaSubmissionTransformer(_Transformer):

    """
    Abstract base class for CommonsenseQA transformers.
    See the transform method of _Transformer.
    """

    __URI_BASE = "benchmark:commonsense_qa"
    __BENCHMARK_SCORE_CLASSES = {"TestScore": TestScore, "DevScore": DevScore}

    @abstractmethod
    def __transform_submission(self, **kwds) -> Generator[_Model, None, None]:
        """
        Transform previously extracted submission metadata into submission (and related) models.
        :param kwds: merged dictionary of initial extract kwds and the result of extract
        :return: generator of models
        """

    @abstractmethod
    def __transform_submission_sample(self, **kwds) -> Generator[_Model, None, None]:

        """
        Transform previously-extracted submission sample data into Submission Sample (and related) models.
        :param kwds: merged dictionary of initial extract kwds and the result of extract
        :return: generator of models
        """
