from typing import NamedTuple, Tuple

from mcs-benchmark-data.benchmark_dataset import BenchmarkDataset
from mcs-benchmark-data.benchmark_context import BenchmarkContext
from mcs-benchmark-data.benchmark_question_type import BenchmarkQuestionType

class Benchmark(NamedTuple):
    #A collection of datasets composing a benchmark
    id: str
    name: str
    abstract: str
    author: Tuple[str, ...]
    dataset: Tuple[BenchmarkDataset, ...]