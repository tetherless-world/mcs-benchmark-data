from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkChoices(_Model):
    '''List of possible choices in a benchmark sample'''
    numberOfItems: int
    choices: Tuple[BenchmarkChoice, ...]