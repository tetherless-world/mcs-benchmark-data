from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import URIRef

from mcs_benchmark_data.models.benchmark_input import BenchmarkInput


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkQuestionType(BenchmarkInput):
    """The type of a benchmark sample (i.e. multiple choice, true/false)."""

    @classmethod
    def multiple_choice(cls, *, uri_base: str, benchmark_sample_uri: URIRef):
        return cls(
            uri=URIRef(uri_base + ":multiple_choice"),
            benchmark_sample_uri=benchmark_sample_uri,
        )

    @classmethod
    def true_false(cls, *, uri_base: str, benchmark_sample_uri: URIRef):
        return cls(
            uri=URIRef(uri_base + ":true_false"),
            benchmark_sample_uri=benchmark_sample_uri,
        )
