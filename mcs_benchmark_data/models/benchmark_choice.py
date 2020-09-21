from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Literal

from ..namespace import MCS
from rdflib import Graph
from rdflib.namespace import RDF
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkChoice(_Model):
    '''A possible choice for a benchmark sample'''
    '''Sub-classes: BenchmarkAnswer, BenchmarkHypothesis, BenchmarkSolution'''
    text: str

    def to_rdf(self, *, add_to_resource: Resource) -> None:
        #How to add text? Which namespace to use?
        #add_to_resource.add(MCS.BenchmarkConcept, self.concept)