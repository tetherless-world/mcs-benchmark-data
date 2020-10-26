from typing import NamedTuple
from dataclasses import dataclass


from mcs_benchmark_data._benchmark_file_names import _BenchmarkFileNames


@dataclass(frozen=True)
class CommonsenseQaBenchmarkFileNames(_BenchmarkFileNames):
    dev_samples: str = "dev_rand_split.jsonl"
    train_samples: str = "train_rand_split.jsonl"
    test_samples: str = "test_rand_split_no_answers.jsonl"
