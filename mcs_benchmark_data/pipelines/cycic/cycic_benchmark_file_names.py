from typing import NamedTuple
from dataclasses import dataclass


from mcs_benchmark_data._benchmark_file_names import _BenchmarkFileNames


@dataclass(frozen=True)
class CycicBenchmarkFileNames(_BenchmarkFileNames):
    dev_labels: str = "CycIC_dev_labels.jsonl"
    dev_samples: str = "CycIC_dev_questions.jsonl"
    train_labels: str = "CycIC_training_labels.jsonl"
    train_samples: str = "CycIC_training_questions.jsonl"
