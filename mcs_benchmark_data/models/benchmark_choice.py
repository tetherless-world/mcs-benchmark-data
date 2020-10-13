from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.namespace import SCHEMA, MCS
from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkChoice(_Model):
    """A possible choice for a benchmark sample"""

    """Sub-classes: BenchmarkAnswer, BenchmarkHypothesis, BenchmarkSolution"""
    text: str
    position: int
