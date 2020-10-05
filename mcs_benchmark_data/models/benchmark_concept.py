from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph, URIRef
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import RDF, XSD

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkConcept(_Model):
    """The ConceptNet concept which the question was created from (i.e. electricity)"""

    benchmark_sample_uri: URIRef
    concept: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        resource.add(RDF.type, self.benchmark_sample_uri)
        resource.add(XSD.string, self._quote_rdf_literal(self.concept))

        return resource
