from typing import NamedTuple, Optional
from dataclasses import dataclass

from mcs_benchmark_data._benchmark_file_names import _BenchmarkFileNames


@dataclass(frozen=True)
class InlineLabelsBenchmarkFileNames(_BenchmarkFileNames):
    """
    Class for benchmarks that have the solutions to their
    samples in the same files as the samples themselves
    """

    dev_samples: str
    train_samples: str
    test_samples: str
