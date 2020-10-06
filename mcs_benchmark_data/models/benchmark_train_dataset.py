from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import RDF

from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkTrainDataset(BenchmarkDataset):
    """A dataset containing training samples of a benchmark"""

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = super.to_rdf(self, graph=graph)
        resource.add(RDF.string, self._quote_rdf_literal("BenchmarkTrainDataset"))

        return resource
