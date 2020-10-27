from typing import NamedTuple
from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._benchmark_file_names import (
    _BenchmarkFileNames,
)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class KagnetCommonsenseQaSubmissionFileNames(_BenchmarkFileNames):
    submission: str = "dev_rand_split_kagnet_submission.jsonl"
