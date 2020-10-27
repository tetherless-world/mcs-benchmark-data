from typing import NamedTuple
from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class _BenchmarkFileNames:
    meta_data: str = "metadata.json"
