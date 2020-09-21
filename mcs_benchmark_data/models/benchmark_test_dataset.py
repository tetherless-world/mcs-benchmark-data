from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import NamedTuple

from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkTestDataset(BenchmarkDataset):
    '''A dataset containing test samples of a benchmark'''
    type: "BenchmarkTestDataset"

    def to_rdf(
        self, *, graph: Graph, **kwds) -> Resource:
        resource = super.to_rdf(self,graph=graph)

        #How to add type?

        return resource