from rdflib import Namespace
from rdflib.namespace import NamespaceManager

MCS = Namespace("http://purl.org/twc/mcs/")
OWL = Namespace("http://www.w3.org/2002/07/owl")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = Namespace("http://schema.org/")
VANN = Namespace("http://purl.org/vocab/vann#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


def bind_namespaces(namespace_manager: NamespaceManager):
    namespace_manager.bind("mcs", MCS)
    namespace_manager.bind("owl", OWL)
    namespace_manager.bind("rdf", RDF)
    namespace_manager.bind("rdfs", RDFS)
    namespace_manager.bind("schema", SCHEMA)
    namespace_manager.bind("vann", VANN)
    namespace_manager.bind("xsd", XSD)
