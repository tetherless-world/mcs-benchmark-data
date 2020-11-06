from typing import Optional

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

from rdflib import Graph, URIRef
from rdflib.resource import Resource

from mcs_benchmark_data.namespace import MCS, SCHEMA

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class BenchmarkSample(_Model):
    """An entry in a benchmark dataset"""

    dataset_uri: URIRef
    correct_choice: Optional[URIRef]

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)

        graph.add((self.dataset_uri, MCS.sample, self.uri))

        resource.add(SCHEMA.includedInDataset, self.dataset_uri)

        if self.correct_choice is not None:
            resource.add(MCS.correctChoice, self.correct_choice)

        return resource
