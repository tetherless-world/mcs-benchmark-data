from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from mcs_benchmark_data.namespace import RDF, MCS
from rdflib import Graph, URIRef
from rdflib.resource import Resource

from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkChoices:
    """List of possible choices in a benchmark sample"""

    benchmark_sample_uri: URIRef
    choices: Tuple[BenchmarkChoice, ...]

    def to_rdf(self, *, graph: Graph) -> None:
        for choice in self.choices:
            graph.add((self.benchmark_sample_uri, MCS.choice, choice.uri))
