from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from typing import NamedTuple, Tuple, Optional

from rdflib import Graph
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import MCS, SCHEMA

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.benchmark_dataset import BenchmarkDataset
from mcs_benchmark_data.models.submission import Submission


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Benchmark(_Model):
    """A collection of datasets composing a benchmark"""

    name: str
    abstract: str
    authors: Tuple[str, ...]
    datasets: Tuple[BenchmarkDataset, ...]
    submissions: Optional[Tuple[Submission, ...]]

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)

        resource.add(SCHEMA.name, self._quote_rdf_literal(self.name))
        resource.add(SCHEMA.abstract, self._quote_rdf_literal(self.abstract))
        for author in self.authors:
            resource.add(SCHEMA.person, self._quote_rdf_literal(author))

        for dataset in self.datasets:
            resource.add(MCS.benchmarkDataset, dataset)

        if self.submissions is not None:
            for submission in self.submissions:
                resource.add(MCS.submission, submission)

        return resource
