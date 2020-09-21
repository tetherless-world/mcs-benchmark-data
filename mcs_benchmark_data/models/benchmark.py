from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import NamedTuple, Tuple

from rdflib import Graph
from rdflib.resource import Resource
from ..namespace import MCS, RDF

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.submission import Submission

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class Benchmark(_Model):
    '''A collection of datasets composing a benchmark'''
    name: str
    abstract: str
    author: Tuple[str, ...]
    dataset: Tuple[BenchmarkDataset, ...]
    submissions: Tuple[Submission, ...]

    def to_rdf(
        self, *, graph: Graph, **kwds) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph, **kwds
        )
        resource.add(RDF.type, MCS[self.__class__.__name__])

        #How to add name? FOAF?
        #How to add abstract? Text?
        #How to add authors? FOAF? DCTERMS?
        for ds in self.dataset:
            resource.add(MCS.BenchmarkDataset, ds)
            #Do I need to additionally call ds.to_rdf?
        if self.submissions is not None:
            for submission in self.submissions:
                resource.add(MCS.Submission, submission)

        return resource