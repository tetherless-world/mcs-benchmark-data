from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._model import _Model

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkConcept(_Model):
    '''The ConceptNet concept which the question was created from (i.e. electricity)'''
    concept: str

