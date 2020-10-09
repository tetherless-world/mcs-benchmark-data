from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph, URIRef
from rdflib.resource import Resource

from mcs_benchmark_data.namespace import XSD, MCS

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class DevScore(_Model):
    """Score of a system's correct predictions against a dev benchmark dataset"""

    submission_uri: URIRef
    is_based_on: str
    name: str
    value: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        resource.add(MCS.includedInDataset, self.submission_uri)
        resource.add(MCS.isBasedOn, self._quote_rdf_literal(self.is_based_on))
        resource.add(MCS.name, self._quote_rdf_literal(self.name))
        resource.add(MCS.value, self._quote_rdf_literal(self.value))

        return resource
