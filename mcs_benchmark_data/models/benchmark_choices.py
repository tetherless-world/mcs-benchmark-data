from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from mcs_benchmark_data.namespace import RDF
from rdflib import Graph, URIRef
from rdflib.resource import Resource

from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkChoices:
    """List of possible choices in a benchmark sample"""

    benchmark_sample_uri: URIRef
    choices: Tuple[BenchmarkChoice, ...]

    # Not necessary, since it doesn't have a URI - I believe
    # def to_rdf(self, *, graph: Graph) -> Resource:
    #     resource = super().to_rdf(graph=graph)
    #     resource.add(MCS.includedInDataset, benchmark_sample_uri)

    #     return resource
