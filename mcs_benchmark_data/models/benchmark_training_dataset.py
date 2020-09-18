from typing import NamedTuple

from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset

class BenchmarkDevDataset(BenchmarkDataset):
    '''A dataset containing training samples of a benchmark'''
    '''Super-class: BenchmarkDataset'''
    type: "BenchmarkTrainingDataset"