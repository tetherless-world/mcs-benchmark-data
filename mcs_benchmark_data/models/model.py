from dataclasses import dataclass
from rdflib import URIref

@dataclass(frozen = True)
class Model():
    id: URIref