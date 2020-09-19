from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import NamedTuple

from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkTrainingDataset(BenchmarkDataset):
    '''A dataset containing training samples of a benchmark'''
    type: "BenchmarkTrainingDataset"