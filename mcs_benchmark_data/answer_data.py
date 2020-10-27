from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class AnswerData:
    label: str
    text: str
