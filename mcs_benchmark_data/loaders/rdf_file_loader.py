from pathlib import Path
from typing import Optional

from pathvalidate import sanitize_filename
from rdflib import Graph
import bz2

from tqdm import tqdm

from mcs_benchmark_data.loaders._buffering_loader import _BufferingLoader
from mcs_benchmark_data.namespace import bind_namespaces


class RdfFileLoader(_BufferingLoader):
    __CONTEXT = [
        "https://tetherless-world.github.io/mcs-ontology/utils/context.jsonld",
        {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "mcs": "http://purl.org/twc/mcs/",
        },
    ]

    def __init__(
        self,
        *,
        compress: bool = True,
        file_path: Optional[Path] = None,
        format="json-ld",
        **kwds,
    ):
        _BufferingLoader.__init__(self, **kwds)
        self.__compress = compress
        self.__file_path = file_path
        self.__format = format

    def _flush(self, models):
        graph = Graph()
        bind_namespaces(graph.namespace_manager)
        self._logger.info("serializing %d models to RDF", len(models))
        for model in tqdm(models):
            if isinstance(model, dict):
                print(model)
            model.to_rdf(graph=graph)
        self._logger.info("serialized %d models to RDF", len(models))

        file_path = self.__file_path
        if file_path is None:
            file_name_parts = [
                sanitize_filename(self._pipeline_id),
                self.__format.replace("-", ""),
            ]
            if self.__compress:
                file_name_parts.append("bz2")
            file_name = ".".join(file_name_parts)
            file_path = self._loaded_data_dir_path / file_name

        graph_serialize_kwds = {"context": self.__CONTEXT, "format": self.__format}

        self._logger.info("writing graph to %s", file_path)
        with open(file_path, "w+b") as file_:
            if self.__compress:
                with bz2.open(file_, "wb") as bz2_file:
                    graph.serialize(destination=bz2_file, **graph_serialize_kwds)
            else:
                graph.serialize(destination=file_, **graph_serialize_kwds)
        self._logger.info("wrote graph to %s", file_path)
