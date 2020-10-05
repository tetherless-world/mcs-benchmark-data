from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json
from rdflib import Graph, URIRef
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.namespace import XSD, MCS


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkPrompt(_Model):
    """A benchmark's sample prompt element"""
    """Sub-classes: BenchmarkQuestion, BenchmarkObservation, BenchmarkGoal"""
    
    antecedent_uri: URIRef
    text: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        resource.add(MCS.includedInDataset, self.antecedent_uri)
        resource.add(XSD.string, self._quote_rdf_literal(self.text))

        return resource
