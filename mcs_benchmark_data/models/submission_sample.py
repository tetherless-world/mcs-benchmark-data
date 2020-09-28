from typing import Literal
from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.namespace import SCHEMA, XSD
from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class SubmissionSample(_Model):
    '''An entry in a submission dataset (i.e. prediction)'''
    about: str
    includedInDataset: str
    value: int

    def to_rdf(
        self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph
        )
        resource.add(SCHEMA.about, self._quote_rdf_literal(self.about))
        resource.add(XSD.string, self._quote_rdf_literal(self.includedInDataset))
        resource.add(SCHEMA.value, Literal(self.value))

        return resource