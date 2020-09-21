from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib.resource import Resource
from ..namespace import MCS

from mcs_benchmark_data.models.benchmark_prompt import BenchmarkPrompt
from mcs_benchmark_data.models.benchmark_concept import BenchmarkConcept

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkQuestion(BenchmarkPrompt):
    '''A benchmark's sample question element'''
    concept: BenchmarkConcept

    def to_rdf(self, *, add_to_resource: Resource) -> None:
        if self.concept is not None:
            add_to_resource.add(MCS.BenchmarkConcept, self.concept)