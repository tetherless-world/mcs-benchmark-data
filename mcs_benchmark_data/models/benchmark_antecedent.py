from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple, Union

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_prompt import BenchmarkPrompt
from mcs_benchmark_data.models.benchmark_question import BenchmarkQuestion
from mcs_benchmark_data.models.benchmark_observation import BenchmarkObservation
from mcs_benchmark_data.models.benchmark_goal import BenchmarkGoal
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext

from mcs_benchmark_data.namespace import MCS, SCHEMA
from rdflib import Graph
from rdflib.resource import Resource

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkAntecedent(_Model):
    '''A list of elements that compose a benchmark sample'''
    elements: Union[Tuple[BenchmarkContext, BenchmarkPrompt], Tuple[BenchmarkPrompt,...]]

    def to_rdf( self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph
        )
        for element in self.elements:
            if isinstance(element,BenchmarkContext):
                resource.add(MCS.benchmarkContext, element)
            elif isinstance(element, BenchmarkQuestion):
                resource.add(MCS.benchmarkQuestion, element)
            elif isinstance(element, BenchmarkObservation):
                resource.add(MCS.benchmarkObservation, element)
            elif isinstance(element, BenchmarkGoal):
                resource.add(MCS.benchmarkGoal, element)
            else:
                 resource.add(MCS.benchmarkPrompt, element)


        return resource
