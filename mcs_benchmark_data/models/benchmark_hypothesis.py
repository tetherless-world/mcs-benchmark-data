from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from mcs_benchmark_data.namespace import MCS, RDF
from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkHypothesis(BenchmarkChoice):
    """A benchmark's sample hypothesis choice"""

    """Choice of observations (aNLI)"""

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        resource.add(RDF.type, MCS.BenchmarkChoice)

        return resource