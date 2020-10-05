from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.namespace import MCS, SCHEMA
from rdflib import Graph, URIRef
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkDataset(_Model):
    """A file containing elements (questions, answers, context, observations, ...) of a benchmark"""
    """Sub-classes: BenchmarkDevDataset, BenchmarkTestDataset, BenchmarkTrainDataset"""
    
    benchmark_uri: URIRef
    name: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        resource.add(MCS.includedInDataset, self.benchmark_uri)
        resource.add(SCHEMA.name, self._quote_rdf_literal(self.name))

        return resource
