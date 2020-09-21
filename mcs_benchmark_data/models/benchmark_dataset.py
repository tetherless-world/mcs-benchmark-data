from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from ..namespace import RDF, MCS
from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_sample import BenchmarkSample

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkDataset(_Model):
    '''A file containing elements (questions, answers, context, observations, ...) of a benchmark'''
    '''Sub-classes: BenchmarkDevDataset, BenchmarkTestDataset, BenchmarkTrainingDataset'''
    name: str
    entries: Tuple[BenchmarkSample,...]

    def to_rdf(
        self, *, graph: Graph, **kwds) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph, **kwds
        )
        resource.add(RDF.type, MCS[self.__class__.__name__])

        #How to add name?
        for entry in self.entries:
            entry.to_rdf(add_to_resource=resource)

        return resource