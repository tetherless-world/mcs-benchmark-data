from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph
from rdflib.resource import Resource
from ..namespace import 

from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkDevDataset(BenchmarkDataset):
    '''A dataset containing dev samples of a benchmark'''
    type: "BenchmarkDevDataset"

    def to_rdf(
        self, *, graph: Graph, **kwds) -> Resource:
        super.to_rdf(self,graph=graph)

        #How to add type?

        return resource