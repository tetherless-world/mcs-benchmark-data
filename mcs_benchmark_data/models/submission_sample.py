from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.namespace import MCS, SCHEMA
from rdflib import Graph, URIRef, Literal
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
        graph.add((self.submission_uri, MCS.submissionSample, self.uri))
        resource.add(SCHEMA.value, Literal(self.value))
        resource.add(SCHEMA.about, self._quote_rdf_literal(self.about))

        return resource
