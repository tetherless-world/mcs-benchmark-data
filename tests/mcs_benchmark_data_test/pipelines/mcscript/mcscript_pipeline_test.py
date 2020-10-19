import bz2
from io import StringIO

from rdflib import Graph
from rdflib.compare import to_isomorphic
from rdflib.parser import StringInputSource

from mcs_benchmark_data.path import DATA_DIR_PATH
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_pipeline import (
    MCScriptBenchmarkPipeline,
)


def test_extract_transform_load(tmp_path):
    MCScriptBenchmarkPipeline(
        dev_json_file="dev-data_small.json",
        test_json_file="test-data_small.json",
        train_json_file="train-data_small.json",
    ).extract_transform_load()
    loaded_data_dir_path = DATA_DIR_PATH / "loaded" / MCScriptBenchmarkPipeline.ID
    assert loaded_data_dir_path.is_dir()
    rdf_bz2_file_path = loaded_data_dir_path / (
        MCScriptBenchmarkPipeline.ID + ".jsonld.bz2"
    )
    assert rdf_bz2_file_path.is_file()

    new_graph = Graph()
    with open(rdf_bz2_file_path, "rb") as rdf_bz2_file:
        with bz2.open(rdf_bz2_file, "rb") as rdf_file:
            new_graph.parse(source=rdf_file, format="json-ld")
