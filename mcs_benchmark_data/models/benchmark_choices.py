from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from ..namespace import MCS
from rdflib import Graph
from rdflib.namespace import RDF
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_choice import BenchmarkChoice

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkChoices(_Model):
    '''List of possible choices in a benchmark sample'''
    choices: Tuple[BenchmarkChoice, ...]

    def to_rdf(
        self, *, graph: Graph, **kwds) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph, **kwds
        )
        resource.add(RDF.type, MCS[self.__class__.__name__])

        for choice in self.choices:
            resource.add(MCS.BenchmarkChoice, choice)
            choice.to_rdf(add_to_resource=resource)
        return resource