from typing import NamedTuple
from dataclasses import dataclass

from mcs_benchmark_data._benchmark_file_names import _BenchmarkFileNames


@dataclass(frozen=True)
class PhysicalIQaBenchmarkFileNames(_BenchmarkFileNames):
    dev_labels: str = "dev_labels.lst"
    dev_samples: str = "dev.jsonl"
    train_labels: str = "train_labels.lst"
    train_samples: str = "train.jsonl"
    test_samples: str = "test.jsonl"
