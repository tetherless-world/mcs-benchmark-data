from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import Tuple

from rdflib import Graph
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import SCHEMA

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Benchmark(_Model):
    """A collection of datasets composing a benchmark"""

    name: str
    abstract: str
    authors: Tuple[str, ...]

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)

        resource.add(SCHEMA.name, self._quote_rdf_literal(self.name))
        resource.add(SCHEMA.abstract, self._quote_rdf_literal(self.abstract))
        for author in self.authors:
            resource.add(SCHEMA.author, self._quote_rdf_literal(author))

        return resource
