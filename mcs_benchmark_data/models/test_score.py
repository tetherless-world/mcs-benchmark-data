from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph, URIRef
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import MCS, SCHEMA

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class TestScore(_Model):
    """Score of a system's correct predictions against a test benchmark dataset"""

    submission_uri: URIRef
    is_based_on: str
    name: str
    value: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        graph.add((self.submission_uri, MCS.testScore, self.uri))
        resource.add(SCHEMA.isBasedOn, self._quote_rdf_literal(self.is_based_on))
        resource.add(SCHEMA.name, self._quote_rdf_literal(self.name))
        resource.add(SCHEMA.value, self._quote_rdf_literal(self.value))

        return resource
