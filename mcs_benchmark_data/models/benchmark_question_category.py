from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from enum import auto, Enum

from mcs_benchmark_data.models.benchmark_input import BenchmarkInput


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkQuestionCategory(BenchmarkInput, str, Enum):
    """The category of a benchmark sample (i.e. temporal reasoning, temporal sequences ...)"""

    TEMPORAL_REASONING = "TEMPORAL_REASONING"
    TAXONOMIC_REASONING = "TAXONOMIC_REASONING"
    QUALITATIVE_REASONING = "QUALITATIVE_REASONING"
    TEMPORAL_SEQUENCES = "TEMPORAL_SEQUENCES"
