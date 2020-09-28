from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from mcs_benchmark_data.namespace import MCS, SCHEMA
from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkChoices(_Model):
    '''List of possible choices in a benchmark sample'''
    choices: Tuple[BenchmarkChoice, ...]

    def to_rdf(
        self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph
        )

        for choice in self.choices:
            resource.add(MCS.benchmarkChoice, choice)

        return resource