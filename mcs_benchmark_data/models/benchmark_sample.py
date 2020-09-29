from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple
from typing_extensions import Literal

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
    questionType: BenchmarkQuestionType
    questionCategory: BenchmarkQuestionCategory
    antecedent: BenchmarkAntecedent
    choices: BenchmarkChoices
    correctChoice: int

    def to_rdf(
        self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph
        )

        
        resource.add(XSD.string, self._quote_rdf_literal(self.includedInDataset))

        resource.add(MCS.benchmarkQuestionType, self.questionType)

        resource.add(MCS.benchmarkQuestionCategory, self.questionCategory)

        resource.add(MCS.benchmarkAntecedent, self.antecedent)

        resource.add(MCS.benchmarkChoices, self.choices)

        resource.add(XSD.int, Literal(self.correctChoice))

        return resource

