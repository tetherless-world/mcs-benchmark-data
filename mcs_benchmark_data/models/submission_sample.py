from typing_extensions import Literal
from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.namespace import SCHEMA, XSD, MCS
from rdflib import Graph, URIRef
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class SubmissionSample(_Model):
    """An entry in a submission dataset (i.e. prediction)"""

    submission_uri: URIRef
    value: int
    about: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        resource.add(MCS.includedInDataset, self.submission_uri)
        resource.add(SCHEMA.value, Literal(self.value))
        resource.add(XSD.string, self._quote_rdf_literal(self.about))

        return resource
