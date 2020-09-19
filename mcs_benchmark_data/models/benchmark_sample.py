from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext
from mcs_benchmark_data.models.benchmark_prompt import BenchmarkPrompt
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_question_category import BenchmarkQuestionCategory
from mcs_benchmark_data.models.benchmark_choices import BenchmarkChoices

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkSample(_Model):
    '''An entry in a benchmark dataset'''
    includedInDataset: str
    question_type: BenchmarkQuestionType
    question_category: BenchmarkQuestionCategory
    antecedent: Tuple[BenchmarkContext, BenchmarkPrompt]
    choice: BenchmarkChoices
    correctChoice: int