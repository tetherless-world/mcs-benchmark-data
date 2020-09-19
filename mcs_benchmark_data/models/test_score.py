from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._model import _Model

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class TestScore(_Model):
    '''Score of a system's correct predictions against a test benchmark dataset'''
    name: str
    value: str
    