from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph, URIRef
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import RDF, MCS, SCHEMA

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkContext(_Model):
    """Context element of a benchmark sample"""

    antecedent_uri: URIRef
    text: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        graph.add((self.antecedent_uri, MCS.BenchmarkContext, self.uri))
        resource.add(SCHEMA.text, self._quote_rdf_literal(self.text))

        return resource
