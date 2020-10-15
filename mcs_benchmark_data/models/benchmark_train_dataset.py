from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkTrainDataset(BenchmarkDataset):
    """A dataset containing training samples of a benchmark"""
