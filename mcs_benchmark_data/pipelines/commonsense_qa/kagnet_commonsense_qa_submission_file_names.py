from typing import NamedTuple
from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._benchmark_submission_file_names import (
    _BenchmarkSubmissionFileNames,
)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class KagnetCommonsenseQaSubmissionFileNames(_BenchmarkSubmissionFileNames):
    submission_file_name: str = "dev_rand_split_kagnet_submission.jsonl"
