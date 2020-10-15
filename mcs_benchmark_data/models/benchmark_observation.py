from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import SCHEMA

from mcs_benchmark_data.models.benchmark_input import BenchmarkInput


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkObservation(BenchmarkInput):
    """A benchmark's sample observation element"""

    """Prompt for aNLI"""

    text: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = super().to_rdf(graph=graph)
        resource.add(SCHEMA.text, self._quote_rdf_literal(self.text))

        return resource