from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json
from rdflib import Graph
from rdflib.resource import Resource

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.namespace import XSD, MCS


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkPrompt(_Model):
    """A benchmark's sample prompt element"""

    """Sub-classes: BenchmarkQuestion, BenchmarkObservation, BenchmarkGoal"""
    text: str

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)
        # Trying to add sub-class name if possible...
        resource.add(MCS.MCS[self.__class__.__name__], self)
        resource.add(XSD.string, self._quote_rdf_literal(self.text))

        return resource
