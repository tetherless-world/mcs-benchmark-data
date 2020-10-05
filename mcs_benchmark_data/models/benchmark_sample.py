from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing_extensions import Literal

from rdflib import Graph, URIRef
from rdflib.resource import Resource

from mcs_benchmark_data.namespace import MCS, XSD

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_question_category import BenchmarkQuestionCategory


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkSample(_Model):
    """An entry in a benchmark dataset"""

    dataset_uri: URIRef
    question_type: BenchmarkQuestionType
    question_category: BenchmarkQuestionCategory
    correct_choice: int

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)

        resource.add(MCS.includedInDataset, self.dataset_uri)

        resource.add(MCS.benchmarkQuestionType, self.question_type)

        resource.add(MCS.benchmarkQuestionCategory, self.question_category)

        resource.add(XSD.int, Literal(self.correct_choice))

        return resource
