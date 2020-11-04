from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class AnswerData:
    """
    Class for sample answers
    @param label: the label of the answer (e.g. True/False, A/B/C/D/E)
    @param text: the answer text
    """

    label: str
    text: str
