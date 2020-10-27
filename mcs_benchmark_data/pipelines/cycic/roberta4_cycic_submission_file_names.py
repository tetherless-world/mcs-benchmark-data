from typing import NamedTuple
from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._benchmark_file_names import (
    _BenchmarkFileNames,
)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Roberta4CycicSubmissionFileNames(_BenchmarkFileNames):
    submission_file_name: str = "CycIC_dev_cycic-transformers_submission.jsonl"
