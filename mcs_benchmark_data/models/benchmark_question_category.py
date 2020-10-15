from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import URIRef

from mcs_benchmark_data.models.benchmark_input import BenchmarkInput


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkQuestionCategory(BenchmarkInput):
    """The category of a benchmark sample (i.e. temporal reasoning, temporal sequences ...)"""

    @classmethod
    def temporal_reasoning(cls, *, uri_base: str, benchmark_sample_uri: URIRef):
        return cls(
            uri=URIRef(uri_base + ":temporal_reasoning"),
            benchmark_sample_uri=benchmark_sample_uri,
        )

    @classmethod
    def taxonomic_reasoning(cls, *, uri_base: str, benchmark_sample_uri: URIRef):
        return cls(
            uri=URIRef(uri_base + ":taxonomic_reasoning"),
            benchmark_sample_uri=benchmark_sample_uri,
        )

    @classmethod
    def qualitative_reasoning(cls, *, uri_base: str, benchmark_sample_uri: URIRef):
        return cls(
            uri=URIRef(uri_base + ":qualitative_reasoning"),
            benchmark_sample_uri=benchmark_sample_uri,
        )

    @classmethod
    def temporal_sequences(cls, *, uri_base: str, benchmark_sample_uri: URIRef):
        return cls(
            uri=URIRef(uri_base + ":temporal_sequences"),
            benchmark_sample_uri=benchmark_sample_uri,
        )
