from dataclasses import dataclass
from typing import Tuple

from mcs_benchmark_data.namespace import MCS, RDF


from dataclasses_json import LetterCase, dataclass_json
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.resource import Resource


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class _Model:
    uri: URIRef



    def to_rdf(self, *, graph: Graph) -> Resource:
        """
        Convert this model to RDF.
        """

        resource = graph.resource(self.uri)

        resource.add(RDF.type, MCS[self.__class__.__name__])

        return resource