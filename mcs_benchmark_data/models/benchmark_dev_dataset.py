from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkDevDataset(BenchmarkDataset):
    """A dataset containing dev samples of a benchmark"""

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = super().to_rdf(self, graph=graph)
        resource.add(XSD.string, self._quote_rdf_literal("BenchmarkDevDataset"))

        return resource
