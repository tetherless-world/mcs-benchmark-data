from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkMetadata:
    """A model to parse data for a given benchmark"""

    name: str
    abstract: str
    authors: Tuple[str, ...]
