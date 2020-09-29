from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing_extensions import Literal

from mcs_benchmark_data.namespace import MCS, SCHEMA
from rdflib import Graph
from rdflib.namespace import RDF
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkChoice(_Model):
    """A possible choice for a benchmark sample"""

    """Sub-classes: BenchmarkAnswer, BenchmarkHypothesis, BenchmarkSolution"""
    text: str
    position: int

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)

        resource.add(SCHEMA.answer, self._quote_rdf_literal(self.text))
        resource.add(SCHEMA.position, self._quote_rdf_literal(self.position))

        return resource
