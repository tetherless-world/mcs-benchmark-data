from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import NamedTuple, Tuple

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.submission import Submission

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class Benchmark(_Model):
    '''A collection of datasets composing a benchmark'''
    name: str
    abstract: str
    author: Tuple[str, ...]
    dataset: Tuple[BenchmarkDataset, ...]
    submissions: Tuple[Submission, ...]