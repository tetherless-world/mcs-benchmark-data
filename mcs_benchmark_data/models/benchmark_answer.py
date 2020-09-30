from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkAnswer(BenchmarkChoice):
    """A benchmark answer choice"""

    """Choice of CommonsenseQA, Cosmos QA, Social IQa"""
