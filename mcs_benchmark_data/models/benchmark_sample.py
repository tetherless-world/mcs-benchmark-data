from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph, URIRef, Literal
from rdflib.resource import Resource

from mcs_benchmark_data.namespace import MCS, XSD

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_question_type import BenchmarkQuestionType
from mcs_benchmark_data.models.benchmark_question_category import (
    BenchmarkQuestionCategory,
)


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

        resource.add(
            MCS.benchmarkQuestionType, self._quote_rdf_literal(self.question_type)
        )

        if self.question_category is not None:
            resource.add(
                MCS.benchmarkQuestionCategory,
                self._quote_rdf_literal(self.question_category),
            )

        resource.add(XSD.integer, Literal(self.correct_choice))

        return resource
