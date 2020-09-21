from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkContext(_Model):
    '''Context element of a benchmark sample'''
    text: str
