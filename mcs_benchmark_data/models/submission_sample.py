from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._model import _Model

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class SubmissionSample(_Model):
    '''An entry in a submission dataset (i.e. prediction)'''
    type: str
    includedInDataset: str
    value: int
    about: str