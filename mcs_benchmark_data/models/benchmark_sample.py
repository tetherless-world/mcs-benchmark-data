from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data.namespace import MCS, SCHEMA, XSD

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_question_category import BenchmarkQuestionCategory
from mcs_benchmark_data.models.benchmark_choices import BenchmarkChoices
from mcs_benchmark_data.models.benchmark_antecedent import BenchmarkAntecedent

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkSample(_Model):
    '''An entry in a benchmark dataset'''
    includedInDataset: str
    question_type: BenchmarkQuestionType
    question_category: BenchmarkQuestionCategory
    antecedent: BenchmarkAntecedent
    choices: BenchmarkChoices
    correctChoice: int

    def to_rdf(
        self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph
        )

        
        resource.add(XSD.string, self.includedInDataset)

        resource.add(MCS.benchmarkQuestionType, self.question_type)

        resource.add(MCS.benchmarkQuestionCategory, self.question_category)

        resource.add(MCS.benchmarkAntecedent, self.antecedent)
        self.antecedent.to_rdf(graph)

        resource.add(MCS.benchmarkChoices, self.choices)
        self.choices.to_rdf(graph)

        resource.add(XSD.int, self.correctChoice)

        return resource

