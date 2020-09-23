from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data.namespace import XSD

from mcs_benchmark_data._model import _Model

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class DevScore(_Model):
    '''Score of a system's correct predictions against a dev benchmark dataset'''
    name: str
    value: str

    def to_rdf(
        self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph
        )
        resource.add(XSD.string, self.name)
        resource.add(XSD.string, self.value)

        return resource