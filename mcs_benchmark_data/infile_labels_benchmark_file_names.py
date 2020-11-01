from typing import NamedTuple
from dataclasses import dataclass

from mcs_benchmark_data._benchmark_file_names import _BenchmarkFileNames


@dataclass(frozen=True)
class InfileLabelsBenchmarkFileNames(_BenchmarkFileNames):
    dev_labels: str
    dev_samples: str
    train_labels: str
    train_samples: str
    test_samples: str
