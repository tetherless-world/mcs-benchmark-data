from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json
from rdflib import Graph, Literal, URIRef
from rdflib.resource import Resource

from mcs_benchmark_data.namespace import MCS, RDF


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

    @staticmethod
    def _quote_rdf_literal(text: str) -> Literal:
        fixed = text.replace("'", "\\'")
        fixed = fixed.replace('"', '\\"')
        fixed = fixed.replace("\n", "\\n")
        fixed = fixed.replace("\r", "\\r")
        return Literal(fixed)
