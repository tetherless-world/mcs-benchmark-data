import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_pipeline import (
    MCScriptBenchmarkPipeline,
)
from mcs_benchmark_data.pipelines.mcscript.mcscript_benchmark_file_names import (
    MCScriptBenchmarkFileNames,
)


def test_extract_transform_load():
    MCScriptBenchmarkPipeline(
        file_names=MCScriptBenchmarkFileNames(
            meta_data="metadata.json",
            dev_samples="dev-data.xml",
            train_samples="train-data.xml",
            test_samples="test-data.xml",
        ),
    ).extract_transform_load()

    loaded_data_dir_path = DATA_DIR_PATH / "loaded" / MCScriptBenchmarkPipeline.ID
    assert loaded_data_dir_path.is_dir()
    rdf_bz2_file_path = loaded_data_dir_path / (
        MCScriptBenchmarkPipeline.ID + ".turtle.bz2"
    )
    assert rdf_bz2_file_path.is_file()

    new_graph = Graph()
    with open(rdf_bz2_file_path, "rb") as rdf_bz2_file:
        with bz2.open(rdf_bz2_file, "rb") as rdf_file:
            new_graph.parse(source=rdf_file, format="ttl")
