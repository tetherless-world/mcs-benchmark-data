from typing import Optional

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data._model import _Model

from mcs_benchmark_data.namespace import MCS
from rdflib import Graph, URIRef
from rdflib.resource import Resource


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkAntecedent(_Model):
    """A list of elements that compose a benchmark sample"""

    benchmark_sample_uri: URIRef
    question_type: Optional[URIRef]
    question_category: Optional[URIRef]

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        graph.add((self.benchmark_sample_uri, MCS.antecedent, self.uri))

        if self.question_type is not None:
            resource.add(MCS.question_type, self.question_type)
        if self.question_category is not None:
            resource.add(MCS.question_category, self.question_category)

        return resource
