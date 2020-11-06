from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from datetime import datetime
from typing import Tuple

from rdflib import Graph
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import MCS, SCHEMA

from mcs_benchmark_data._model import _Model


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Submission(_Model):
    """A submission dataset from a system/model with prediction choices for a benchmark"""

    name: str
    description: str
    date_created: datetime
    is_based_on: str  # benchmark name
    contributors: Tuple[str, ...]
    result_of: Tuple[str, datetime, datetime, str]

    def to_rdf(self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(self, graph=graph)

        resource.add(SCHEMA.name, self._quote_rdf_literal(self.name))
        resource.add(SCHEMA.description, self._quote_rdf_literal(self.description))
        resource.add(SCHEMA.dateCreated, self.date_created)
        resource.add(SCHEMA.isBasedOn, self._quote_rdf_literal(self.is_based_on))
        for contributor in self.contributors:
            resource.add(MCS.contributor, self._quote_rdf_literal(contributor))

        resource.add(
            SCHEMA.softwareApplication, self._quote_rdf_literal(self.result_of[0])
        )
        resource.add(SCHEMA.endTime, self.result_of[1])
        resource.add(SCHEMA.startTime, self.result_of[2])
        resource.add(SCHEMA.url, self._quote_rdf_literal(self.result_of[3]))

        return resource
