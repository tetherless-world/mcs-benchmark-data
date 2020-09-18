from typing import NamedTuple, Tuple

from mcs_benchmark_data.models.model import Model
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset

class Benchmark(Model):
    '''A collection of datasets composing a benchmark'''
    name: str
    abstract: str
    author: Tuple[str, ...]
    dataset: Tuple[BenchmarkDataset, ...]