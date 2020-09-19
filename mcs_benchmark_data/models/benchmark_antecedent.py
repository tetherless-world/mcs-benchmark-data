from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple, Union

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkAntecedent(_Model):
    '''A list of elements that compose a benchmark sample'''
    numberOfElements: int
    elements: Union[Tuple[BenchmarkContext, BenchmarkQuestion], Tuple[BenchmarkQuestion]]
