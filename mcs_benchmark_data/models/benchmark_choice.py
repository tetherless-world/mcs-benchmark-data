from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.namespace import SCHEMA, MCS, RDF
from rdflib import Graph, URIRef, Literal
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkChoice(_Model):
    """A possible choice for a benchmark sample"""

    """Sub-classes: BenchmarkAnswer, BenchmarkHypothesis, BenchmarkSolution"""
    benchmark_sample_uri: URIRef
    text: str
    position: int

    def to_rdf(self, *, graph: Graph) -> None:
        resource = _Model.to_rdf(self, graph=graph)
        graph.add((self.benchmark_sample_uri, MCS.choice, self.uri))
        resource.add(RDF.type, MCS.BenchmarkChoice)
        resource.add(SCHEMA.answer, self._quote_rdf_literal(self.text))
        resource.add(SCHEMA.position, Literal(self.position))

        return resource