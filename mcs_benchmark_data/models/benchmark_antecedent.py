from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple, Union

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_prompt import BenchmarkPrompt
from mcs_benchmark_data.models.benchmark_context import BenchmarkContext

from ..namespace import MCS
from rdflib.resource import Resource

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class BenchmarkAntecedent(_Model):
    '''A list of elements that compose a benchmark sample'''
    elements: Tuple[BenchmarkContext, BenchmarkPrompt]

    def to_rdf( self, *, add_to_resource: Resource) -> None:
        if self.elements[0] is not None:
            add_to_resource.add(MCS.BenchmarkContext, self.elements[0].text)
        self.elements[1].to_rdf(add_to_resource = add_to_resource)
