from typing import NamedTuple, Tuple, Optional

from rdflib import Graph
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import MCS, SCHEMA

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.submission import Submission

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkBootstrap(_Model):
    '''A collection of datasets composing a benchmark'''
    name: str
    abstract: str
    authors: Tuple[str, ...]
    datasets: Tuple[BenchmarkDataset, ...]
    submissions: Optional[Tuple[Submission, ...]]

    