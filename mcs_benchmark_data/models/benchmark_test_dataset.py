from typing import NamedTuple

from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset

class BenchmarkDevDataset(BenchmarkDataset):
    '''A dataset containing test samples of a benchmark'''
    '''Super-class: BenchmarkDataset'''
    type: "BenchmarkTestDataset"