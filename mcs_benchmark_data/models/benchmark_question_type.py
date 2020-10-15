from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from enum import auto, Enum

from mcs_benchmark_data.models.benchmark_input import BenchmarkInput


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkQuestionType(BenchmarkInput, str, Enum):
    """The type of a benchmark sample (i.e. multiple choice, true/false)."""

    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    TRUE_FALSE = "TRUE_FALSE"
