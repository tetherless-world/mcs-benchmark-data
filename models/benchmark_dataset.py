from typing import NamedTuple


class BenchmarkDataset(NamedTuple):
    #A file containing elements (questions, answers, context, observations, ...) of a benchmark
    #Sub-classes: BenchmarkDevDataset, BenchmarkTestDataset, BenchmarkTrainingDataset
    id: str
    name: str