from typing import NamedTuple

from mcs-benchmark-data.benchmark_dataset import BenchmarkDataset

class BenchmarkDevDataset(BenchmarkDataset):
    #A dataset containing training samples of a benchmark
    #Super-class: BenchmarkDataset
    type: "BenchmarkTrainingDataset"