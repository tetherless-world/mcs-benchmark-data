from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import XSD

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkContext(_Model):
    '''Context element of a benchmark sample'''
    text: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph
        )
        resource.add(XSD.string, self._quote_rdf_literal(self.text))

        return resource