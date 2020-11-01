from mcs_benchmark_data.path import DATA_DIR_PATH
from rdflib import Graph
import bz2


def assert_valid_rdf_loaded(pipeline_id: str):

    loaded_data_dir_path = DATA_DIR_PATH / pipeline_id / "loaded"
    assert loaded_data_dir_path.is_dir()
    rdf_bz2_file_path = loaded_data_dir_path / (pipeline_id + ".ttl.bz2")
    assert rdf_bz2_file_path.is_file()

    new_graph = Graph()
    with open(rdf_bz2_file_path, "rb") as rdf_bz2_file:
        with bz2.open(rdf_bz2_file, "rb") as rdf_file:
            new_graph.parse(source=rdf_file, format="ttl")
