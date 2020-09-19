from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._model import _Model

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkPrompt(_Model):
    '''A benchmark's sample prompt element'''
    '''Sub-classes: BenchmarkQuestion, BenchmarkObservation, BenchmarkGoal'''
    text: str