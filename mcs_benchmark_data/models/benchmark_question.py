from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from rdflib import Graph
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import MCS, XSD

from mcs_benchmark_data.models.benchmark_prompt import BenchmarkPrompt
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkQuestion(BenchmarkPrompt):
    '''A benchmark's sample question element'''
    concepts: Tuple[BenchmarkConcept, ...]

    def to_rdf( self, *, graph: Graph) -> Resource:
        resource = BenchmarkPrompt().to_rdf(graph=graph)
        for concept in self.concepts:
            resource.add(MCS.benchmarkConcept, concept)