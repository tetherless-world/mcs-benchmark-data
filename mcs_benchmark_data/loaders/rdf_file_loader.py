from pathlib import Path
from typing import Optional

from pathvalidate import sanitize_filename
from rdflib import Graph

from mcs_benchmark_data.loaders._buffering_loader import _BufferingLoader
from mcs_benchmark_data.namespace import bind_namespaces


class RdfFileLoader(_BufferingLoader):
    def __init__(self, *, file_path: Optional[Path] = None, format="ttl", **kwds):
        _BufferingLoader.__init__(self, **kwds)
        self.__file_path = file_path
        self.__format = format

    def _flush(self, models):
        file_path = self.__file_path
        if file_path is None:
            file_path = self._loaded_data_dir_path / (
                sanitize_filename(self._pipeline_id) + "." + self.__format
            )
        graph = Graph()
        bind_namespaces(graph.namespace_manager)
        for model in models:
            model.to_rdf(graph=graph)
        with open(file_path, "w+b") as file_:
            graph.serialize(destination=file_, format=self.__format)
