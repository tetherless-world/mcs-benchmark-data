from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._benchmark_file_names import (
    _BenchmarkFileNames,
)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class TrianMCScriptSubmissionFileNames(_BenchmarkFileNames):
    submission: str = "trian_dev_submission.txt"
