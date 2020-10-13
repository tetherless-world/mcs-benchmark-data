from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.namespace import SCHEMA, MCS, RDF
from rdflib import Graph, Literal
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkAnswer(BenchmarkChoice):
    """A benchmark answer choice"""

    """Choice of CommonsenseQA, Cosmos QA, Social IQa"""

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        resource.add(RDF.type, MCS.BenchmarkChoice)
        resource.add(SCHEMA.answer, self._quote_rdf_literal(self.text))
        resource.add(MCS.position, Literal(self.position))

        return resource