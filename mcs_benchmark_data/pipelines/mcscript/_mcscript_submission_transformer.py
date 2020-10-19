import json
import os
from pathlib import Path
from typing import Generator
from rdflib import URIRef

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.dev_score import DevScore


class _MCScriptSubmissionTransformer(_Transformer):

    """
    Abstract base class for Trian transformers.
    See the transform method of _Transformer.
    """
