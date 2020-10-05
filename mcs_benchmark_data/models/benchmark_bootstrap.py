from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BenchmarkBootstrap:
    """A model to parse data for a given benchmark"""

    name: str
    abstract: str
    authors: Tuple[str, ...]
